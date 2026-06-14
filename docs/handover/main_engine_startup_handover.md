# Main Engine Startup Handover

Last updated: 2026-06-15

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `main-engine-sync-reset`

## Session Role

This is the startup and restart handover for the new branch created from `main` after the decision to retire V3 as the active forward workstream.

## Read Order

Every new session on this branch must read:

1. `docs/charter/main_engine_charter.md`
2. `docs/architecture/main_engine_way_forward_plan.md`
3. this file

Do not start from V3 rebuild handovers by default.

## Sync Rule

The local repo and GitHub must be synchronized together:

```text
Local:  D:\Tools\Stock_Screener_V3
Remote: https://github.com/gigabouy2004-afk/Stock_Screener_V3.git
Branch: main-engine-sync-reset
```

Nightly handover and restart notes must point to these branch-resident documents first.

## Current Decision

- V3 is retired as the active forward branch.
- The new working root is `main-engine-sync-reset`.
- The branch starts from `main`, not from `v3-engine-rebuild-from-charter`.
- The charter, plan, and handover are now expected to move together on this branch.

## Preferred Next Restart Point

1. Verify branch and sync state.
2. Re-read the new charter.
3. Re-read the new plan.
4. Begin the code audit from the `main` tree and classify reusable versus retired material.

## Required Git Check

Run:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -8
```

Expected branch:

```text
main-engine-sync-reset
```
