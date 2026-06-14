# Main Engine Charter

Date: 2026-06-15

Status: Active replacement charter after V3 retirement.

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `main-engine-sync-reset`

## Purpose

V3 is old and is being retired as the active forward path.

This document is the canonical source of truth for the new engine branch that starts clean from `main` and carries the new charter, the new implementation plan, and the active handover documents together in one branch tree.

## Branch Root Rule

All new product-direction work must start from a branch/tree rooted from `main`.

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

The new engine remains a user-directed stock analysis engine.

It must be built as one coherent hierarchy, not as stitched legacy paths and not as a continuation of the V3 rebuild branch.

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

Allowed user-facing paths for the new engine must be explicitly documented in this branch before implementation expands.

## Documentation Authority

Every new session on this branch must read these documents in this order:

1. `docs/charter/main_engine_charter.md`
2. `docs/architecture/main_engine_way_forward_plan.md`
3. `docs/handover/main_engine_startup_handover.md`

Older V3 documents may be used only as historical reference material. They are not the controlling direction for this branch.
