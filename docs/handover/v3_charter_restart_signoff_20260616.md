# V3_Charter Restart Signoff 2026-06-16

Last updated: 2026-06-16

Repo: `D:\Tools\Stock_Screener_V3`

GitHub: `https://github.com/gigabouy2004-afk/Stock_Screener_V3.git`

Branch: `V3_Charter`

Expected branch state:

```text
## V3_Charter...origin/V3_Charter
```

## Low-Token Restart Path

For a new Codex session, read only these files first:

1. [v3_charter_restart_signoff_20260616.md](/D:/Tools/Stock_Screener_V3/docs/handover/v3_charter_restart_signoff_20260616.md)
2. [v3_charter_consolidated_engine_design.md](/D:/Tools/Stock_Screener_V3/docs/charter/v3_charter_consolidated_engine_design.md)
3. [v3_original_intent_and_handover.md](/D:/Tools/Stock_Screener_V3/docs/charter/v3_original_intent_and_handover.md)
4. Verify sync:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -8
```

Do not begin by re-reading older June 1, legacy V3 rebuild, or long historical handover material unless an ambiguity remains after these three files.

## Current Approved Baseline

- The single offline master document is [v3_charter_consolidated_engine_design.md](/D:/Tools/Stock_Screener_V3/docs/charter/v3_charter_consolidated_engine_design.md).
- Current document version is `V1.6`.
- The original June 13 seed document remains [v3_original_intent_and_handover.md](/D:/Tools/Stock_Screener_V3/docs/charter/v3_original_intent_and_handover.md).
- The engine is a CSV-driven equity screener, not a portfolio-management or order-execution system.
- User-facing path families remain:
  - `CROSSOVER`
  - `DIVERGENCE`
  - `SETUP`
- `CROSSOVER` includes:
  - `PRE_BULL_CROSSOVER`
  - `PRE_BEAR_CROSSOVER`

## What Is Locked

- `PRE_BULL_CROSSOVER` is for early bull-phase entry review.
- `PRE_BEAR_CROSSOVER` is for capital-preservation exit review on long-held equities.
- `DIVERGENCE` validates whether an investment opportunity may be developing.
- `SETUP` is a pure-play market-based entry path with a default `1M` structural baseline.
- Indicator processing is API/provider-driven.
- Current free default backend remains Yahoo Finance through `yfinance`, behind a swappable provider abstraction.
- Sector and market context are audit/context rows only with `Weight = 0`.
- `4H` and `1H` MACD are approved only for `CROSSOVER` in the initial release.
- `PriceBand` is now a signed-off matrix row for long-term support/extension context, not a stop-loss or swing-target module.
- `EMA52High` and `EMA200High` are defined as EMA calculations over the truncated daily `High` series.
- The scoring manifest baseline is `config/scoring_manifest.json`.
- Regression artifacts are rooted under `tests/regression/`.

## Current Code Truth

The repo package remains the active implementation surface:

- [src/stock_screener_v3](/D:/Tools/Stock_Screener_V3/src/stock_screener_v3)
- [web_app_v3.py](/D:/Tools/Stock_Screener_V3/web_app_v3.py)

The file [C:\Users\dell\OneDrive\Desktop\Stock_Engine3_Pythoncode.py](/C:/Users/dell/OneDrive/Desktop/Stock_Engine3_Pythoncode.py) has been reviewed and accepted only as a seed scaffold, not as a drop-in replacement.

Accepted carry-forward pieces from that file:

- `DEFAULT_MANIFEST` direction
- `rsi_upper_bound` object shape
- L0 deep-copy slicing pattern
- `EMA52High` and `EMA200High` computation over `High`
- mixed zero-line MACD handling idea
- path-isolated evaluation structure

Explicitly not accepted as-is:

- standalone `tkinter` desktop UI
- mock-data fallback behavior
- simplified divergence placeholder logic
- early `SETUP` forced-return pattern that skips full score and audit trail
- direct standalone script placement outside the package/repo structure

## Current Next Coding Step

The next engineering step is to absorb the accepted parts of `Stock_Engine3_Pythoncode.py` into the real package structure without breaking the charter.

Priority order:

1. Introduce or expand the manifest/config layer inside the package.
2. Preserve the L0 deep-copy slicing and D-vs-D+X isolation rules in the real provider/execution path.
3. Move the approved EMA high-boundary calculations into package indicator code.
4. Keep `web_app_v3.py` as the active UI surface.
5. Do not ship the desktop `tkinter` script as the active engine UI.

## Latest Relevant Commits

- `bb50871` Record V1.6 charter revision hash
- `9c11379` Advance master charter to V1.6
- `5e8180a` Record V1.5 charter revision hash
- `be20679` Advance master charter to V1.5
- `19eb21c` Record V1.4 charter revision hash
- `0f49e7c` Update master charter to V1.4

## Restart Guardrails

- Do not reinterpret the charter from older broad rebuild documents.
- Do not flatten all stage families into one global score meaning.
- Do not let market/sector context become route logic.
- Do not let `SETUP` use intraday MACD layers by default in the initial release.
- Do not introduce hidden magic numbers into evaluator code when the manifest should own them.
- Do not short-circuit Setup forced rejections; score and audit output must still be emitted.

## Restart Decision

If a new session starts now, it should begin from this exact instruction:

```text
Use V1.6 of the consolidated charter as the source of truth.
Use Stock_Engine3_Pythoncode.py only as a seed scaffold.
Integrate accepted manifest/slicing/EMA-high logic into the real package and web app path.
Do not invent a new UI surface or a parallel engine.
```
