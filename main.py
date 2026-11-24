#!/usr/bin/env python3
"""Write a two-line explanation of a queue to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, prints it to stdout,
and enforces the competition gate: 1 to 400 characters, not only white
space, exactly two lines, each line a single sentence, no em dash.
Pass --check to validate without writing anything.
"""

import os
import sys
from pathlib import Path

ENTRY = (
    "A queue is a line of people waiting their turn, like a caterpillar "
    "that crawls forward one small wiggle each time the shop lets the "
    "person at its head go in.\n"
    "The caterpillar fits because a queue really does move in small steps "
    "from the front, one person at a time, but it leaves out that the "
    "people can chat, get bored, or walk away, while a caterpillar never "
    "chooses where it goes."
)

MIN_CHARS = 1
MAX_CHARS = 400
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    args = [a for a in sys.argv[1:] if a != "--check"]
    if args:
        return Path(args[0])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-400")
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\u2014" in text:
        raise ValueError("entry contains an em dash")
    lines = text.split("\n")
    if len(lines) != 2:
        raise ValueError(f"entry has {len(lines)} lines, expected 2")
    for line in lines:
        if not line.strip():
            raise ValueError("entry has an empty line")
        if line.count(".") != 1 or not line.endswith("."):
            raise ValueError("each line must be exactly one sentence")
    return chars


def main() -> int:
    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    if "--check" in sys.argv[1:]:
        lines = ENTRY.split("\n")
        print(
            f"entry is valid: {chars} characters, "
            f"{len(lines)} lines, "
            f"line 1 {len(lines[0])} chars, line 2 {len(lines[1])} chars"
        )
        return 0

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ENTRY, encoding="utf-8")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
