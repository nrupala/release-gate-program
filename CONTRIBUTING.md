# Contributing

Thank you for considering a contribution. This project is maintained by AIMLDS
(2351485 ALBERTA INC.) and contributions are welcome under the project's licence.

This repository is a documentation program: the product is the document set
itself (the release-gate program documents). Contributions are document
changes — corrections, clarifications, and updates to the program text.

## How to contribute

1. Open an issue first for anything beyond a trivial fix, so the change can be discussed.
2. Fork the repository and make your change on a branch.
3. Keep changes focused; unrelated edits belong in their own pull request.
4. Add your change to the CHANGELOG's *Unreleased* section in the same pull request —
   a plain-language line a user would understand. If the change fixes a security issue,
   name the CVE or similar identifier where one exists.
5. Open a pull request describing what changed and why. A maintainer reviews every PR;
   expect a first response within two weeks.

## Checks are part of the change

- New or edited documents must keep every relative link valid: the document
  validation script checks that each relative Markdown link in the repository
  points at a file that exists.
- The full check must pass before a PR is merged. Run it with:
  `python3 scripts/check_docs.py`
  (CI runs the same check on every pull request.)
- A check that CI does not run does not count: if you add a check, wire it into
  CI in the same change.

## Conduct and licensing

Be civil and specific in issues and reviews. By contributing you agree your contribution
is provided under the project's licence.
