#!/usr/bin/env python3
"""Document-set validation for the release-gate-program repository.

The product of this repository is its document set, so the automated check
suite validates the documents themselves:

- every relative Markdown link in every ``*.md`` file resolves to a file
  that exists in the repository;
- every ``*.md`` file is non-empty and decodes as UTF-8.

Exits 0 when the document set is valid, 1 with one line per problem
otherwise. Run it with: ``python3 scripts/check_docs.py`` — an optional
first argument overrides the document root (used by the test suite).
"""

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "data:")


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = (
        Path(args[0]).resolve()
        if args
        else Path(__file__).resolve().parent.parent
    )
    problems = []
    md_files = sorted(p for p in root.rglob("*.md") if ".git" not in p.parts)
    if not md_files:
        problems.append("no Markdown files found")
    links_checked = 0
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            problems.append(f"{md.relative_to(root)}: unreadable: {exc}")
            continue
        if not text.strip():
            problems.append(f"{md.relative_to(root)}: file is empty")
            continue
        for target in LINK_RE.findall(text):
            if target.startswith(SKIP_PREFIXES):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            links_checked += 1
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                problems.append(
                    f"{md.relative_to(root)}: broken relative link -> {target}"
                )
    for problem in problems:
        print(f"FAIL: {problem}")
    print(
        f"check_docs: {len(md_files)} markdown files, "
        f"{links_checked} relative links checked, {len(problems)} problem(s)"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
