# Changelog

All notable changes to release-gate-program are recorded here, per release, in plain language
a user can act on — never a raw commit log. Entries are added with the change itself
(see CONTRIBUTING), and any security fix names the CVE or similar identifier where
one exists.

## [Unreleased]

### Added

- SECURITY.md (GitHub Private Vulnerability Reporting route), CONTRIBUTING.md,
  TEST-PLAN.md, NOTICE, and a CI document-validation check
  (`scripts/check_docs.py`) that verifies every relative Markdown link in the
  document set resolves, with a unit test suite for the validator itself
  (`tests/test_check_docs.py`).
