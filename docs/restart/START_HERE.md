# V3_Charter Restart Folder

Use this folder as the single restart entry point for future Codex sessions.

Folder:

```text
D:\Tools\Stock_Screener_V3\docs\restart
```

Read in this order:

1. [01_v3_original_intent_and_handover.md](/D:/Tools/Stock_Screener_V3/docs/restart/01_v3_original_intent_and_handover.md)
2. [02_current_session_handover.md](/D:/Tools/Stock_Screener_V3/docs/restart/02_current_session_handover.md)
3. [03_README.md](/D:/Tools/Stock_Screener_V3/docs/restart/03_README.md)

Then verify branch state:

```powershell
cd D:\Tools\Stock_Screener_V3
git status --short --branch
git log --oneline --decorate -8
```

Expected branch state:

```text
## V3_Charter...origin/V3_Charter
```

Current restart-relevant commits:

- `66c381f Refresh V3_Charter restart documentation`
- `f62421b Extract stage scoring config defaults`
- `6bd0daf Clarify per-ticker grouped scoring intent`

Current restart baseline:

- `V3_Charter` is the only working branch baseline.
- June 13 charter is the only seed/source-of-truth charter.
- Score is per ticker, category-specific, and grouped by stage family for display.
- Current coding focus is continued extraction of hardcoded evaluator thresholds into explicit config/matrix-owned structures.

These files are restart copies collected into one folder for convenience. If they ever drift, the canonical sources remain:

- [docs/charter/v3_original_intent_and_handover.md](/D:/Tools/Stock_Screener_V3/docs/charter/v3_original_intent_and_handover.md)
- [docs/handover/current_session_handover.md](/D:/Tools/Stock_Screener_V3/docs/handover/current_session_handover.md)
- [README.md](/D:/Tools/Stock_Screener_V3/README.md)
