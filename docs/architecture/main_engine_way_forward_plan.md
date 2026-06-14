# Main Engine Way Forward Plan

Date: 2026-06-15

Branch: `V3_charter`

This plan is the execution contract for the root-start charter branch.

## Plan Intent

This plan operationalizes the June 12/13 charter direction on `V3_charter`.

It exists to answer four questions clearly before code drift resumes:

1. What is the controlling document set?
2. What must be preserved from prior work?
3. What must be audited before changing behavior?
4. What validation gates must exist before promoting new engine logic?

The controlling direction for this branch is:

- `docs/charter/main_engine_charter.md`
- `docs/charter/v3_original_intent_and_handover.md`
- `docs/architecture/main_engine_way_forward_plan.md`
- `docs/handover/current_session_handover.md`
- `docs/handover/v3_engine_rebuild_startup.md`
- `docs/handover/main_engine_startup_handover.md`

## Core Execution Principles

- Start from `main` root only.
- Keep charter, plan, and handover synchronized on the same branch.
- Treat old artifacts as reusable input, not automatic product direction.
- Do not add new signal behavior before audit, path ownership, and validation gates are documented.
- Keep local `D:\Tools\Stock_Screener_V3` and GitHub `origin/V3_charter` synchronized after each completed step.

## Phase 1: Branch Baseline

Goal: establish the charter branch from `main` as the active root documentation path.

Deliverables:

- New charter committed on this branch.
- New plan committed on this branch.
- New handover committed on this branch.
- README updated to point to the new branch-resident documents.
- Local and GitHub sync rule documented explicitly.
- June 12/13 documentation intent restated as root-start branch direction.

Rules:

- The branch must remain rooted from `main`.
- The charter, plan, and handover must live together on this branch.
- No completed step may update only one of local or GitHub.

Completion check:

- `git status --short --branch` shows `V3_charter...origin/V3_charter`
- startup documents point to the branch-resident charter set
- nightly handover references the in-repo files first

## Phase 2: June 12/13 Document Consolidation

Goal: make the June 12/13 documentation set the explicit operating baseline of `V3_charter`.

Deliverables:

- The June 12/13 charter is carried forward as active reference in this branch.
- The June 12/13 handover documents are included in the startup order.
- Conflicting "start from rebuild branch" interpretations are removed from active guidance.
- Each active document states the root-start rule from `main`.

Detailed tasks:

1. Confirm which June 12/13 files are controlling versus historical.
2. Record their read order in the branch startup handover.
3. Mark any older branch-specific restart instructions as non-controlling for `V3_charter`.
4. Ensure the README sends future sessions to the `V3_charter` document chain first.

## Phase 3: Root Charter Boundary

Goal: separate the `V3_charter` root branch from the older rebuild branch.

Deliverables:

- Explicit statement that June 12/13 charter work starts from `main` root as `V3_charter`.
- Clear rule that `v3-engine-rebuild-from-charter` is not the root for the charter-led track.
- Branch startup order that points to the new documents first.

Boundary rules:

- `v3-engine-rebuild-from-charter` may be mined for implementation details, validation evidence, and historical decisions.
- It must not silently define the active charter or restart root.
- If a rule, matrix entry, or validation result from that branch is reused, the reuse must be restated on `V3_charter`.

## Phase 4: New Engine Definition

Goal: define the charter-led engine scope before code direction changes.

Deliverables:

- Confirmed user-facing paths.
- Confirmed hierarchy ownership by level.
- Confirmed backtesting role.
- Confirmed output contract.

Detailed outputs required in this phase:

- Path catalog:
  - `CROSSOVER`
  - `DIVERGENCE`
  - `MOMENTUM_SETUP` / `BULL_EXTENSION`
- Hierarchy ownership note for:
  - L0 input/data/date preparation
  - L1 baseline
  - L2 route
  - L3 path-specific evidence
  - L4 classification/scoring
  - L5 output and D+X validation
- Explicit statement of what cannot become a base route selector.
- Explicit backtesting rule:
  - run selected path as of D
  - load D+X only after classification
  - preserve no-lookahead behavior
- Explicit output contract:
  - explainable candidate state
  - score/confidence/risk reasoning
  - audit fields
  - validation fields

Decision gate before Phase 5:

