# Release Testing & Cybersecurity Program — Consolidated Statement

**Public edition.** This is the complete methodology of the Release
Gate program: what runs on every release, what proves each control,
how gaps are found and closed, and how applications are kept from
going rogue or being taken over. It is published so it can be
scrutinised and adopted. The operating practice that authored it
keeps its own verdict register and evidence packs private — they
describe live systems — and says so plainly, here and in its own
register, whose headline at first publication is **NOT READY**.

**The readiness rule.** A capability, control, or verdict counts only
when a gate run produced filed evidence for it. Everything else is
PLANNED, NOT RUN, or PROVISIONAL — named as such, never smoothed
over. There are no exceptions, including in this document.

**The standing truth.** There is no zero threat (see §6.4). This
program never certifies "zero threat" or "unhackable" — in a verdict,
a release record, or product copy.

## 1. The release gate — what runs on every release

Every release of every product passes the gate before it may call
itself tested. The gate is an independent function that builds
nothing; product teams build and fix, the gate issues verdicts and
evidence only. A verdict is one of: **PASS**, **PASS WITH FINDINGS**,
or **BLOCKED**. Anything the gate could not run is recorded **NOT
RUN**, with the gap named and owned — never silently skipped.

The gate's test families:

- Software testing (full suites, clean-environment runs, regression differentials)
- Network vulnerability
- User security
- Data protection
- Connection protection
- Encryption
- Zero-knowledge
- Zero trust
- User acceptance testing
- Proof of concept
- Security hardening
- Data leakage
- Data isolation
- User isolation
- Boundaries
- Key generation
- GPG/PGP
- Encryption key-management testing

### 1.1 Attacker-view testing (mandatory on every gate)

Scripted and API-level evidence never substitutes for attacking the
surface the way an outsider reaches it. Every gate run for a
networked product includes:

- **Full endpoint and exposure inventory** — every route, method, and public surface enumerated; anything served is in scope.
- **Registration and validation fuzz** — malformed and hostile inputs against every registration, validation, and form path.
- **Consent-screen proof** — what the user is asked to approve, in plain words, verified on the served page.
- **Token-exchange binding probes** — codes and tokens proven single-use, short-lived, and bound to client, redirect, and key.
- **Unauthenticated-surface inventory** — everything reachable with no credentials, probed as an attacker would.
- **Safeguard proof rule** — every claimed safeguard is proven by probe, or listed NOT RUN with the gap owned. An unprobed safeguard is an unproven safeguard.
- **Customer-journey rule** — the primary user journey is completed in a real browser. A behaviour fix evidenced only in stubs or unit tests is not evidence.

### 1.2 Evidence packs

Every gate run files a pack containing the probes, responses, scan
output, and the verdict. A verdict cites the pack; the pack cites the
probes; the probes cite the requests and responses. Any missing link
means the verdict does not issue. Public release logs carry each
batch's state honestly, including its gate verdict and its
release-candidate line.

## 2. The standard — controls and what proves each one

"Compliant" resolves to a fixed control list. A control is satisfied
only by its named probe or evidence artifact, filed in the product's
gate pack. A row with no artifact in the product's latest pack is
OPEN for that product, whatever any earlier run claimed.

**A. Web and API surfaces — OWASP ASVS 4.x (adopted frame).**
Authentication (credential storage, brute-force resistance,
recovery); session management (cookie flags, rotation); access
control (deny-by-default, per-endpoint authorisation, no IDOR —
proven by cross-account probes); validation and encoding (fuzz
results, injection-shape probes); cryptography in transit and at rest
(TLS reports, algorithm inventories); error handling and logging (no
stack traces or personal data to clients; security events logged);
data protection (minimisation, retention, export and deletion
executed as a test user); communications (HTTPS everywhere, HSTS, no
downgrade); malicious-code and file handling (upload probes); API
specifics (method and content-type discipline, per-endpoint rate
limits); configuration (no default credentials, no debug in
production, secrets out of code and history — scanned in both).

**A2. Mobile surfaces — OWASP MASVS.** Phone applications are gated
against the OWASP Mobile Application Security Verification Standard,
the mobile sibling of ASVS: Level L2 for apps that hold keys,
credentials, or sensitive user data, plus the Resilience
requirements (R) where tamper and reverse-engineering resistance is
claimed. A MASVS claim with no probe in the pack is OPEN.

**B. Auth servers — OAuth 2.1 with RFC 7591 / 6749 / 7636 / 8414.**
Dynamic client registration validation (hostile registrations
rejected with spec-correct errors); consent screens in plain words;
authorization-code binding (single-use, PKCE); token hygiene
(lifetimes, scope enforcement, revocation proven by probe); metadata
truth (the published metadata document diffed against actual
behaviour).

