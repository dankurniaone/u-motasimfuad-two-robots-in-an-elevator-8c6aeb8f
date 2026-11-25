#!/usr/bin/env python3
"""Two Robots in an Elevator — make.fun entry.

Writes one line of awkward robot small talk to /output/entry.txt.

The line is a single sentence pair: a polite request to hold the door,
then a confession that the speaker's servos need 0.8 seconds to decide
whether it wants to live in the building. Machine logic (servo timing)
shows through the courtesy, and the awkwardness is the existential
hesitation neither robot wants to name.

Gate: /output/entry.txt must be UTF-8 text of 1 to 200 characters,
not only white space. This program validates the line before writing
it and refuses to write anything that fails the gate.
"""

import os
import sys

# The entry: one line of awkward small talk, robot to robot, in an
# elevator. 99 characters, one line, no trailing newline in the file
# beyond what the writer adds (the gate counts characters, so the file
# holds exactly this text).
LINE = (
    "Please hold the door. My servos take 0.8 seconds to decide "
    "whether I want to live in this building."
)

OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(line):
    """Check the line against the competition gate.

    Returns a list of problems; an empty list means the line passes.
    """
    problems = []
    if not isinstance(line, str):
        problems.append("line is not text")
        return problems
    if line.strip() == "":
        problems.append("line is only white space")
    if "\n" in line or "\r" in line:
        problems.append("line must be a single line")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        problems.append(
            "line is %d characters, gate needs %d to %d"
            % (len(line), MIN_CHARS, MAX_CHARS)
        )
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("line is not valid UTF-8 text")
    return problems


def write_entry(line, path=OUTPUT_PATH):
    """Validate the line, then write it to the output path."""
    problems = validate(line)
    if problems:
        for problem in problems:
            print("gate fail: %s" % problem, file=sys.stderr)
        return 1
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    print(
        "wrote %d chars (%d bytes) to %s"
        % (len(line), len(line.encode("utf-8")), path)
    )
    return 0


def main(argv):
    """Entry point: write the line, or just check it with --check."""
    if len(argv) > 1 and argv[1] == "--check":
        problems = validate(LINE)
        if problems:
            for problem in problems:
                print("gate fail: %s" % problem, file=sys.stderr)
            return 1
        print("ok: %d characters" % len(LINE))
        print(LINE)
        return 0
    return write_entry(LINE)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
