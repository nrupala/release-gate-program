# Release Gate — Release Testing & Cybersecurity Program

A complete, evidence-based program for release testing, cybersecurity
assessment, gap testing, and attack prevention — for conventional,
zero-trust / zero-knowledge, and agentic software.

**The readiness rule.** A capability, control, or verdict counts only
when a gate run produced filed evidence for it. Everything else is
PLANNED, NOT RUN, or PROVISIONAL — named as such, never smoothed over.
There is no percentage compliance score and no automatic signing at a
threshold: the bar is evidence, then a clean watched week.

**The standing truth.** There is no zero threat. This program never
certifies "zero threat" or "unhackable" — in a verdict, a release
record, or product copy. The goal is to raise the cost of compromise
until attack is mathematically, cryptographically, or economically
infeasible, and to state exactly how far that has been proven.

## What's inside

- `PROGRAM.md` — the complete program statement: the gate and its test
  families (including attacker-view and agentic-systems families), the
  control standard (OWASP ASVS / MASVS, OAuth 2.1, MCP authorization,
  SOC 2-style operations), the five-criterion release bar and the
  one-week release-candidate rule, money-surface rules, the threat
  basis (MITRE ATT&CK plus live indicator feeds), ethical-hacking
  practice and named tooling, zero-knowledge and agent testing,
  formal methods and the blind-spot register, prevention patterns,
  and the governance cadence.
- `LICENSE` — Apache License 2.0.
- `COMMERCIAL.md` — dual licensing: commercial terms for proprietary
  use, certification, and support.

## Provenance

This program is the working system of an independent software
practice (2351485 ALBERTA INC., operating as AIMLDS). It runs on every
release we ship; the register of verdicts and the evidence packs stay
private, because they describe live systems. The method is open so it
can be scrutinised, adopted, and improved — scrutiny is the point.

Guardian Mesh, the defined-flow protection layer this program
specifies, is at https://github.com/nrupala/guardian-mesh
(interfaces Apache 2.0, core AGPL-3.0).

## Adopting it

Start with PROGRAM.md §1 (the gate), §2 (the standard), and §3 (the
bar). Run the gate on one release, file the evidence pack, and let the
gap register (§9) tell you the truth about where you stand. Templates
for gate packs, release records, and spec inputs are on the roadmap.