**C. Connectors — the MCP authorization specification.**
Protected-resource metadata served and accurate; 401 challenge
correctness; audience binding (a token for another resource is
rejected — no passthrough or confusion); the API-key lane (keys
hashed at rest, scoped, revocable, revocation probed).

**D. Operations — SOC 2-style controls, adopted as habits and
evidenced as controls.** Access (named accounts, least privilege,
rotation, no shared standing credentials); change (every production
change via reviewed pull request plus a recorded gate verdict);
logging and monitoring (watchdogs on critical surfaces — a silent
monitor is itself a finding); incident response (a written runbook,
walked quarterly); backups and recovery (backups taken, restore
drilled per product per quarter); vendor and report handling
(unsolicited security reports are treated as tips, verified against
our own systems, and answered only when genuine in identity and
substance).

**E. Design criteria — the defined-gateway law (adopted 2026-10-21).** The controls above test what a system does; these criteria govern how it is BUILT. The principle: software has defined pathways on which things move — if things are not as required on their given pathway, or are not on the right pathway, they cannot move further.

1. **Defined pathways; everything else is rejected by construction.** Every product declares its pathways — the routes by which data, commands, and authority legitimately move — each with its defined situation (who may move what, in what state, under what conditions). Movement off a declared pathway is stopped by the structure, not filtered after the fact. The declaration is a filed artefact (the pathway inventory, in the product's gate contract family); a gate run diffs the implementation against it and probes off-pathway movement directly. An undeclared flow found in the implementation is a finding; a declared flow with no enforcement point is a finding.
2. **Structure is not sanitization.** A pathway system stops off-path movement, but malicious content can still ride a VALID pathway. So every gateway validates what rides: strict type-level schemas enforced at the gateway before payloads reach internal handlers, payload validation, memory safety in the handlers, and cryptographic boundary checks. The pathway decides WHERE things may move; validation decides WHAT may ride.
3. **Dual-zone separation.** A product that holds keys or processes sensitive data separates a PROCESSING zone (business logic over tokens, anonymized, or attested data) from a CRYPTOGRAPHIC zone — an isolated process or thread holding private-key operations, decryption, and raw sensitive data, from which nothing raw crosses back. Inside the zone: local stores encrypted with Argon2id-derived keys, hardware-backed where the platform offers; session keys ephemeral; decryption in buffers zeroed after use, with the zeroing proven in the built artefact.
4. **Isolation is mandatory at the sensitive points; the mechanism is the strongest the platform supports.** Wherever a system signs or issues, handles user credentials, or holds critical data, that function lives in an isolated bubble. The tier order is strict: (a) HARDWARE-BACKED — secure enclave, TEE, hardware-backed keystore, protected VMs, protected confirmation — wherever the platform provides it; and where the platform is a design choice, choose one that provides it, because a system not built ready for hardware isolation cannot be given it later. (b) Where hardware isolation does not exist, a SOFTWARE-DEFINED AIR GAP: the bubble is a separate process or VM with no direct connectivity in either direction — nothing reaches it directly and it initiates nothing; all exchange crosses the defined gateway as validated artefacts (one-directional where the flow allows), no shared memory, no direct calls. (c) Plain in-process separation only as a named, accepted exception, recorded as the weakest tier wherever it stands. Honest limit, binding on all claims: a software-defined gap on a shared host is weaker than hardware isolation — it defeats application-layer and network attackers, not a compromised kernel or host — so a product claims the tier it actually implements, and the gate's zone-boundary probes grade the tier, not the intention.
5. **Protected movement and safe construction.** Traffic between a product's own components and over its first-party sync/telemetry pipelines uses mutual TLS with strict certificate or public-key pinning where the product controls the channel; low-level and isolated modules are written in memory-safe languages.

## 3. The release bar and the release-candidate rule

A product earns the word "release" only with all five criteria, each
proven by named evidence:

| Criterion | Meaning | Proven by |
|---|---|---|
| CONTROL | We control exactly what ships | Tagged reproducible build; deployed artifact hash equals the gated artifact; full endpoint inventory; any drift fails the bar |
| UNDERSTANDING | We understand what it does | Evidence pack complete against the standard; findings and accepted risks named by a person; the plain-words customer test passes |
| MANAGEMENT | Its operation is managed, not hoped | Monitoring and watchdogs live with a named owner; logs captured and read; cost and quota guardrails where consumed |
| LIFECYCLE | Its whole life is handled | Deploy path proven; rollback drilled (performed, not described); upgrade from the previous version tested; retire path defined before deploy |
| STABILITY | Its behaviour holds under load and time | Worst-case performance proven with margin; full suite green in a clean environment; no unresolved high or critical findings; the soak below |

**The release-candidate rule.** Any batch that passes all gates is a
RELEASE CANDIDATE for one week of deployed soak under active watch
before it may be called a release. Candidates deploy live
immediately — security fixes never wait for ceremony. A disqualifying
gap found during the soak returns the batch through the fix loop and
starts a fresh candidate week; an additive batch with no new attack
surface joins the running window; a new feature with a new public
surface takes its own focused candidate row. A register holds every
batch's verdict, deploy date, window, and graduation outcome.

## 4. Money-surface rules

Batches that touch money carry rules of their own, written after a
fleet-wide billing sweep caught — among lesser findings — a
production licence issuer that trusted a test-mode webhook secret,
and three products whose payment paths were armed but never
provisioned. The sweep's rules are standing:

- **Secret-name inventory on every money gate.** The gate reads the production configuration's secret NAMES (never values) and diffs them against the secrets the code requires. A batch whose code needs a secret production does not hold is blocked, however good its tests are.
- **Genuine-permission proof.** A provisioned key is proven by behaviour against real provider objects (a real unpaid session must return its payment-incomplete answer; a real customer must mint a real portal session) — presence is not proof.
- **Test/live namespace separation.** Test-mode events must never be able to grant, mint, or extend anything in the live namespace. Verification fallbacks across that line are Critical by definition.
- **Error acknowledgement discipline.** A webhook handler that fails after signature verification must return an error so the provider retries; silent success responses on failure are findings.
- **Buy-entry smoke first.** The purchase entry point is proven reachable before the deeper battery runs; a dead front door makes the rest moot.
- **Proof standard.** One full real-money cycle (buy, entitle, cancel, revoke, refund) proves the shared payment pattern once per provider account; each further product proves the pattern's legs by read-backs and behaviour short of a new purchase, unless a specific leg cannot be evidenced any other way.

## 5. Threat basis — MITRE ATT&CK

The program's threat model is not improvised. The threat basis is
**MITRE ATT&CK**, the compiled, openly available knowledge base of
adversary tactics and techniques maintained by MITRE and built from
real-world observations — 14 tactics and more than 270 techniques
across its Enterprise, Mobile, and ICS matrices, published in
machine-readable form (STIX data) for use in tooling, measurement,
and training, free for use under MITRE's terms with attribution.

- **Threat measurement.** Coverage is measured by mapping gate checks, detection rules, and protection-layer evaluation rules to ATT&CK technique IDs. A technique with no mapped check or control is a visible empty cell — a gap with a name — not an unknown.
- **Prevention design.** Countermeasures are chosen against techniques, using MITRE's companion knowledge bases: CAPEC (attack patterns), CWE (weakness types — mapped into coding and review standards), and D3FEND (the defensive-countermeasure knowledge graph).
- **System training.** The STIX form of ATT&CK is the dataset the tooling consumes — coverage reports, protection-rule design, and bench emulation sets are built from technique definitions, so the defence targets the documented behaviour of real attackers rather than a vendor's summary.

**Per-product threat models (adopted 2026-10-21).** A shared threat basis is not a product's threat model. Each product also carries its OWN threat model, produced from its actual code by a repo-grounded method (OpenAI's security-threat-model skill, Apache-2.0): the system model extracted from the repository with every architectural claim anchored to evidence, trust boundaries enumerated as concrete edges (protocol, auth, encryption, validation), the assets that drive risk, entry points, realistic attacker capabilities AND explicit non-capabilities, threats enumerated as abuse paths tied to assets and boundaries, and mitigations distinguished as existing (with evidence) from recommended. The model is a design-stage artefact and a gate input: a gate run checks the product against its own model's abuse paths, and a product with no current model carries that as a named gap.
- **Live indicator feeds.** ATT&CK describes how attackers behave; indicator feeds supply what is malicious right now — addresses, domains, file hashes, malware URLs. Open sources are adopted as outward connectors (never as product fabric): LevelBlue OTX, MISP, the abuse.ch suite (URLhaus, ThreatFox, MalwareBazaar), GreyNoise, VirusTotal, and the NIST National Vulnerability Database / CVE for vulnerability identity and severity. Paid enterprise intelligence platforms are reference reading only, under a free-first rule. Ingestion design rules: indicators are validated in context against known-good traffic before any automated block, and every indicator carries a time-to-live and is retired when stale. A feed that is wired but inactive is reported as exactly that.

