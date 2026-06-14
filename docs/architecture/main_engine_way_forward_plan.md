# Main Engine Way Forward Plan

Date: 2026-06-15

Branch: `V3_charter`

This plan is the execution contract for the root-start charter branch.

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

## Phase 2: Root Charter Boundary

Goal: separate the `V3_Charter` root branch from the older rebuild branch.

Deliverables:

- Explicit statement that June 12/13 charter work starts from `main` root as `V3_charter`.
- Clear rule that `v3-engine-rebuild-from-charter` is not the root for the charter-led track.
- Branch startup order that points to the new documents first.

## Phase 3: New Engine Definition

Goal: define the charter-led engine scope before code direction changes.

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
