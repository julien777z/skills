import argparse
import ast
from enum import StrEnum
from pathlib import Path


class ParagraphCandidateKind(StrEnum):
    """Name the relationship between adjacent review candidates."""

    GUARD_TO_GUARD = "guard-to-guard"
    GUARD_TO_NEXT_STAGE = "guard-to-next-stage"
    VALUE_TO_VALIDATION = "value-to-validation"
    OPERATION_TO_NEXT_STAGE = "operation-to-next-stage"


def statement_kind(
    previous: ast.stmt, current: ast.stmt
) -> ParagraphCandidateKind | None:
    """Classify an adjacent statement pair worth reviewing."""

    if isinstance(previous, ast.If) and isinstance(current, ast.If):
        return ParagraphCandidateKind.GUARD_TO_GUARD

    if (
        isinstance(previous, ast.If)
        and previous.body
        and isinstance(previous.body[-1], (ast.Raise, ast.Return))
    ):
        return ParagraphCandidateKind.GUARD_TO_NEXT_STAGE

    if isinstance(previous, (ast.Assign, ast.AnnAssign)) and isinstance(
        current, ast.If
    ):
        return ParagraphCandidateKind.VALUE_TO_VALIDATION

    if isinstance(previous, ast.Expr) and (
        isinstance(previous.value, ast.Call)
        or isinstance(previous.value, ast.Await)
        and isinstance(previous.value.value, ast.Call)
    ):
        if isinstance(current, (ast.Expr, ast.Assign, ast.AnnAssign)):
            return ParagraphCandidateKind.OPERATION_TO_NEXT_STAGE

    return None


def statement_lists(node: ast.AST) -> list[list[ast.stmt]]:
    """Return statement lists owned by an AST node."""

    blocks: list[list[ast.stmt]] = []

    if isinstance(
        node,
        (
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.ClassDef,
            ast.If,
            ast.For,
            ast.AsyncFor,
            ast.While,
            ast.With,
            ast.AsyncWith,
            ast.Try,
            ast.TryStar,
            ast.ExceptHandler,
            ast.match_case,
        ),
    ):
        blocks.append(node.body)

    if isinstance(
        node, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.TryStar)
    ):
        blocks.append(node.orelse)

    if isinstance(node, (ast.Try, ast.TryStar)):
        blocks.append(node.finalbody)

    return blocks


def candidates(path: Path) -> list[str]:
    """List adjacent stage candidates in functions within a Python file."""

    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    found: list[str] = []

    for function in ast.walk(tree):
        if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        for block in ast.walk(function):
            for statements in statement_lists(block):
                for previous, current in zip(statements, statements[1:]):
                    end = previous.end_lineno
                    if end is None or current.lineno != end + 1:
                        continue

                    kind = statement_kind(previous, current)
                    if kind:
                        found.append(f"{path}:{end}-{current.lineno}: {kind}")

    return list(dict.fromkeys(found))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List adjacent Python statements that may need a paragraph break."
    )

    parser.add_argument("paths", nargs="+", type=Path)

    args = parser.parse_args()

    for file_path in args.paths:
        for candidate in candidates(file_path):
            print(candidate)