## 6. Ethical-hacking practice — attacking ourselves first

Prevention is validated by offence, run by us against our own systems
before anyone else does. Rules: authorised surfaces and test data
only; destructive proofs of concept on staging or isolated clones,
never production; benches never hold production secrets; test keys
are revoked at run close; every run is recorded (image hash, tool
versions, commands, output) — an unrecorded run is a NOT RUN.

- **Per-release offensive basics (Kali bench).** Network service and version inventory; web exposure scanning; connection-protection reports (protocol versions, cipher strength, certificate chain and expiry, HSTS and header posture); authentication attacks against our own test accounts to prove rate limiting, lockout, and alerting actually fire; offline password-strength proofs against our own generated test hashes — never against customer hashes.
- **Verification benches (Arch).** A crypto bench (key-generation entropy and source checks, GPG/PGP verification, an independent sealed-proof verifier, hash-chain re-verification — a tampered proof must come back NOT VALID); an isolation bench (cross-tenant probe harness, boundary and fault injection, data-residency diffs); an evidence bench (independent re-verification of gate packs themselves).
- **Technique emulation.** Attack simulations are built from ATT&CK techniques, so each emulation answers a measurable question: does this documented technique succeed against us, and does our detection see it?
- **Periodic full adversarial pass.** Quarterly, pentest-class, against the highest-exposure product on a staging clone, and once against any newly exposed surface before its first release gate closes.
- **Platform rule.** Benches and demo systems are Linux virtual machines, never containers: the offensive bench is a full KVM virtual machine; verification benches are microVMs cloned from pinned golden images, one clean instance per run, destroyed at run close.

