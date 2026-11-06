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
| Validator tests (`tests/test_check_docs.py`) | The validator itself: a valid set passes; a broken relative link fails; an empty document fails; external links are not treated as files | `python3 -m unittest discover -s tests -v` | Yes — `.github/workflows/ci.yml` |
| Document validation (`scripts/check_docs.py`) | Every `*.md` file is non-empty and UTF-8 readable; every relative Markdown link resolves to a file that exists | `python3 scripts/check_docs.py` | Yes — `.github/workflows/ci.yml` |

## CI gates

- Validator test suite and document validation green on every push and
  pull request to `main`; a broken relative link, an empty/unreadable
  document, or a failing validator test blocks merge.

## Cadence

- Every pull request: validator tests + document validation.
- Every release candidate: the release-readiness run (checker + evidence
  reads), per the house Release-Readiness Standard.

## Coverage bar

No numeric floor; new or edited documents land with the validation check
passing, per CONTRIBUTING.
