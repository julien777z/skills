import json
import os
import re
import sys
from argparse import ArgumentParser
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Final, TypedDict

PROJECTS_ROOT: Final[Path] = Path.home() / ".claude" / "projects"
SESSION_ENV: Final[str] = "CLAUDE_CODE_SESSION_ID"
ROUND_GAP: Final[timedelta] = timedelta(seconds=90)
LOOP_GAP: Final[timedelta] = timedelta(minutes=10)
STALE_AFTER: Final[timedelta] = timedelta(minutes=10)
PATH_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"(?<![\w/.-])\.?[\w-]+(?:/[\w.-]+)+(?:\.\w{1,5}|/)"
)
COMMAND_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"<command-name>/?([\w:-]+)</command-name>"
)
SCRATCH_MARKERS: Final[tuple[str, ...]] = ("tmp/", "scratchpad", ".claude/", "home/")


class Launch(TypedDict):
    """One Agent tool call in the session transcript."""

    at: str
    description: str
    agent_type: str
    scope: list[str]


class Subagent(TypedDict):
    """One subagent's launch, run and cost."""

    description: str
    agent_type: str
    state: str
    started: str
    last_activity: str
    seconds: float
    fresh_tokens: int
    cached_tokens: int
    tool_uses: int
    scope: list[str]


class Round(TypedDict):
    """Subagents launched together."""

    number: int
    started: str
    subagents: list[Subagent]


class Loop(TypedDict):
    """One burst of subagent work, the skills invoked during it, and its rounds."""

    skills: list[str]
    running: bool
    started: str
    last_activity: str
    seconds: float
    fresh_tokens: int
    cached_tokens: int
    subagent_count: int
    rounds: list[Round]
    per_scope: dict[str, int]
    overlapping_scope: dict[str, list[str]]


