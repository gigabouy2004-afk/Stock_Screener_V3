from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreWeights:
    route: float
    timing: float
    structure: float
    participation: float
    context: float
    risk: float

    def as_label(self) -> str:
        return (
            f"route={_format_number(self.route)},timing={_format_number(self.timing)},"
            f"structure={_format_number(self.structure)},participation={_format_number(self.participation)},"
            f"context={_format_number(self.context)},risk={_format_number(self.risk)}"
        )


@dataclass(frozen=True)
class StageScoreThresholds:
    selected_min: float
    watch_min: float


@dataclass(frozen=True)
class StageScoringConfig:
    weights: ScoreWeights
    thresholds: StageScoreThresholds


CROSSOVER_SCORING = StageScoringConfig(
    weights=ScoreWeights(route=30.0, timing=20.0, structure=20.0, participation=15.0, context=10.0, risk=10.0),
    thresholds=StageScoreThresholds(selected_min=72.0, watch_min=58.0),
)

SETUP_SCORING = StageScoringConfig(
    weights=ScoreWeights(route=30.0, timing=20.0, structure=20.0, participation=15.0, context=10.0, risk=10.0),
    thresholds=StageScoreThresholds(selected_min=72.0, watch_min=58.0),
)

DIVERGENCE_SCORING = StageScoringConfig(
    weights=ScoreWeights(route=30.0, timing=20.0, structure=15.0, participation=10.0, context=15.0, risk=10.0),
    thresholds=StageScoreThresholds(selected_min=72.0, watch_min=56.0),
)


def _format_number(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return f"{value:g}"