### 6.1 Named tooling and the assessment-to-report structure

The five movements of every release — assess what the app requires,
put the protocol in place, run the tests, build the rectification
plan from the results, and report it all in the release record — are
the pipeline's shape. The named engines that standardise each stage:

- **Policy-as-code** — Open Policy Agent / Conftest checks of routing graphs and payload schemas against the defined pathways before runtime: the mechanical form of the defined-flow (Zero Gap) rule.
- **Static analysis** — Semgrep with custom rules for the project's own invariants (including explicit buffer-zeroing rules) and CodeQL taint tracking from ingress to sink.
- **Composition analysis** — Trivy and OSV-Scanner on every build, against the open vulnerability databases of §5.
- **Mobile dynamic testing** — MobSF plus Frida instrumentation under the OWASP Mobile Security Testing Guide: debugger and hook detection, memory-dump resistance — the proof machinery behind the MASVS bar of §2.
- **Store-compliance assessment** — manifest, permissions, and declarations checked against store policy (Google Play Data Safety, Apple privacy labels, App Tracking Transparency) as a named assessment class in gate scope.
- **Gap-to-fix machinery** — failures triage by severity into tracked issues carrying the failing case; a fix closes only when the gate re-runs that case green.
- **Build identity** — ephemeral, scoped build tokens via OIDC workload identity federation in place of long-lived static keys.
- **Code-audit engine (adopted 2026-10-21)** — Cloudflare's security-audit skill (MIT): a six-phase codebase audit — reconnaissance producing a machine-readable coverage ledger, coverage-led hunting by isolated agents, candidate validation by a fresh verifier assigned to DISPROVE each candidate, schema-validated findings, independent record verification, neutral reporting. It is the code-side engine beside Semgrep/CodeQL: it audits source inside a sandbox and refuses live probing by design, so it complements — never replaces — the gate's deployed-surface proof. Its AI/LLM and data-lifecycle hunting classes are adopted as code-side companions to §6.2/§6.5, and its coverage-ledger mechanic is the adopted form of the coverage map's v2 (§6.5's traceability rule, made mechanical).

**Findings discipline (adopted 2026-10-21, from the same source).** A candidate vulnerability carries exactly one of three verdicts — CONFIRMED (complete source trace plus a bounded observed result), NEEDS_VALIDATION (an exact unresolved fact named; NO severity may be attached), REJECTED (disproved, and kept on record). Severity is earned by surviving an assigned disproof attempt, never assigned at discovery. This grades candidates inside a run; release verdicts (PASS / PASS WITH FINDINGS / BLOCKED) are unchanged.

One deliberate difference from common blueprints: there is no
percentage compliance score and no automatic signing at a threshold.
The release bar is evidence — no unresolved high or critical
findings, then a clean watched week. A score can be gamed; a soak
cannot.

### 6.2 Testing zero-trust, zero-knowledge, and agent systems

