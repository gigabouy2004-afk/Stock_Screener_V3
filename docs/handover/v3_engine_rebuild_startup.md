# V3 Engine Rebuild Startup

Last updated: 2026-06-13

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `v3-engine-rebuild-from-charter`

Purpose: startup and handover document for rebuilding Stock Screener V3 from the canonical charter and matrices.

## Branch Role

Use this branch for corrected V3 engine reconstruction.

`main` remains the documented baseline and historical reference. Do not continue product-direction work directly on `main` until the rebuilt engine is validated and intentionally merged.

## Startup Order

Every new session on this branch must read these files in order:

1. `docs/charter/v3_original_intent_and_handover.md`
2. `docs/architecture/v3_stage_family_indicator_working_matrix.md`
3. `docs/architecture/v3_evidence_stage_matrix.md`
4. `docs/handover/current_session_handover.md`
5. This file

Do not start from old sector/regime validation artifacts, transition signoffs, or calibration reports unless a specific row in the working matrix points there.

## Required Git Check

Run:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -8
```

Expected branch:

```text
v3-engine-rebuild-from-charter...origin/v3-engine-rebuild-from-charter
```

## Current Build Contract

The engine must be rebuilt as one hierarchy:

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

Allowed user-facing paths:

- `CROSSOVER`
- `DIVERGENCE`
- `MOMENTUM_SETUP` / `BULL_EXTENSION`

Backtesting is not a fourth path. It is the validation column: run the same selected path as of historical D, then load D+X price only after classification.

## Reusable Code Only

Existing V3 code may be reused only as implementation material, not as product direction.

Reusable areas:

- API/provider wrapper ideas.
- symbol normalization.
- indicator calculation helpers.
- D-date slicing and D+X backtesting utilities.
- CSV/report/output helpers.
- reason-code and audit-output practices.

Do not carry forward as product direction:

- broad sector-folder calibration;
- cross-sector reports;
- default pan-USA scanning;
- market/sector/regime drift as a base engine;
- old WeightedScore as a promotion gate;
- any isolated rule that breaks path boundaries.

## Working Matrix Rule

Before coding any indicator, evidence item, context aid, or score component, update or confirm its row in:

```text
docs/architecture/v3_stage_family_indicator_working_matrix.md
```

Each row must define:

- API data required;
- V3 level;
- meaning for Crossover;
- meaning for Divergence;
- meaning for Momentum Setup / Bull Extension;
- Backtesting / D+X validation role;
- output fields;
- guardrail.

## First Implementation Step

Start with a code audit, not new signal rules.

Recommended first branch task:

1. Inventory current code modules.
2. Classify each module as:
   - reusable utility;
   - drift/historical artifact;
   - candidate for deletion later;
   - unclear and needs user decision.
3. Produce a short audit document under `docs/analysis/`.
4. Do not change engine behavior until the audit is documented.

## Documentation Discipline

At the end of every completed step:

1. Update the relevant architecture/handover document.
2. Commit locally.
3. Push this branch to GitHub.
4. Leave `git status --short --branch` clean.