- The branch docs must be sufficient for a new session to explain the engine scope without re-reading scattered validation artifacts.

## Phase 5: Code Audit From Main Root

Goal: decide what survives from the `main` tree into the new engine.

Deliverables:

- Module inventory.
- Classification of each module as reusable, historical, delete-later, or unclear.
- Short audit note under `docs/analysis/`.

Audit scope:

- `src/stock_screener_v3/`
- `tests/`
- `web_app_v3.py`
- report/output helpers
- provider/data-loading helpers
- evaluator and evidence modules
- backtesting utilities

Required classification labels:

- `REUSABLE_UTILITY`
- `REUSABLE_WITH_REFACTOR`
- `HISTORICAL_REFERENCE`
- `DELETE_LATER`
- `UNCLEAR_REQUIRES_DECISION`

Minimum audit questions per module:

1. Does it enforce or violate path-first design?
2. Does it mix calculation and decision logic?
3. Is it tied to V3 rebuild assumptions that no longer control this branch?
4. Can it survive unchanged, or does it need a boundary wrapper/refactor?
5. What tests already protect it?

Guardrail:

- Do not change engine behavior until the audit and the branch direction are documented.

## Phase 6: Architecture Freeze For Rebuild

Goal: lock the immediate target architecture before implementation waves begin.

Deliverables:

- Confirmed module boundaries.
- Confirmed data-provider boundary.
- Confirmed evidence-pack boundary.
- Confirmed evaluator boundary per path.
- Confirmed ranking/output boundary.

Required architecture decisions:

- what belongs in `models.py`
- what belongs in `data_provider.py`
- what belongs in `evidence.py`
- what belongs in `evaluators.py`
- what belongs in `runner.py`
- what belongs in `backtesting.py` and `backtest_engine.py`
- what belongs in reporting/output modules

Guardrail:

- No feature wave starts until path ownership and module ownership are both explicit.

## Phase 7: Implementation Wave 1

Goal: stabilize the shared engine skeleton without adding speculative new rules.

Deliverables:

- Clean L0-L5 orchestration path.
- Shared input and run contract.
- Shared evidence-pack assembly rules.
- Shared output contract for scan and backtest modes.
- Minimal tests for orchestration and non-leakage.

Focus:

- wiring
- contracts
- invariants
- no-lookahead safety
- audit visibility

Not the focus:

- calibration-driven score tuning
- sector expansion
- new broad context layers

## Phase 8: Path Implementation Waves

Goal: rebuild path logic deliberately, one family at a time, without leakage.

Execution order:

1. `CROSSOVER`
2. `DIVERGENCE`
3. `MOMENTUM_SETUP` / `BULL_EXTENSION`

For each path, required deliverables are:

- route definition
- required evidence definition
- optional support/context definition
- scoring and confidence rules
- anti-leakage tests
- D+X validation output fields

Per-path promotion gate:

- documented path contract
- implementation aligned to matrix ownership
- path-specific tests
- at least one dated validation note

## Phase 9: Validation Pack

Goal: prevent rule promotion based on isolated examples.

Minimum validation pack:

- at least 5 D dates
- multiple market regimes
- restricted-universe runs
- mixed/random samples
- candidate-density review
- score-bucket review
- best-high / worst-low view where relevant
- baseline comparison where relevant

Required reports:

- candidate summary
- failure summary
- score-bucket summary
- path-family summary
- collision/ranking summary when multiple families fire

Promotion rule:

- no rule becomes part of the active engine solely because it fixes one failure cluster

## Phase 10: Handover Discipline

Goal: make restart quality part of the build process.

At the end of a meaningful work block:

- update the charter if product direction changed
- update this plan if phase scope or sequencing changed
- update the active handover if restart context changed
- ensure the nightly handover points to the branch-resident files first
- leave enough restart context for the next session to continue without rediscovery

Required handover content:

- active branch
- controlling files
- current phase
- completed deliverables
- next concrete restart point
- open risks or unresolved decisions

## Completion Discipline

At the end of each completed step:

1. update charter if direction changed;
2. update this plan if phase order changed;
3. update handover if restart context changed;
4. commit locally in `D:\Tools\Stock_Screener_V3`;
5. push the same branch to GitHub;
6. verify branch sync with `git status --short --branch` and `git log --oneline --decorate -5`.
