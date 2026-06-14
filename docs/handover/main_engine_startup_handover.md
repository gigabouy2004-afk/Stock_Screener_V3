# V3 Charter Startup Handover

Last updated: 2026-06-15

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `V3_charter`

## Session Role

This is the startup and restart handover for the charter branch created from `main` to carry the June 12/13 root-start documentation direction.

## Read Order

Every new session on this branch must read:

1. `docs/charter/main_engine_charter.md`
2. `docs/charter/v3_original_intent_and_handover.md`
3. `docs/architecture/main_engine_way_forward_plan.md`
4. `docs/handover/current_session_handover.md`
5. `docs/handover/v3_engine_rebuild_startup.md`
6. this file

Do not start from `v3-engine-rebuild-from-charter` handovers by default for this charter-led track.

## Sync Rule

The local repo and GitHub must be synchronized together:

```text
Local:  D:\Tools\Stock_Screener_V3
Remote: https://github.com/gigabouy2004-afk/Stock_Screener_V3.git
Branch: V3_charter
```

Nightly handover and restart notes must point to these branch-resident documents first.

## Current Decision

- The June 12/13 documentation intent is preserved as a root-start branch from `main`.
- The active working root is `V3_charter`.
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
V3_charter
```