When a system is built so that nothing outside it can see inside —
end-to-end encrypted, zero-knowledge, components treating each other
as untrusted, including agents — inspection-based testing fails by
design. The method is: test the proofs, the boundaries, and the state
transitions.

- **Fail-closed decryption fuzzing.** Malformed and plaintext payloads are injected into storage layers; the system must fault cryptographically, never fail open. A standing gate check for zero-knowledge products, alongside tamper batteries on signed artefacts.
- **Key-lifecycle proofs.** Ephemeral keys are proven destroyed at session end, and compromise of a current key is proven to expose neither past nor future sessions (forward secrecy), by test.
- **Attestation challenges.** Where a product claims hardware-enclave backing (Secure Enclave, TEE, pKVM), the claim is challenged: the client must prove a genuine, untampered enclave before any synchronisation, and the gate tests rejection of a failed attestation.
- **Side-channel and timing checks.** Cryptographic operations are timed for information leakage about keys or data structure — honestly the hardest family to run well, and NOT RUN until a bench exists to run it.
- **The agent trust battery.** For agent and microservice surfaces: a rogue proxy is inserted between components (intercepted traffic must be unreadable ciphertext; an injected payload must break the state machine, not bend it); capability-escalation probes verify a compromised agent cannot exceed its scoped tokens; mutual TLS and pinning are fuzzed (expired, mispinned, and imposter peers dropped).
- **Conditional tooling.** Zero-knowledge circuit testing (SnarkJS / Circom-class) applies only to a product that actually implements proof circuits; claims of the no-plaintext-visibility kind are proven by code path and the checks above.

### 6.3 Formal methods and the frontier layers

Testing samples behaviour; proof settles it. For the smallest,
highest-assurance cores, the program names a tier above testing —
with its limits stated first: **a proof proves conformance to a
specification. It does not catch a wrong specification or a
mis-provisioned deployment** — and the costliest escapes in practice
(armed-but-unprovisioned batches, a test secret trusted in
production) are exactly those. Formal methods are therefore a tier
for small critical cores, never a substitute for the gate's probes.

- **Non-interference proofs (Lean-class theorem proving).** The rigorous answer to the data-harvester problem: define Secret and Public domains formally and prove that changes in the Secret domain have zero mathematical effect on the Public output stream. A rogue dependency or backdoored SDK that bundles telemetry into network output then fails verification itself. Target components, chosen because they are small and fully specified: the cryptographic vault core, and the protection layer's evaluator.
- **Correct-by-construction pathways.** Defined-flow routing rules modelled as state machines and proven — unauthorised transitions mathematically impossible rather than runtime-checked.
- **Protocol verification.** Tamarin / ProVerif models of mutual-TLS, key-exchange, and handshake designs, proven against man-in-the-middle, replay, and reflection under a stated adversary model.
- **Symbolic execution.** KLEE / SMT-solver-class exhaustive path exploration for small critical modules.
- **Frontier layers, named with their scope.** Hardware fault injection (voltage, clock, electromagnetic glitching) is a physical-access tier, answered on device products by secure-element hardware choice. Multi-agent collusion — agents subverting intent using individually valid messages — extends the agent trust battery as a research-grade input. Epistemic logic (proving what a node knows, and that it stayed blind to context) is recorded with no tooling path claimed.

### 6.4 The standing truth, and the blind spots

**There is no zero threat.** Any system that executes instructions,
touches hardware, or interacts with the outside world presents an
attack surface; a claim of immunity is itself a security failure,
because it manufactures false confidence. This program never
certifies "zero threat", "unhackable", or any synonym — in gate
verdicts, in release records, or in product copy. The engineering
goal is the honest one: raise the cost, complexity, and effort of
compromise until attack is mathematically, cryptographically, or
economically infeasible — and say exactly how far that has been
proven, and no further. Even a formally verified, zero-gap,
encrypted system faces these blind spots; each carries a posture:

- **The human and operational layer.** Proofs do not stop a compromised developer key signing malicious code legally, a user phished into authorising a rogue device, or an insider altering a pipeline before verification. Posture: vaulted credentials, least privilege, change only via reviewed pull requests. Named controls to adopt: multi-party (M-of-N threshold) authorisation for releases and key operations, and FIDO2 hardware keys for administrative actions.
- **The toolchain itself.** A compromised compiler can inject malicious code into mathematically clean source (the Thompson "trusting trust" problem). Mitigation tier: reproducible builds with hash equality, hermetic builds on isolated builders without external network access, hash-locked dependencies, and toolchain provenance under the SLSA target of §7.4 (Level 4 named for the highest-risk modules, licence issuers first).
- **The host platform.** A zero-day in the host operating system kernel, or a microarchitectural leak of the Spectre class, can read application memory across isolation boundaries — inherited risk no app code can patch. Posture: sensitive operations isolated in hardware-backed environments where offered, minimal plaintext lifetime in memory, the risk named as inherited rather than solved.
- **Metadata and traffic analysis.** Encrypted payloads still leak through timing, frequency, and packet size. Posture: constant-time cryptography and timing checks; traffic padding and dummy-traffic obfuscation for sync and telemetry surfaces as a named design direction.
- **Economic and resource attacks.** An attacker may never touch the code: manipulate an agent's inputs or incentives so it acts against intent while obeying its rules, or force expensive verification work until wallets, CPU, or battery are exhausted. Posture: rate bounds and resource quotas at every gateway — behaviour-proven wherever per-endpoint rate limits are gated.

