from argparse import ArgumentParser
from collections.abc import Iterator
from ast import AsyncFunctionDef, ClassDef, FunctionDef, Module, Name, parse, walk
from enum import StrEnum
from http import HTTPStatus
from pathlib import Path
from re import findall
from typing import Final

ARTICLES: Final[frozenset[str]] = frozenset({"a", "an", "the"})
MAX_NAME_WORDS: Final[int] = 8
HELPER_PACKAGES: Final[frozenset[str]] = frozenset({"utils", "fixtures"})
NON_MODEL_NAMES: Final[frozenset[str]] = frozenset(
    {
        "Any",
        "AsyncGenerator",
        "AsyncIterator",
        "Awaitable",
        "Callable",
        "Coroutine",
        "Generator",
        "Iterator",
        "Literal",
        "Optional",
        "Path",
        "Self",
        "Union",
    }
)

STATUS_CODES: Final[frozenset[int]] = frozenset(status.value for status in HTTPStatus)


class NamingCheck(StrEnum):
    """One block of the printed report, labeled by its check."""

    ARTICLE_LED = "article-led name"
    TOO_LONG = "name past eight words"
    STATUS_TOKEN = "numeric status token"
    NOUN_OVERLAP = "class or module noun overlap"
    MODEL_HELPER = "model-returning helper (name it create_<shape>)"
    OTHER_HELPER = "other helper (first word shown)"


NAME_CHECKS: Final[tuple[NamingCheck, ...]] = (
    NamingCheck.ARTICLE_LED,
    NamingCheck.TOO_LONG,
    NamingCheck.STATUS_TOKEN,
    NamingCheck.NOUN_OVERLAP,
)

HELPER_CHECKS: Final[tuple[NamingCheck, ...]] = (
    NamingCheck.MODEL_HELPER,
    NamingCheck.OTHER_HELPER,
)


def stem(word: str) -> str:
    """Reduce a word to its singular, lowercase stem."""

    word = word.lower()

    return word[:-1] if len(word) > 3 and word.endswith("s") else word


def words_of(identifier: str) -> list[str]:
    """Split a snake_case or CamelCase identifier into lowercase words."""

    return [word.lower() for word in findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", identifier)]


def python_files(paths: list[Path]) -> list[Path]:
    """Expand the given files and directories into every Python file beneath them."""

    files: list[Path] = []

    for path in paths:
        files.extend(sorted(path.rglob("*.py")) if path.is_dir() else [path])

    return files


def iter_test_functions(
    node: Module | ClassDef, enclosing: ClassDef | None = None
) -> Iterator[tuple[FunctionDef | AsyncFunctionDef, ClassDef | None]]:
    """Yield every test function with the class that directly encloses it, if any."""

    for child in node.body:
        if isinstance(child, ClassDef):
            yield from iter_test_functions(child, child)
        elif isinstance(child, (FunctionDef, AsyncFunctionDef)) and child.name.startswith("test_"):
            yield child, enclosing


def name_findings(path: Path, module: Module) -> dict[NamingCheck, list[str]]:
    """Run the four name checks over every test function of one module."""

    findings: dict[NamingCheck, list[str]] = {check: [] for check in NAME_CHECKS}
    module_nouns = {stem(word) for word in words_of(path.stem.removeprefix("test_"))}

    for function, enclosing in iter_test_functions(module):
        words = [word for word in function.name.removeprefix("test_").split("_") if word]
        where = f"{path}:{function.lineno}\t{function.name}"
        class_nouns = {stem(word) for word in words_of(enclosing.name) if word != "test"} if enclosing else set()
        overlap = sorted({stem(word) for word in words} & (class_nouns | module_nouns))

        if words and words[0].lower() in ARTICLES:
            findings[NamingCheck.ARTICLE_LED].append(where)

        if len(words) > MAX_NAME_WORDS:
            findings[NamingCheck.TOO_LONG].append(f"{where}\t{len(words)} words")

        if any(word.isdigit() and int(word) in STATUS_CODES for word in words):
            findings[NamingCheck.STATUS_TOKEN].append(where)

        if overlap:
            findings[NamingCheck.NOUN_OVERLAP].append(f"{where}\t{', '.join(overlap)}")

    return findings


def returns_model(function: FunctionDef | AsyncFunctionDef) -> bool:
    """Tell whether the return annotation names a class rather than a builtin or typing form."""

    if function.returns is None:
        return False

    names = [node.id for node in walk(function.returns) if isinstance(node, Name)]

    return any(name[:1].isupper() and name not in NON_MODEL_NAMES for name in names)


def helper_findings(path: Path, module: Module) -> dict[NamingCheck, list[str]]:
    """List the module-level helpers of a utils or fixtures package, split by return type."""

    findings: dict[NamingCheck, list[str]] = {check: [] for check in HELPER_CHECKS}

    if not HELPER_PACKAGES & set(path.parts[:-1]):
        return findings

    for node in module.body:
        if not isinstance(node, (FunctionDef, AsyncFunctionDef)) or node.name.startswith("_"):
            continue

        first_word = node.name.split("_", maxsplit=1)[0]
        row = f"{path}:{node.lineno}\t{node.name}"

        if returns_model(node):
            findings[NamingCheck.MODEL_HELPER].append(row)
        else:
            findings[NamingCheck.OTHER_HELPER].append(f"{row}\t{first_word}")

    return findings


def main() -> None:
    """Print one block per check with a row per hit, and `none` where a check finds nothing."""

    parser = ArgumentParser(description="Print the rubric's test-naming checks over files or directories.")
    parser.add_argument("paths", nargs="+", type=Path, help="Test files or directories to check.")

    arguments = parser.parse_args()

    results: dict[NamingCheck, list[str]] = {check: [] for check in NamingCheck}

    for path in python_files(arguments.paths):
        module = parse(path.read_text(encoding="utf-8"), filename=str(path))

        for check, rows in (name_findings(path, module) | helper_findings(path, module)).items():
            results[check].extend(rows)

    for check, rows in results.items():
        print(f"== {check}")
        print("\n".join(rows) if rows else "none")


if __name__ == "__main__":
    main()
