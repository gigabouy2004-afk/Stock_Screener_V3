# V3 Charter Working Plan

Date: 2026-06-15

Branch: `V3_charter`

This document does not introduce a new phased methodology.

Its purpose is only to restate, in one place, the active working direction already established by the June 12/13 charter and handover documents now carried on `V3_charter`.

## Controlling Documents

The active document chain for this branch is:

1. `docs/charter/main_engine_charter.md`
2. `docs/charter/v3_original_intent_and_handover.md`
3. `docs/handover/current_session_handover.md`
4. `docs/handover/v3_engine_rebuild_startup.md`
5. this file

If any note conflicts with `docs/charter/v3_original_intent_and_handover.md`, that charter remains controlling unless the user explicitly changes direction.

## Root Rule

The June 12/13 documentation intent is that charter-led work starts from the root only, as branch `V3_charter` from `main`.

The branch-resident charter, handover, and working-plan documents must move together.

The local repo at:

```text
D:\Tools\Stock_Screener_V3
```

and the GitHub branch at:

```text
origin/V3_charter
```

must remain synchronized.

## Active Engine Direction

The active engine direction carried forward from the June 12/13 documents is:

- the engine is CSV-based and user-directed;
- it is not a broad market research engine by default;
- it must process only the user-provided universe;
- it must analyze only the user-selected path or paths;
- it must preserve path-first design;
- it must prevent one path's evidence from leaking into another path's route logic.

The branch also carries this explicit V2 baseline rule:

- individually working V2 calculations are reference material for `V3_charter`;
- they should be treated as reusable calculation candidates, not automatic final engine behavior;
- each reused V2 calculation must still be placed at the correct V3 ownership level.

The engine flow remains:

```text
CSV input
-> user-selected path
-> API data retrieval required by that path
-> L0 preparation
-> L1 baseline
-> L2 route
-> L3 path-specific evidence
-> L4 classification and scoring
-> L5 output and D+X validation
```

## Active User-Facing Paths

The active allowed user-facing paths remain:

- `CROSSOVER`
- `DIVERGENCE`
- `MOMENTUM_SETUP` / `BULL_EXTENSION`

No hidden fourth path should be introduced.

Market context, sector context, EMA200, lifetime high behavior, and other aids may refine confidence, risk, explanation, or validation only inside the selected path trajectory.

They must not become a base route selector unless the charter is explicitly changed.

## Working Matrix Requirement

The active matrix requirement carried forward from June 12/13 remains in force.

Reference documents:

- `docs/architecture/v3_evidence_stage_matrix.md`
- `docs/architecture/v3_stage_family_indicator_working_matrix.md`

No indicator, evidence item, or context aid should be treated as globally meaningful across all paths by default.

If an item is used, its path ownership and meaning should be explicit in the matrix.

This applies directly to V2 calculations that previously worked in isolation.

Their prior usefulness is a reason to reference them, not a reason to bypass matrix ownership.

## What This Branch Is Doing

This branch is carrying the June 12/13 charter set forward from `main` root.

It is not changing the underlying charter direction on its own.

It is establishing one synchronized branch where:

- the charter is present;
- the handover is present;
- the working plan is present;
- local and GitHub stay in sync;
- future implementation/detailing can happen without losing the June 12/13 source of truth.

## Immediate Working Focus

The immediate focus is to detail the active engine work without changing the June 12/13 charter meaning.

That means:

- preserve the exact path-first contract;
- preserve the exact three-path user model;
- preserve the L0-L5 hierarchy;
- baseline individually working V2 calculations as reference inputs for `V3_charter`;
- preserve D-date and D+X validation rules;
- preserve the matrix ownership rule;
- preserve the local/GitHub sync rule;
- restate implementation details only when they are grounded in the carried-forward docs or code.

## Restart Rule

At restart, begin by re-reading:

1. `docs/charter/v3_original_intent_and_handover.md`
2. `docs/handover/current_session_handover.md`
3. `docs/handover/v3_engine_rebuild_startup.md`
4. this file

Then continue detailing or implementing from that carried-forward direction only.
