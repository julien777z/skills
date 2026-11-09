from argparse import ArgumentParser
from ast import Call, ClassDef, Import, ImportFrom, get_docstring, parse, unparse, walk
from pathlib import Path

DATA_CLASS_MODULES = {"dataclasses", "pydantic.dataclasses", "pydantic"}
NAMED_TUPLE_MODULES = {"typing", "typing_extensions"}


def declaration_lines(declaration: ClassDef, expressions: set[str]) -> list[int]:
    """Locate model declarations matching the imported spellings."""

    declarations = [item.func if isinstance(item, Call) else item for item in declaration.decorator_list]
    declarations.extend(declaration.bases)

    return [item.lineno for item in declarations if unparse(item) in expressions]


def python_findings(path: Path) -> list[str]:
    """Find prohibited module docstrings and Python data-class declarations."""

    module = parse(path.read_bytes(), filename=str(path))
    findings: list[str] = []
    declarations: set[str] = set()

    if get_docstring(module) is not None:
        findings.append(f"{path}:{module.body[0].lineno}: module docstring")

    for node in walk(module):
        if isinstance(node, Import):
            for imported in node.names:
                name = imported.asname or imported.name

                if imported.name in DATA_CLASS_MODULES:
                    declarations.add(f"{name}.dataclass")
                    if imported.name == "pydantic":
                        declarations.add(f"{name}.dataclasses.dataclass")
                if imported.name in NAMED_TUPLE_MODULES:
                    declarations.add(f"{name}.NamedTuple")
        if isinstance(node, ImportFrom):
            for imported in node.names:
                if (
                    node.module in DATA_CLASS_MODULES and imported.name == "dataclass"
                    or node.module in NAMED_TUPLE_MODULES and imported.name == "NamedTuple"
                ):
                    declarations.add(imported.asname or imported.name)
                if node.module == "pydantic" and imported.name == "dataclasses":
                    declarations.add(f"{imported.asname or imported.name}.dataclass")

    for node in walk(module):
        if isinstance(node, ClassDef):
            for line in declaration_lines(node, declarations):
                findings.append(f"{path}:{line}: data class declaration")

    return findings


def main() -> None:
    """Print the Python rule findings for the review's source files."""

    parser = ArgumentParser()
    parser.add_argument("files", type=Path, nargs="+")
    options = parser.parse_args()

    for path in options.files:
        for finding in python_findings(path):
            print(finding)


if __name__ == "__main__":
    main()