The direction of travel for the whole program, stated once: from
patching individual vulnerabilities after discovery toward making
entire classes of them structurally impossible. The claim is earned
class by class, each with its proof; it is never a blanket property
of a product — and the closing flourish of any roadmap ("the
complete toolkit", "the highest standard") is precisely the kind of
sentence this program does not write about itself.

### 6.5 Agentic systems — the families this program adds itself

Agents are a new surface class: software that reads untrusted
content, decides, and acts with real authority. The families above
cover their transport and cryptography; these cover what is specific
to an agent.

- **Instruction-injection battery.** Content an agent processes — web pages, files, tool outputs, other agents' messages — is untrusted data, never instruction. The gate fires direct and indirect injection suites and proves: the instruction hierarchy holds (system over user over content), injected instructions are treated as data, and no injected content can make the agent disclose its context, its instructions, or anything outside the task's scope. An agent that follows an instruction found in the wild fails the gate.
- **Tool authority and blast radius.** Every tool an agent can call is inventoried with its authority: what it can change, whether the change is reversible, and what approval it requires. Irreversible and outward-facing actions (sending, paying, deleting, publishing) require the human approval the action's weight demands; the approval surface is itself tested — it must show the actual action, amount, and recipient in plain words at decision time, because an approval that is always granted is not a control. Tool calls are idempotent where the tool allows it, and a pre-execution simulation or dry run is required where one exists.
- **Halt semantics.** A stop, pause, or audit request must actually stop the agent — proven by interrupting a live run mid-task and verifying no downstream effects land after the halt. An agent that finishes "one last thing" after being stopped fails.
- **Runaway and self-exhaustion bounds.** Iteration caps, delegation-depth caps, and budget caps (tokens, time, money) are configured — and then proven by test runs that deliberately loop, recurse, and overspend: the cap must trip, visibly, with the run's state preserved for inspection.
- **Memory and context integrity.** An agent with persistent memory can be poisoned: false facts or instructions planted in stored memory steer every later session. The gate tests memory writes (only authorised sources can write; writes are attributable), memory provenance (a recalled "fact" carries where it came from), and poisoning recovery. Context contamination between tasks and between users is probed the same way as tenant isolation — because it is tenant isolation.
- **Delegation and confused-deputy probes.** When an agent acts for a person, its authority is scoped, expiring, and non-transferable, and it can never widen its own authority. Probes attempt the classic deputy's trick: getting the agent to use its legitimate access for a third party's benefit, or to accept a delegation from someone who never held the authority being delegated.
- **Confinement and egress.** An agent that browses or executes code runs confined: filesystem scope, network egress allowlist, and credential access limited to the task — proven by escape probes, not by reading the configuration.
- **Model-as-dependency.** The model is a dependency with a behaviour surface. A model version change is a release: the adversarial conversation suite re-runs against the new version before it serves. Evaluation is statistical — behaviour varies run to run, so agent gates set pass thresholds over repeated runs rather than single demonstrations. Provider failure modes are tested: model unreachable, malformed output, and provider compromise are all fail-closed events.
- **Trace completeness.** Every consequential agent action must be attributable in a sealed trace to the instruction that authorised it, the tool call that executed it, and the approval that permitted it. An action with no trace is a finding by definition.
- **Requirement traceability (all families).** Completeness is mechanical, not asserted: every family in §1, every control row in §2, and every adopted item in §§5–6 resolves to exactly one of — a named gate check with a proof form, a bench that runs it, or a named gap in §9 with a closer. A requirement that resolves to none of the three is itself a gap and enters the register until it does. This rule is what "no gaps" means in this program: not that nothing is missing, but that nothing missing is unnamed.

## 7. Prevention — keeping applications from going rogue, and keeping attackers out

### 7.1 Design patterns proven at the gate

Each pattern below is a standing expectation for new surfaces, and
each entered the program by being behaviour-proven on a live product
during a gate run:

- **Fail-closed issuance.** Licence and entitlement issuers mint nothing unless every binding checks out: live mode, paid state, the exact product, the exact price, the exact amount and currency — and an unconfigured binding mints nothing at all.
- **Revoke-only money rails.** Where a webhook only needs to react to failure, it is built so it can pause, clear, or stop — never issue, extend, or revive.
- **Replay-safe writes.** Entitlement state changes are written so a replayed or duplicated provider event converges to the same state instead of double-granting.
- **Single-use, hashed recovery.** Access-recovery tokens are random, stored only as hashes, short-lived, and burned on use; replies are identical for known and unknown accounts so the path cannot enumerate users.
- **Signed artefacts with public revocation.** Licences and certificates are cryptographically signed; revocation is published on a blocklist the client checks; a tampered artefact verifies NOT VALID.
- **Defined-flow invocation (the anti-rogue rule).** A protected action can only happen in its specified shape: an invocation that cannot be formed as the specified handshake cannot happen at all — prevention by construction, not by a check that can be bypassed. This is the protection layer's core doctrine (§8).

### 7.2 Authorisation and anti-hacking as product features

Protection is a feature to ship, not only a process to run: signed
artefact certification, offline-verifiable licences, and entitlement
binding to payment facts are product capabilities, gated like any
other. The systematising layer is a defined-flow evaluator on the
product's exposed surface (§8): every protected request is evaluated,
allowed or blocked, and the decision is sealed in a tamper-evident
proof that travels with the product's release record. No product may
claim the protection layer's coverage until the capability behind
the claim is behaviour-proven at the gate.

### 7.3 Ransomware and takeover posture

What stands in a conforming practice: least-privilege, scoped
credentials per product (restricted provider keys with named
permissions); secrets in a vault, inventories read by name only; no
shared standing credentials; backups taken on schedule for source
and product state, with restore part of the release bar's lifecycle
criterion; production changes only through reviewed pull requests
with gate verdicts; integrity declarations and watchers on
production surfaces so undeclared changes alarm immediately.

And the part that must be said in the same breath: an incident-
response capability exists only when a written runbook exists and
has been walked. Backups and good design are not a response. A
practice that cannot point to a walked runbook says so — in its gap
register, in those words.

### 7.4 Adopted targets — design input, not yet evidence

- **Build and supply-chain integrity.** Target: SLSA Level 3 for customer products (hermetic builds on isolated builders, non-falsifiable provenance signed with Sigstore/cosign), reproducible byte-for-byte builds, and dependencies pinned to cryptographic hashes rather than version ranges. The proven subset in any conforming practice starts narrower: deployed-artifact hash equality with the gated artefact, and per-product dependency audits. The walk to the target is an assessed path, not an aspiration: OpenSSF Scorecard, Best Practices badge progression (Passing, Silver, Gold), and SLSA levels assessed checkpoint by checkpoint, each checkpoint carrying its remediation — and a format pass never counts as an awarded badge; claims require the evidence behind them.
- **Zeroization that survives the compiler.** A buffer-zeroing rule is a control only if the zeroing exists in the shipped artefact: compilers eliminate stores they can prove unread (dead-store elimination), so source-level zeroing can be silently optimized away. The check must prove zeroization in the built artefact, not in the source's intent.
- **Runtime hygiene specifics.** Decryption buffers are ephemeral and zeroed immediately after use; sync and telemetry channels use mutual TLS with certificate pinning; low-level or isolated modules are written in memory-safe languages (Rust, Swift) where the platform allows. Strict schema validation at every gateway is a standing expectation.
- **Regulated-data safeguards.** Where a product handles regulated data (for example protected health information under HIPAA §164.312), that regime's technical safeguards become a gate section for that product, with a dual-isolation pattern — processing zone separated from the cryptographic vault zone — as the required architecture.

## 8. Guardian Mesh — the protection layer the gate specifies

Guardian Mesh is the reference implementation of the defined-flow
protection layer: an evaluator that sits on a product's exposed
surface. A request that cannot present the specified handshake shape
is not denied by a check — it cannot be formed at all. Evaluations
resolve to ALLOW or BLOCK and are sealed in tamper-evident proofs;
certificates carry a full lifecycle (issue, renew, revoke, expire).

- **Specs come from the gate.** Every gate run emits protection-layer spec inputs alongside its verdict: every escape or near-miss, every NOT RUN, every new attack or failure class, and every family where evidence was thin. Each input names the risk, the new gate check that now catches the class, and what the layer must be able to prove for that check (evaluation input, verdict rule, sealed-proof fields, tamper behaviour, certificate-lifecycle impact).
- **Proof before credit.** A capability becomes a gate requirement only after it is behaviour-proven at the gate (valid proof verifies VALID; tampered proof verifies NOT VALID; no answer means BLOCK). Until then it is a spec input, and no gate pack may credit it as a control.
- **Certification boundary.** Certification warrants the tested artefact — the virtual machine, its spec, and its build instructions — never a customer's own deployment choices.
- **Compliance-as-proof.** Because an auditor cannot be shown the inside of a zero-knowledge system, the sealed proofs double as the audit artefact: a proof of correct execution an outsider can verify without seeing any underlying data. This is the audit model for every zero-visibility product.

Repository: https://github.com/nrupala/guardian-mesh (interfaces and
specifications Apache 2.0; daemon core AGPL-3.0-or-later).

