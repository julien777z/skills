from argparse import ArgumentParser
from ast import (
    AST,
    AnnAssign,
    Assert,
    Assign,
    AsyncFor,
    AsyncFunctionDef,
    AsyncWith,
    Await,
    Call,
    ClassDef,
    Constant,
    ExceptHandler,
    Expr,
    For,
    FunctionDef,
    If,
    Import,
    ImportFrom,
    Module,
    Name,
    Raise,
    Return,
    Try,
    TryStar,
    While,
    With,
    get_docstring,
    match_case,
    parse,
    stmt,
    unparse,
    walk,
)
from enum import StrEnum
from pathlib import Path
from typing import Final

DATA_CLASS_MODULES: Final[set[str]] = {"dataclasses", "pydantic.dataclasses", "pydantic"}
NAMED_TUPLE_MODULES: Final[set[str]] = {"typing", "typing_extensions"}
MIGRATION_DOCSTRING_FUNCTIONS: Final[set[str]] = {"upgrade", "downgrade"}
MAX_TEST_NAME_WORDS: Final[int] = 8


class ParagraphCandidateKind(StrEnum):
    """Name the relationship between adjacent statements that may need a blank line."""

    GUARD_TO_GUARD = "guard-to-guard"
    GUARD_TO_NEXT_STAGE = "guard-to-next-stage"
    VALUE_TO_VALIDATION = "value-to-validation"
    OPERATION_TO_NEXT_STAGE = "operation-to-next-stage"


def declaration_lines(declaration: ClassDef, expressions: set[str]) -> list[int]:
    """Locate model declarations matching the imported spellings."""

    declarations = [item.func if isinstance(item, Call) else item for item in declaration.decorator_list]
    declarations.extend(declaration.bases)

    return [item.lineno for item in declarations if unparse(item) in expressions]


def data_class_spellings(module: Module) -> set[str]:
    """Collect the names a module uses to declare data classes and named tuples."""

    spellings: set[str] = set()

    for node in walk(module):
        if isinstance(node, Import):
            for imported in node.names:
                name = imported.asname or imported.name

                if imported.name in DATA_CLASS_MODULES:
                    spellings.add(f"{name}.dataclass")

                    if imported.name == "pydantic":
                        spellings.add(f"{name}.dataclasses.dataclass")

                if imported.name in NAMED_TUPLE_MODULES:
                    spellings.add(f"{name}.NamedTuple")

        if isinstance(node, ImportFrom):
            for imported in node.names:
                if (
                    node.module in DATA_CLASS_MODULES and imported.name == "dataclass"
                    or node.module in NAMED_TUPLE_MODULES and imported.name == "NamedTuple"
                ):
                    spellings.add(imported.asname or imported.name)

                if node.module == "pydantic" and imported.name == "dataclasses":
                    spellings.add(f"{imported.asname or imported.name}.dataclass")

    return spellings


def is_migration_revision(module: Module) -> bool:
    """Tell whether a module is a migration revision file."""

    assigned = {
        target.id
        for statement in module.body
        if isinstance(statement, (Assign, AnnAssign))
        for target in (statement.targets if isinstance(statement, Assign) else [statement.target])
        if isinstance(target, Name)
    }

    return {"revision", "down_revision"} <= assigned


def statement_start(statement: stmt) -> int:
    """Return the first line of a statement or its decorators."""

    decorators = getattr(statement, "decorator_list", [])

    return min([statement.lineno, *(decorator.lineno for decorator in decorators)])


def statement_end(statement: stmt) -> int:
    """Return the last line of a statement."""

    return statement.end_lineno or statement.lineno


def has_blank_line(lines: list[str], previous_end: int, next_start: int) -> bool:
    """Tell whether a blank line separates two statements."""

    return any(not line.strip() for line in lines[previous_end:next_start - 1])


def statement_lists(node: AST) -> list[list[stmt]]:
    """Return the statement lists an AST node owns."""

    blocks: list[list[stmt]] = []

    if isinstance(
        node,
        (
            FunctionDef,
            AsyncFunctionDef,
            ClassDef,
            If,
            For,
            AsyncFor,
            While,
            With,
            AsyncWith,
            Try,
            TryStar,
            ExceptHandler,
            match_case,
        ),
    ):
        blocks.append(node.body)

    if isinstance(node, (If, For, AsyncFor, While, Try, TryStar)):
        blocks.append(node.orelse)

    if isinstance(node, (Try, TryStar)):
        blocks.append(node.finalbody)

    return blocks


def called_function(statement: stmt) -> str | None:
    """Return the source text of the function an expression statement calls."""

    if not isinstance(statement, Expr):
        return None

    value = statement.value.value if isinstance(statement.value, Await) else statement.value

    return unparse(value.func) if isinstance(value, Call) else None


