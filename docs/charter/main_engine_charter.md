# V3 Charter Branch Charter

Date: 2026-06-15

Status: Active root charter branch for the June 12/13 documentation direction.

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `V3_charter`

## Purpose

This document is the canonical source of truth for the charter branch that starts from `main` and carries the June 12/13 charter direction, the active implementation plan, and the active handover documents together in one branch tree.

## Branch Root Rule

All charter-led product-direction work must start from a branch/tree rooted from `main`.

The active branch must contain, together:

- this charter;
- the active implementation plan;
- the active handover/startup documents.

The branch is not valid as the new working root if those three document sets drift apart.

## Local And GitHub Sync

The canonical local repository is:

```text
D:\Tools\Stock_Screener_V3
```

The canonical remote repository is:

```text
https://github.com/gigabouy2004-afk/Stock_Screener_V3.git
```

Required rule:

```text
The local branch in D:\Tools\Stock_Screener_V3 and the matching GitHub branch must remain synchronized for code, charter, plan, and handover state.
```

Completed work is not complete until:

1. the branch-resident charter is updated if direction changed;
2. the branch-resident plan is updated if execution order changed;
3. the branch-resident handover is updated if restart context changed;
4. the local branch is committed;
5. the same branch is pushed to GitHub;
6. local and remote are verified in sync.

Nightly handover notes must point to these in-repo branch documents as the primary restart source.

## Product Intent

The engine remains a user-directed stock analysis engine.

The June 12/13 documentation intent is that the charter work starts from the root only, as the `V3_charter` branch from `main`.

It must be built as one coherent hierarchy, not as stitched legacy paths and not as a continuation of the `v3-engine-rebuild-from-charter` branch.

## V2 Reference Rule

`V3_charter` must explicitly use V2 as a calculation reference baseline.

The reason is simple: many V2 calculations worked individually, even when later combined behavior drifted or became logically mixed.

Therefore:

- individually working V2 calculations are valid reference inputs for `V3_charter`;
- they may be reused, rechecked, or reimplemented as calculation-level building blocks;
- they must not be copied forward as uncontrolled route logic or cross-path overrides.

The active rule is:

```text
V2 calculations may be referenced because they worked individually.
V3_charter must then place them at the correct ownership level inside the path-first engine.
```

This means a V2 calculation must be evaluated in two separate ways:

1. Did the calculation itself work correctly in isolation?
2. Does its placement inside V3 obey the selected-path, matrix-owned, anti-leakage contract?

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

Allowed user-facing paths must be explicitly documented in this branch before implementation expands.

## Documentation Authority

Every new session on this branch must read these documents in this order:

1. `docs/charter/main_engine_charter.md`
2. `docs/charter/v3_original_intent_and_handover.md`
3. `docs/architecture/main_engine_way_forward_plan.md`
4. `docs/handover/current_session_handover.md`
5. `docs/handover/v3_engine_rebuild_startup.md`
6. `docs/handover/main_engine_startup_handover.md`

The June 12/13 charter and handover documents must be carried forward on `V3_charter` as part of the active branch document set, not left outside the root charter branch.