## 9. The gap register — what is not done, and what closes it

The register is kept unsparing on purpose: a gap closes only with
filed evidence. The canonical gap classes every adopter should
expect to carry, each with its closer:

1. **Track record is young.** A new gate is a discipline, not a track record. Closer: time plus executed runs; no shortcut exists.
2. **Provisional early verdicts.** Verdicts issued under a weaker checklist stand as PROVISIONAL until re-gated under the widened standard.
3. **Dependency auditing coverage.** Audits must run per product through a lane with working tooling egress, filed in packs — partial cover is named partial.
4. **Benches specified, not built.** Every bench-dependent check is NOT RUN until a bench proves it. Closer: the bench plan, in order (offensive, crypto, isolation, evidence).
5. **Protection-layer capabilities are spec inputs, not proofs.** Closer: the first behaviour-proof on a live surface.
6. **Findings carried across teams.** Open findings close only when their re-proof lands at the gate.
7. **Clean-environment evidence degraded.** When CI capacity is exhausted or unavailable, local clean runs substitute and packs say so, in those words.
8. **Incident response does not exist as a capability** until the runbook is written and walked (§7.3). For most young programs this is the most serious gap, and it should outrank new feature work.
9. **No full adversarial pass has ever run** until the first scheduled pass lands (§6). Newly exposed surfaces ship without one until then — named, not hidden.
10. **Verifier independence is structural, not organisational.** The verifying lane is never the building lane, and verdicts cite evidence chains — but true external review (a second reviewer, human or firm) is a purchase decision, named as such.
11. **Threat-coverage mapping not yet run.** Adopting ATT&CK as the basis (§5) and mapping coverage against it are two different events; the second is a work item with an empty-cell register as its output.