def paragraph_kind(previous: stmt, current: stmt) -> ParagraphCandidateKind | None:
    """Classify an adjacent statement pair a reader judges for a paragraph break."""

    if isinstance(previous, If) and isinstance(current, If):
        return ParagraphCandidateKind.GUARD_TO_GUARD

    if isinstance(previous, If) and previous.body and isinstance(previous.body[-1], (Raise, Return)):
        return ParagraphCandidateKind.GUARD_TO_NEXT_STAGE

    if isinstance(previous, (Assign, AnnAssign)) and isinstance(current, If):
        return ParagraphCandidateKind.VALUE_TO_VALIDATION

    operation = called_function(previous)

    if operation and isinstance(current, (Expr, Assign, AnnAssign, Assert)) and called_function(current) != operation:
        return ParagraphCandidateKind.OPERATION_TO_NEXT_STAGE

    return None


def docstring_findings(path: Path, module: Module, lines: list[str]) -> list[str]:
    """Find multi-line ordinary docstrings and docstrings without a blank line after them."""

    findings: list[str] = []
    migration = is_migration_revision(module)

    for node in walk(module):
        if not isinstance(node, (FunctionDef, AsyncFunctionDef, ClassDef)) or get_docstring(node) is None:
            continue

        docstring = node.body[0]
        exempt = (
            migration
            and isinstance(node, (FunctionDef, AsyncFunctionDef))
            and node.name in MIGRATION_DOCSTRING_FUNCTIONS
        )

        end = statement_end(docstring)

        if end > docstring.lineno and not exempt:
            findings.append(f"{path}:{docstring.lineno}: multi-line docstring")

        if len(node.body) > 1 and not has_blank_line(lines, end, statement_start(node.body[1])):
            findings.append(f"{path}:{end}: no blank line after docstring")

    return findings


def adjacent_pairs(statements: list[stmt], lines: list[str]) -> list[tuple[stmt, stmt, int, int]]:
    """Return each adjacent statement pair no blank line separates, with its boundary lines."""

    pairs: list[tuple[stmt, stmt, int, int]] = []

    for previous, current in zip(statements, statements[1:]):
        end = statement_end(previous)
        start = statement_start(current)

        if not has_blank_line(lines, end, start):
            pairs.append((previous, current, end, start))

    return pairs


def layout_findings(path: Path, module: Module, lines: list[str]) -> list[str]:
    """Find multi-line statements run into the next one and adjacent pairs that may need a blank line."""

    findings: list[str] = []
    functions = [node for node in walk(module) if isinstance(node, (FunctionDef, AsyncFunctionDef))]
    function_blocks = {
        id(statements) for function in functions for node in walk(function) for statements in statement_lists(node)
    }

    blocks = [module.body, *(statements for node in walk(module) for statements in statement_lists(node))]

    for statements in blocks:
        for previous, current, end, start in adjacent_pairs(statements, lines):
            is_docstring = (
                previous is statements[0] and isinstance(previous, Expr) and isinstance(previous.value, Constant)
            )

            is_import_group = isinstance(previous, (Import, ImportFrom)) and isinstance(current, (Import, ImportFrom))
            kind = paragraph_kind(previous, current)

            if end > previous.lineno and not is_docstring and not is_import_group:
                findings.append(f"{path}:{end}-{start}: no blank line after multi-line statement")
            elif kind and id(statements) in function_blocks and start == end + 1:
                findings.append(f"{path}:{end}-{start}: paragraph candidate, {kind}")

    return list(dict.fromkeys(findings))


def long_test_name_findings(path: Path, module: Module) -> list[str]:
    """Find test function names longer than the testing rule allows."""

    findings: list[str] = []

    for node in walk(module):
        if not isinstance(node, (FunctionDef, AsyncFunctionDef)) or not node.name.startswith("test_"):
            continue

        words = [word for word in node.name.removeprefix("test_").split("_") if word]

        if len(words) > MAX_TEST_NAME_WORDS:
            findings.append(f"{path}:{node.lineno}: test name of {len(words)} words after test_")

    return findings


def python_findings(path: Path) -> list[str]:
    """Find the Python rule shapes a reader can check mechanically in one file."""

    source = path.read_text(encoding="utf-8")
    module = parse(source, filename=str(path))
    lines = source.splitlines()
    findings: list[str] = []
    spellings = data_class_spellings(module)

    if get_docstring(module) is not None:
        findings.append(f"{path}:{module.body[0].lineno}: module docstring")

    for node in walk(module):
        if isinstance(node, ClassDef):
            for line in declaration_lines(node, spellings):
                findings.append(f"{path}:{line}: data class declaration")

    findings.extend(docstring_findings(path, module, lines))
    findings.extend(layout_findings(path, module, lines))
    findings.extend(long_test_name_findings(path, module))

    return findings


def main() -> None:
    """Print the Python rule findings and paragraph candidates for the given source files."""

    parser = ArgumentParser(description="List Python rule shapes and adjacent statements that may need a blank line.")

    parser.add_argument("files", type=Path, nargs="+")

    options = parser.parse_args()

    for path in options.files:
        for finding in python_findings(path):
            print(finding)


if __name__ == "__main__":
    main()
