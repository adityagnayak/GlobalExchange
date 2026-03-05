"""engine package — mathematical computation layer."""

from engine.analyzer import SecurityAnalyzer, RiskMetrics, VaRResult, BenchmarkMismatch
from engine.constants import (
    ALL_BENCHMARKS, BENCHMARKS, BENCHMARK_NAMES,
    CURRENCY_MAP, EXCHANGE_BENCHMARK, EXCHANGE_NAME,
    WORLD_INDICES,
)
from engine.charts import (
    build_price_chart,
    build_returns_chart,
    build_drawdown_chart,
    build_distribution_chart,
    build_rolling_metrics_chart,
)

__all__ = [
    "SecurityAnalyzer", "RiskMetrics", "VaRResult", "BenchmarkMismatch",
    "ALL_BENCHMARKS", "BENCHMARKS", "BENCHMARK_NAMES", "CURRENCY_MAP",
    "EXCHANGE_BENCHMARK", "EXCHANGE_NAME", "WORLD_INDICES",
    "build_price_chart", "build_returns_chart", "build_drawdown_chart",
    "build_distribution_chart", "build_rolling_metrics_chart",
]