def parse_time(value: str) -> datetime:
    """Read an ISO 8601 transcript timestamp."""

    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def read_records(path: Path) -> list[dict[str, object]]:
    """Return a JSONL file's records, skipping lines that are not JSON objects."""

    records: list[dict[str, object]] = []

    for line in path.read_text(errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        if isinstance(record, dict):
            records.append(record)

    return records


def content_blocks(record: dict[str, object]) -> list[dict[str, object]]:
    """Return a transcript record's message content blocks."""

    message = record.get("message")
    content = message.get("content") if isinstance(message, dict) else None

    if not isinstance(content, list):
        return []

    return [block for block in content if isinstance(block, dict)]


def prompt_scope(prompt: str) -> list[str]:
    """Return the repository files and folders a subagent's prompt names."""

    paths = {
        match
        for match in PATH_PATTERN.findall(prompt)
        if not any(marker in match for marker in SCRATCH_MARKERS)
    }

    return sorted(paths)


def read_session(transcript: Path) -> tuple[dict[str, Launch], list[tuple[str, str]]]:
    """Return each Agent call keyed by tool-use id, and every skill invocation with its time."""

    launches: dict[str, Launch] = {}
    skills: list[tuple[str, str]] = []

    for record in read_records(transcript):
        at = str(record.get("timestamp", ""))
        message = record.get("message")
        text = message.get("content") if isinstance(message, dict) else None

        if record.get("type") == "user" and isinstance(text, str):
            skills.extend((at, name) for name in COMMAND_PATTERN.findall(text))

        for block in content_blocks(record):
            if block.get("type") == "text":
                found = COMMAND_PATTERN.findall(str(block.get("text", "")))
                skills.extend((at, name) for name in found)

            arguments = block.get("input")

            if block.get("type") != "tool_use" or not isinstance(arguments, dict):
                continue

            if block.get("name") == "Skill":
                skills.append((at, str(arguments.get("skill", ""))))
            elif block.get("name") == "Agent":
                launches[str(block.get("id"))] = Launch(
                    at=at,
                    description=str(arguments.get("description", "")),
                    agent_type=str(arguments.get("subagent_type", "general-purpose")),
                    scope=prompt_scope(str(arguments.get("prompt", ""))),
                )

    return launches, skills


def read_subagent(
    record_path: Path, launch: Launch | None, meta: dict[str, object]
) -> Subagent:
    """Return one subagent's run and cost from its own transcript."""

    records = read_records(record_path)
    stamps = [str(record["timestamp"]) for record in records if record.get("timestamp")]
    fresh = 0
    cached = 0
    tool_uses = 0

    for record in records:
        message = record.get("message")
        usage = message.get("usage") if isinstance(message, dict) else None

        if isinstance(usage, dict):
            for key, value in usage.items():
                if isinstance(value, int) and key.endswith("tokens"):
                    if key == "cache_read_input_tokens":
                        cached += value
                    else:
                        fresh += value

        tool_uses += sum(
            1 for block in content_blocks(record) if block.get("type") == "tool_use"
        )

    started = launch["at"] if launch else (stamps[0] if stamps else "")
    last = stamps[-1] if stamps else started
    seconds = (
        (parse_time(last) - parse_time(started)).total_seconds() if started else 0.0
    )

    return Subagent(
        description=str(
            meta.get("description") or (launch["description"] if launch else "")
        ),
        agent_type=str(
            meta.get("agentType") or (launch["agent_type"] if launch else "")
        ),
        state=subagent_state(meta.get("finished") is True, last),
        started=started,
        last_activity=last,
        seconds=round(max(seconds, 0.0), 1),
        fresh_tokens=fresh,
        cached_tokens=cached,
        tool_uses=tool_uses,
        scope=launch["scope"] if launch else [],
    )


def subagent_state(finished: bool, last_activity: str) -> str:
    """Return finished, running, or stopped for a subagent that went quiet before finishing."""

    if finished:
        return "finished"

    if last_activity and datetime.now(UTC) - parse_time(last_activity) > STALE_AFTER:
        return "stopped"

    return "running"


def new_loop(subagent: Subagent) -> Loop:
    """Start a loop at this subagent."""

    return Loop(
        skills=[],
        running=False,
        started=subagent["started"],
        last_activity=subagent["last_activity"],
        seconds=0.0,
        fresh_tokens=0,
        cached_tokens=0,
        subagent_count=0,
        rounds=[],
        per_scope={},
        overlapping_scope={},
    )


def group_loops(subagents: list[Subagent], skills: list[tuple[str, str]]) -> list[Loop]:
    """Group subagents into loops of continuous work, and each loop into rounds by launch time."""

    loops: list[Loop] = []

    for subagent in sorted(subagents, key=lambda found: found["started"]):
        start = parse_time(subagent["started"])

        if not loops or start - parse_time(loops[-1]["last_activity"]) > LOOP_GAP:
            loops.append(new_loop(subagent))

        loop = loops[-1]
        rounds = loop["rounds"]

        if not rounds or start - parse_time(rounds[-1]["started"]) > ROUND_GAP:
            rounds.append(
                Round(number=len(rounds) + 1, started=subagent["started"], subagents=[])
            )

        rounds[-1]["subagents"].append(subagent)
        loop["running"] = loop["running"] or subagent["state"] == "running"
        loop["last_activity"] = max(loop["last_activity"], subagent["last_activity"])
        loop["fresh_tokens"] += subagent["fresh_tokens"]
        loop["cached_tokens"] += subagent["cached_tokens"]
        loop["subagent_count"] += 1

        for path in subagent["scope"]:
            loop["per_scope"][path] = loop["per_scope"].get(path, 0) + 1

    for loop in loops:
        began = parse_time(loop["started"]) - LOOP_GAP
        ended = parse_time(loop["last_activity"])
        readers: dict[str, set[str]] = {}

        loop["seconds"] = round(
            (ended - parse_time(loop["started"])).total_seconds(), 1
        )
        loop["skills"] = list(
            dict.fromkeys(
                name for at, name in skills if began <= parse_time(at) <= ended
            )
        )

        for found in loop["rounds"]:
            for subagent in found["subagents"]:
                for path in subagent["scope"]:
                    readers.setdefault(path, set()).add(subagent["description"])

        loop["overlapping_scope"] = {
            path: sorted(names) for path, names in readers.items() if len(names) > 1
        }

    return loops


def find_session(session_id: str) -> Path:
    """Return the transcript of the session with this id."""

    matches = sorted(PROJECTS_ROOT.glob(f"*/{session_id}.jsonl"))

    if not matches:
        raise SystemExit(
            f"No transcript for session {session_id} under {PROJECTS_ROOT}"
        )

    return matches[0]


def main() -> None:
    """Print the session's running loops and its last finished loops as JSON."""

    parser = ArgumentParser(
        description="Summarize the subagent loops of a Claude Code session."
    )
    parser.add_argument(
        "--session",
        default=os.environ.get(SESSION_ENV),
        help="session id; the current one by default",
    )
    parser.add_argument(
        "--previous", type=int, default=5, help="how many finished loops to include"
    )
    arguments = parser.parse_args()

    if not arguments.session:
        raise SystemExit(
            f"Pass --session, or run inside a session that sets {SESSION_ENV}"
        )

    transcript = find_session(arguments.session)
    launches, skills = read_session(transcript)
    subagents: list[Subagent] = []

    for meta_path in sorted(
        (transcript.with_suffix("") / "subagents").glob("agent-*.meta.json")
    ):
        meta = json.loads(meta_path.read_text())
        record_path = meta_path.with_name(
            meta_path.name.replace(".meta.json", ".jsonl")
        )

        if isinstance(meta, dict) and record_path.exists():
            subagents.append(
                read_subagent(
                    record_path, launches.get(str(meta.get("toolUseId"))), meta
                )
            )

    loops = group_loops(subagents, skills)
    running = [loop for loop in loops if loop["running"]]
    previous = [loop for loop in loops if not loop["running"]][-arguments.previous :][
        ::-1
    ]

    json.dump(
        {"session": arguments.session, "running": running, "previous": previous},
        sys.stdout,
        indent=1,
    )


if __name__ == "__main__":
    main()