## 10. Cadence and governance

- **Per-release gate** — every release, before merge and deploy, verdict recorded in the release record.
- **Development frame** — the delivery pipeline's practices map to NIST SSDF (SP 800-218), so the build side of the program cites the same standard an outside reviewer would.
- **Weekly fleet sweep** — a scheduled sweep re-checks already-released software and verifies every shipped release carries a recorded verdict; a missing verdict is reported as a process defect. The sweep is a backstop, never a substitute for the per-release gate.
- **Site-integrity watch** — production surfaces are baselined; changes outside a declared work window alarm immediately, and declared-but-uncertified changes are carried until a certification resolves them.
- **Periodic adversarial pass** — quarterly (§6), plus once against any newly exposed surface before its first gate closes.
- **Quarterly operations evidence** — restore-drill record per product, incident-response tabletop record, access-inventory review, filed with the program records.
- **Independence** — the verifying lane is never the building lane for the same release; a fix's verification re-probes the live surface from the gate, and the fixing team's own "verified" is a claim, not evidence.
- **Report handling** — unsolicited security reports are tips: verified against our own systems, fixed and published when real, answered only when genuine in identity and substance.

## 11. Evidence and records — what a conforming practice keeps

- The program files: this statement, the standard, the gap register, the release bar, the cadence, the bench plan, the candidate register, and the coverage mappings.
- The gate playbook: checklists, the deep-scan playbook, the protection-layer and bench backbone, and case files for every genuine external report and every instructive escape.
- Gate packs: one per run — verdicts and probe evidence, retained.
- The delivery pipeline: the fixed pathway every product build travels, its mechanical gates, and its escape ledger — every escape becomes a corpus case and a mechanical check before its fix ships.
- The threat basis: MITRE ATT&CK (attack.mitre.org; STIX data in the mitre-attack/attack-stix-data repository), with CAPEC, CWE, and D3FEND as companion bases, and the open indicator sources of §5.

*End of the public edition. The methodology is the contribution;
the evidence standard is the price of believing it.*
