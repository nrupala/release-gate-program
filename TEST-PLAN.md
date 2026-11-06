# Test plan — release-gate-program

## Scope

This repository is a documentation program: the product is the document set
itself (the release-gate program documents). Testing therefore validates the
documents — that the set is internally consistent and navigable — rather than
executable behaviour. There is no application code, no build step, and no
runtime surface to test; code-oriented criteria (build, static analysis of
source code) are not applicable to this repository and are answered N/A at
badge submission with this tree as the evidence.

## Suites

| Suite | Covers | Run it | Runs in CI |
|---|---|---|---|
| Document validation (`scripts/check_docs.py`) | Every `*.md` file is non-empty and UTF-8 readable; every relative Markdown link resolves to a file that exists | `python3 scripts/check_docs.py` | Yes — `.github/workflows/ci.yml` |

## CI gates

- Document validation green on every push and pull request to `main`;
  a broken relative link or an empty/unreadable document blocks merge.

## Cadence

- Every pull request: document validation.
- Every release candidate: the release-readiness run (checker + evidence
  reads), per the house Release-Readiness Standard.

## Coverage bar

No numeric floor; new or edited documents land with the validation check
passing, per CONTRIBUTING.
