"""Stock Screener V3 core package."""

from stock_screener_v3.backtest_engine import BacktestEngine, InMemoryPriceProvider
from stock_screener_v3.data_provider import YahooPriceProvider
from stock_screener_v3.evaluators import CrossoverEvaluator, DivergenceEvaluator
from stock_screener_v3.models import (
    BacktestResult,
    BacktestRunConfig,
    CandidateClass,
    EvidencePack,
    PriceDataBundle,
    ReviewPriority,
    ScoreResult,
    StageEvaluation,
    UniverseRecord,
)

__all__ = [
    "BacktestEngine",
    "BacktestResult",
    "BacktestRunConfig",
    "CandidateClass",
    "CrossoverEvaluator",
    "DivergenceEvaluator",
    "EvidencePack",
    "InMemoryPriceProvider",
    "PriceDataBundle",
    "ReviewPriority",
    "ScoreResult",
    "StageEvaluation",
    "UniverseRecord",
    "YahooPriceProvider",
]
