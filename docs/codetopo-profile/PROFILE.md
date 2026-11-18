# Codetopo Profile — Release Gate Program (nrupala/release-gate-program)

**What this is.** The agent-facing map of this repository, generated with
Codetopo 0.9.1 (local engine, `~/.cargo/bin/codetopo`) so an arriving agent
can see the machine — topology, trust boundaries, money surface — before it
submits or changes anything. Read this first; the graph snapshot beside it
(`snapshot.json`, `stats.json`) is the measured evidence.

- **Repo:** nrupala/release-gate-program
- **Commit profiled:** `4d43d46c0611664409ca18e6465418ced33d5748` (main)
- **Engine:** codetopo 0.9.1 · index run 2026-11-18
- **Graph:** 9 files walked · 0 failed · 77 nodes · 110 edges · audit chain valid (3 entries, head `f1e24081…ce27b`)
- **Nodes by kind:** external 38 · file 9 · module 9 · doc 7 · method 7 · variable 4 · class 1 · function 1 · package 1
- **Edges by kind:** calls 46 · contains 38 · reads 17 · imports 9

## Coverage honesty

Codetopo extracts Rust, TypeScript/JavaScript and Python, plus Markdown as Doc nodes. What is actually here (stated plainly, per the repo's own readiness rule): this is the gate program's **public face — documentation plus one Python script**. The 7 Markdown files (`README.md`, `PROGRAM.md`, `COMMERCIAL.md`, `TEST-PLAN.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`) are indexed as Doc nodes, and the single Python module `scripts/check_docs.py` (+ its test) is extracted at symbol level. That is the entire graph (13 symbols) — there is no gate-runner implementation in this repo to profile; the program's machinery lives elsewhere and must not be inferred from this pack.

## Topology

- `README.md` + `PROGRAM.md` — the program definition: the readiness rule (a capability counts only when a gate run produced filed evidence; everything else is PLANNED / NOT RUN / PROVISIONAL), and the standing truth that the program never certifies "zero threat" or "unhackable".
- `scripts/check_docs.py` — the repo's only code: a documentation checker (1 class, 7 methods in the graph), with `tests/test_check_docs.py` as its test.
- `COMMERCIAL.md`, `SECURITY.md`, `TEST-PLAN.md`, `CONTRIBUTING.md`, `CHANGELOG.md` — commercial terms, security posture, test plan and history as public documents; `.github/workflows/ci.yml` runs the checker/tests.

## Trust boundaries

- **No runtime, no credentials:** this repo executes nothing in production and holds no auth, secret, token or session handling — the only code is a docs checker that reads repository files.
- **The trust-relevant content is doctrinal:** the docs define what the wider gate program may claim (evidence-or-it-didn't-happen; no "zero threat" claims). Editing `PROGRAM.md` / `README.md` changes the public contract of the program — treat wording changes there as governance changes, not copy edits.
- **Blast radius:** reputational/doctrinal only — `scripts/check_docs.py` is self-contained (46 call edges, all internal).

## Money surface

**No money surface found in code.** Greps for `stripe|paddle|checkout|billing` over the Python source returned no hits; there is no payment, checkout or spend path. `COMMERCIAL.md` describes the program's commercial terms as a document — read it directly for terms; no transaction machinery exists in this repo at the profiled commit.

## How an agent should approach

1. Read `README.md`, then this profile, then the snapshot.
2. Use `codetopo` queries against the snapshot (descendants, blast-radius,
   symbol) before editing — especially around the hubs named above.
3. Do not add credentials, account identifiers or key material to any file
   here — names and paths only. Respect the trust boundaries above as
   design constraints, not suggestions.
4. Run the repo's own tests after any change; regenerate this profile
   (below) whenever the code changes.

## Regeneration

`docs/codetopo-profile/refresh.sh` (in this pack) re-downloads the repo
at a named ref, re-runs the index, and rewrites `snapshot.json`,
`stats.json` and the header block inputs of this profile. Regenerate at
every release / material change.

Release gate: NOT RUN — Guardian Mesh: NOT RUN (this profile pack is a
documentation artifact; it is not a release-gate or Guardian Mesh verdict).
