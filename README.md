# king-wen-legal

Constitutional legal knowledge graph + King Wen training bridge.
Artifacts first. No fabrication. Drop-down links below.

---

## Repository layout

<details>
<summary><strong>target/legal-data/</strong></summary>

```
target/legal-data/
├── constitutional-structural-truth-graph.json
├── constitution-complete-word-inventory.json
├── timelined-dictionary-diff.json
├── skill-clusters/
│   ├── manifest.json
│   └── constitutional-legal-knowledge-cluster.json
├── diff-graph-topology.json
├── constitutional-readouts/
│   ├── originalist-meaning.json
│   ├── modern-legal-meaning.json
│   └── diff-readout.json
├── inject-bindings/
│   └── constitution-inject-bindings.json
└── project-structure.json
```

| File | Purpose |
|---|---|
| `constitutional-structural-truth-graph.json` | 14-classified-term truth graph with drift + blast radius |
| `constitution-complete-word-inventory.json` | Full word inventory with Webster 1789/1913 provenance |
| `timelined-dictionary-diff.json` | Dictionary diff with variable influence for drift analysis |
| `skill-clusters/manifest.json` | 8 semantic-domain skill cluster manifest |
| `diff-graph-topology.json` | Left/right diff visualization: originalist vs modern meanings |
| `constitutional-readouts/originalist-meaning.json` | Originalist meaning + 1789/1913 definitions per term |
| `constitutional-readouts/modern-legal-meaning.json` | Modern statutory/administrative usage with drift annotations |
| `constitutional-readouts/diff-readout.json` | RED/ORANGE drift summary across classified terms |
| `inject-bindings/constitution-inject-bindings.json` | Parser + term identity kits with `fabrication_policy: PROHIBITED` |
| `project-structure.json` | Completion manifest + canonical paths + cron job IDs |
| `source-registry.json` | Source registry for Gutenberg/Webster provenance |
| `sovereign-constitutional-crosswalk.md` | Sovereign-to-constitutional crosswalk notes |
| `tmp_scripts/` | Builder/probe/rebuild/patch scripts for artifacts |
| `webster-1913-sections/` | Cached 1913 Webster HTML sections: pg661–pg668 |

</details>

<details>
<summary><strong>src/openjarvas/</strong></summary>

OpenJarvas-side workspace tree.
Use for bridge code, docs/audit artifacts, and future OpenJarvas bindings.

</details>

---

## Quick start

```bash
git clone git@github.com:Kbro1989/king-wen-legal.git
cd king-wen-legal
```

---

## Skill cluster

This repo is the canonical artifact home for the `constitutional-legal-knowledge` Hermes skill cluster.

**Core skills**

| # | Skill | Role |
|---|---|---|
| 1 | `rules` | Parasitic enforcement: zero placeholders, no fabrication, no destructive mock |
| 2 | `research/legal-data` | Canonical artifact owner + `/learn` hooks |
| 3 | `research/constitutional-structural-truth-graph` | 14 classified terms + drift + blast radius |
| 4 | `research/constitutional-dictionary-clustering` | MISSING_FOR_CLUSTER semantics + parser bindings |
| 5 | `verification/local-artifact-audit` | Exact-path/line-number audit |
| 6 | `verification/canonical-table-audit` | Roundtrip integrity + source-truth audit |
| 7 | `research/governance-topology` | Graph construction + rendering |
| 8 | `research/verifiable-research` | Source-verified expansion + evidence maps |
| 9 | `research/kingwen-jarvis-megatron-learn` | King Wen/Jarvis training gate |
| 10 | `research/kingwen-truth-reconciliation` | Immutable-table reconciliation |
| 11 | `research/antigravity-forensics` | Brain/conversation scratch forensics |

**Dictionary edition skills**

| Skill | Source coverage |
|---|---|
| `1789-webster-dissertation` | 1789 Webster dissertation-only source (non-lexical) |
| `1913-webster-a-b` | 1913 Webster A–B |
| `1913-webster-c` | 1913 Webster C |
| `1913-webster-de` | 1913 Webster D–E |
| `1913-webster-fgh` | 1913 Webster F–G–H |
| `1913-webster-mno` | 1913 Webster M–N–O |
| `1913-webster-pq` | 1913 Webster P–Q |
| `1913-webster-r` | 1913 Webster R |
| `1913-webster-s` | 1913 Webster S |
| `1913-webster-tuvw` | 1913 Webster T–U–V–W |
| `1913-webster-xyz` | 1913 Webster X–Y–Z |

---

## Usage

### Hermes `/learn` sequence

Run these in Hermes CLI/desktop/dashboard:

