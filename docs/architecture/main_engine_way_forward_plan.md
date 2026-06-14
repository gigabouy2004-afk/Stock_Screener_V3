# Main Engine Way Forward Plan

Date: 2026-06-15

Branch: `main-engine-sync-reset`

This plan is the execution contract for the new post-V3 branch.

## Phase 1: Branch Baseline

Goal: establish the new branch from `main` as the only active forward path.

Deliverables:

- New charter committed on this branch.
- New plan committed on this branch.
- New handover committed on this branch.
- README updated to point to the new branch-resident documents.
- Local and GitHub sync rule documented explicitly.

Rules:

- The branch must remain rooted from `main`.
- The charter, plan, and handover must live together on this branch.
- No completed step may update only one of local or GitHub.

## Phase 2: Retirement Boundary

Goal: separate historical V3 material from the new working direction.

Deliverables:

- Explicit statement that V3 is retired as the active forward path.
- Clear rule that V3 documents are historical reference only unless explicitly re-adopted.
- Branch startup order that points to the new documents first.

## Phase 3: New Engine Definition

Goal: define the new engine scope before code direction changes.

Deliverables:

- Confirmed user-facing paths.
- Confirmed hierarchy ownership by level.
- Confirmed backtesting role.
- Confirmed output contract.

## Phase 4: Code Audit From Main Root

Goal: decide what survives from the `main` tree into the new engine.

Deliverables:

- Module inventory.
- Classification of each module as reusable, historical, delete-later, or unclear.
- Short audit note under `docs/analysis/`.

Guardrail:

- Do not change engine behavior until the audit and the branch direction are documented.

## Completion Discipline

At the end of each completed step:

1. update charter if direction changed;
2. update this plan if phase order changed;
3. update handover if restart context changed;
4. commit locally in `D:\Tools\Stock_Screener_V3`;
5. push the same branch to GitHub;
6. verify branch sync with `git status --short --branch` and `git log --oneline --decorate -5`.