```
/learn research/legal-data
/learn research/constitutional-structural-truth-graph
/learn research/constitutional-dictionary-clustering
/learn verification/local-artifact-audit
/learn verification/canonical-table-audit
/learn research/governance-topology
/learn research/verifiable-research
/learn research/kingwen-jarvis-megatron-learn
/learn research/kingwen-truth-reconciliation
/learn research/antigravity-forensics
/learn rules
/learn research/legal-data/dictionary-editions/1789-webster-dissertation
/learn research/legal-data/dictionary-editions/1913-webster-a-b
/learn research/legal-data/dictionary-editions/1913-webster-c
/learn research/legal-data/dictionary-editions/1913-webster-de
/learn research/legal-data/dictionary-editions/1913-webster-fgh
/learn research/legal-data/dictionary-editions/1913-webster-mno
/learn research/legal-data/dictionary-editions/1913-webster-pq
/learn research/legal-data/dictionary-editions/1913-webster-r
/learn research/legal-data/dictionary-editions/1913-webster-s
/learn research/legal-data/dictionary-editions/1913-webster-tuvw
/learn research/legal-data/dictionary-editions/1913-webster-xyz
```

### Enforcement cron jobs

| Job | Schedule | Purpose |
|---|---|---|
| `rules-skill-check` | every 15m | Scans all `SKILL.md` for placeholders/stubs/mock/fake/invalid/minimal content |
| `rules-session-check` | every 30m | Injects rules check into active Hermes sessions + suggests `/learn` cluster attachment |

---

## Artifact details

<details>
<summary><strong>constitutional-structural-truth-graph.json</strong></summary>

- **14 classified terms** with drift classification: `GREEN`, `ORANGE`, `RED`, `UNVERIFIED`
- Blast-radius mapping: primary/secondary/subdomains
- Source: Gutenberg Constitution cache + Webster 1789/1913
- Envelope: `status: complete`, `fabrication_policy: PROHIBITED`

</details>

<details>
<summary><strong>diff-graph-topology.json</strong></summary>

- Left nodes: originalist meanings
- Right nodes: modern legal meanings
- Center: Constitution text with character-offset inject/parse sites
- 28 nodes / 14 edges / 14 inject sites / 14 parse sites
- Circuit-split metadata included where modern meaning diverges across jurisdictions

</details>

<details>
<summary><strong>inject-bindings/constitution-inject-bindings.json</strong></summary>

- 14 term identity kits
- 14 parser bindings
- Stable identifier: `constitution-inject-bindings-v1`
- Future integration: King Wen allowed, status `planned_but_not_prepped`
- `fabrication_policy: PROHIBITED`

</details>

<details>
<summary><strong>skill-clusters/manifest.json</strong></summary>

- 8 semantic domains
- 7 required keys per cluster
- Drift classification per cluster
- Coverage gaps + MISSING_FOR_CLUSTER semantics

</details>

<details>
<summary><strong>constitutional-readouts/</strong></summary>

- `originalist-meaning.json`: 1789/1913 definitions + original-intent inference
- `modern-legal-meaning.json`: modern statutory/administrative usage + drift annotations
- `diff-readout.json`: 9 RED + 5 ORANGE drift terms

</details>

---

## Rules

This repo enforces the `rules` skill contract:

- Zero placeholders/stubs/todos/mocks/fakes/invalid/minimal content in `src/`, skills, tests, workers, tools, runtime artifacts
- Source-truth separation: past truth, present overlay, future plan stay in their own timelines
- Mock workflows must never spawn `delete`, `clean up`, `remove`, or similar destructive actions
- Real artifacts only: deliver working artifacts backed by real tool output
- Verification before claim: every write/patch/terminal call must produce real output

Violations halt forward claims and require explicit repair direction.

---

## Environment

| Component | Value |
|---|---|
| Host | Windows 10 / git-bash |
| Hermes config | `C:\Users\krist\AppData\Local\hermes\config.yaml` |
| Skills dir | `C:\Users\krist\AppData\Local\hermes\skills\` |
| OpenJarvis | `C:\Users\krist\Desktop\OpenJarvis` |
| King Wen immutable tables | `C:\Users\krist\Desktop\KING-WEN-I-CHING-IMMUTABLE-TABLES` |
| Gutenberg cache | `C:\Users\krist\AppData\Local\hermes\cache\web\` |

---

## Verification

```bash
# Verify project structure
python3 target/legal-data/tmp_scripts/verify_project_structure.py

# Verify inject bindings
python3 target/legal-data/tmp_scripts/verify_inject_bindings.py

# Verify skill cluster
python3 target/legal-data/tmp_scripts/verify_skill_cluster.py
```

All verifications are ad-hoc and cleaned up after execution.

## Dependency flow

```
King Wen immutable tables
    -> emotional_engine.py / collapse_full_128(output)
        -> 5-axis vector + inject_site payload
            -> OpenJarvis Cartesia adapter / sidecar
                -> Voicebox training payloads
                    -> profiles.py / generation.py / personality.py
```

**Direction:** King Wen owns the method/state truth. Voicebox is downstream training consumer. The bridge is payload-shaped, not direct imports.

## Known blockers

- `test_collapse_full_1024.py` asserts `total_resolved == 1024`, but current engine returns `512` resolved states. This requires either test alignment or engine expansion; do not change engine behavior without explicit approval.
- `test_progressive_intents.py` is diagnostic-only because consensus is locked across slider values.

---

## Status

- Artifacts: complete and pushed to `main`
- Cluster: 21 skills activated
- Enforcement: cron jobs running
- README: this file
