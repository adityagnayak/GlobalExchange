"""
engine/analyzer.py

Institutional-grade security analysis engine.
Pure computation layer — zero UI imports, zero Streamlit dependencies.
All public methods return plain Python scalars, dicts, or pandas objects.
"""

from __future__ import annotations

import time
import warnings
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats

from engine.constants import (
    EXCHANGE_BENCHMARK,
    EXCHANGE_CURRENCY,
    EXCHANGE_NAME,
    BENCHMARK_NAMES,
    CURRENCY_MAP,
    RISK_FREE_RATE,
    TRADING_DAYS,
)

warnings.filterwarnings("ignore")


# ─── Result dataclasses ────────────────────────────────────────────────────────

@dataclass
class VaRResult:
    hist:  float
    param: float
    cvar:  float


@dataclass
class RiskMetrics:
    """All computed risk & performance metrics for one security."""
    # Core
    beta:             float = float("nan")
    annualized_return: float = float("nan")
    volatility:       float = float("nan")
    max_drawdown:     float = float("nan")
    # Advanced
    alpha:            float = float("nan")
    sharpe:           float = float("nan")
    sortino:          float = float("nan")
    information_ratio: float = float("nan")
    calmar:           float = float("nan")
    correlation:      float = float("nan")
    skewness:         float = float("nan")
    kurtosis:         float = float("nan")
    # VaR
    var_90:  VaRResult = field(default_factory=lambda: VaRResult(float("nan"), float("nan"), float("nan")))
    var_95:  VaRResult = field(default_factory=lambda: VaRResult(float("nan"), float("nan"), float("nan")))
    var_99:  VaRResult = field(default_factory=lambda: VaRResult(float("nan"), float("nan"), float("nan")))


@dataclass
class PeriodPerformance:
    label:        str
    stock_return: float
    bench_return: float
    excess_return: float
    volatility:   float


@dataclass
class BenchmarkMismatch:
    exchange:       str
    suggested:      str
    suggested_name: str
    current:        str


# ─── Main Analyzer ─────────────────────────────────────────────────────────────

class SecurityAnalyzer:
    """
    Encapsulates all data fetching and metric calculation for a single ticker.

    Usage
    -----
    analyzer = SecurityAnalyzer("AAPL", benchmark="SPY")
    ok = analyzer.fetch_data(period="5y")
    if ok:
        metrics = analyzer.compute_all_metrics()
    """

    def __init__(self, ticker: str, benchmark: str = "SPY") -> None:
        self.ticker:    str = ticker.upper().strip()
        self.benchmark: str = benchmark

        self.data:             Optional[pd.DataFrame] = None
        self.benchmark_data:   Optional[pd.DataFrame] = None
        self.info:             dict = {}
        self.returns:          Optional[pd.Series]    = None
        self.benchmark_returns: Optional[pd.Series]   = None
        self.benchmark_warning: Optional[str]         = None

    # ── Data Fetching ──────────────────────────────────────────────────────────

    def fetch_data(
        self,
        period:     str            = "5y",
        start_date: Optional[str]  = None,
        end_date:   Optional[str]  = None,
    ) -> bool:
        """
        Fetch price history for the ticker and benchmark.
        Returns True on success, False on failure.
        Retries up to 3 times with back-off on rate limits.
        """
        for attempt in range(3):
            try:
                if attempt > 0:
                    time.sleep(attempt * 2)

                ticker_obj = yf.Ticker(self.ticker)

                if start_date and end_date:
                    self.data = ticker_obj.history(start=start_date, end=end_date)
                else:
                    self.data = ticker_obj.history(period=period)

                if self.data is None or self.data.empty:
                    if attempt == 2:
                        return False
                    continue

                # Info fetch — non-fatal if it fails
                try:
                    raw = ticker_obj.info
                    self.info = raw if raw and len(raw) > 1 else {}
                except Exception:
                    self.info = {}

                bench_obj = yf.Ticker(self.benchmark)
                if start_date and end_date:
                    self.benchmark_data = bench_obj.history(start=start_date, end=end_date)
                else:
                    self.benchmark_data = bench_obj.history(period=period)

                if self.benchmark_data is None or self.benchmark_data.empty:
                    if attempt == 2:
                        return False
                    continue

                self.returns           = self.data["Close"].pct_change().dropna()
                self.benchmark_returns = self.benchmark_data["Close"].pct_change().dropna()
                return True

            except Exception as e:
                err = str(e).lower()
                if "429" in err or "too many requests" in err:
                    if attempt < 2:
                        continue
                if attempt == 2:
                    return False

        return False

    # ── Currency & Exchange Helpers ────────────────────────────────────────────

    def get_currency(self) -> str:
        if self.info:
            c = self.info.get("currency")
            if c:
                return c
        for suffix, currency in EXCHANGE_CURRENCY.items():
            if suffix in self.ticker:
                return currency
        return "USD"

    def get_currency_symbol(self) -> str:
        return CURRENCY_MAP.get(self.get_currency(), self.get_currency() + " ")

    def get_exchange_suffix(self) -> str:
        for suffix in EXCHANGE_BENCHMARK:
            if suffix in self.ticker:
                return suffix
        return ""

    def check_benchmark_mismatch(self) -> Optional[BenchmarkMismatch]:
        suffix = self.get_exchange_suffix()
        if not suffix:
            return None
        suggested = EXCHANGE_BENCHMARK.get(suffix)
        if suggested and suggested != self.benchmark:
            return BenchmarkMismatch(
                exchange=EXCHANGE_NAME.get(suffix, suffix),
                suggested=suggested,
                suggested_name=BENCHMARK_NAMES.get(suggested, suggested),
                current=self.benchmark,
            )
        return None

    # ── Number Formatting ──────────────────────────────────────────────────────

    @staticmethod
    def format_large(value: Optional[float], prefix: str = "") -> str:
        """Format large numbers as e.g. $2.41T, £342B."""
        if value is None or (isinstance(value, float) and np.isnan(value)):
            return "N/A"
        try:
            v = float(value)
            if abs(v) >= 1e12:
                return f"{prefix}{v/1e12:.2f}T"
            if abs(v) >= 1e9:
                return f"{prefix}{v/1e9:.2f}B"
            if abs(v) >= 1e6:
                return f"{prefix}{v/1e6:.2f}M"
            return f"{prefix}{v:,.0f}"
        except Exception:
            return "N/A"

    # ── Aligned Returns ────────────────────────────────────────────────────────

    def _aligned(self) -> pd.DataFrame:
        """Inner-join stock and benchmark returns on date index."""
        merged = pd.concat(
            [self.returns, self.benchmark_returns], axis=1, join="inner"
        )
        merged.columns = ["stock", "bench"]
        return merged.dropna()

    # ══════════════════════════════════════════════════════════════════════════
    # INDIVIDUAL METRIC CALCULATIONS
    # ══════════════════════════════════════════════════════════════════════════

    def calculate_beta(self) -> float:
        merged = self._aligned()
        if len(merged) == 0:
            self.benchmark_warning = (
                f"No overlapping trading days between {self.ticker} and "
                f"{self.benchmark}. Use a benchmark from the same market."
            )
            return float("nan")
        if len(merged) < 30:
            self.benchmark_warning = (
                f"Only {len(merged)} overlapping trading days — "
                "metrics may be unreliable."
            )
        try:
            cov = np.cov(merged["stock"], merged["bench"])
            beta = cov[0, 1] / cov[1, 1]
            return float(beta) if not np.isnan(beta) else float("nan")
        except Exception:
            return float("nan")

    def calculate_alpha(self) -> float:
        """Jensen's Alpha."""
        beta = self.calculate_beta()
        if np.isnan(beta):
            return float("nan")
        merged = self._aligned()
        if len(merged) == 0:
            return float("nan")
        stock_ann = (1 + merged["stock"].mean()) ** TRADING_DAYS - 1
        bench_ann = (1 + merged["bench"].mean()) ** TRADING_DAYS - 1
        return stock_ann - (RISK_FREE_RATE + beta * (bench_ann - RISK_FREE_RATE))

    def calculate_annualized_return(self) -> float:
        if self.returns is None or len(self.returns) == 0:
            return float("nan")
        n_years = len(self.returns) / TRADING_DAYS
        if n_years <= 0:
            return float("nan")
        total = (1 + self.returns).prod() - 1
        return float((1 + total) ** (1 / n_years) - 1)

    def calculate_volatility(self) -> float:
        if self.returns is None or len(self.returns) == 0:
            return float("nan")
        return float(self.returns.std() * np.sqrt(TRADING_DAYS))

    def calculate_max_drawdown(self) -> float:
        if self.data is None or self.data.empty:
            return float("nan")
        prices   = self.data["Close"]
        roll_max = prices.cummax()
        return float(((prices - roll_max) / roll_max).min())

    def calculate_drawdown_series(self) -> pd.Series:
        prices   = self.data["Close"]
        roll_max = prices.cummax()
        return (prices - roll_max) / roll_max

    def calculate_sharpe(self) -> float:
        if self.returns is None:
            return float("nan")
        daily_rf = RISK_FREE_RATE / TRADING_DAYS
        excess   = self.returns - daily_rf
        if excess.std() == 0:
            return float("nan")
        return float((excess.mean() / excess.std()) * np.sqrt(TRADING_DAYS))

    def calculate_sortino(self) -> float:
        if self.returns is None:
            return float("nan")
        daily_rf = RISK_FREE_RATE / TRADING_DAYS
        excess   = self.returns - daily_rf
        downside = excess[excess < 0]
        if len(downside) == 0 or downside.std() == 0:
            return float("nan")
        return float((excess.mean() / downside.std()) * np.sqrt(TRADING_DAYS))

    def calculate_information_ratio(self) -> float:
        merged = self._aligned()
        if len(merged) == 0:
            return float("nan")
        active = merged["stock"] - merged["bench"]
        if active.std() == 0:
            return float("nan")
        return float((active.mean() / active.std()) * np.sqrt(TRADING_DAYS))

    def calculate_calmar(self) -> float:
        ann = self.calculate_annualized_return()
        mdd = self.calculate_max_drawdown()
        if np.isnan(ann) or np.isnan(mdd) or mdd == 0:
            return float("nan")
        return float(ann / abs(mdd))

    def calculate_correlation(self) -> float:
        merged = self._aligned()
        if len(merged) < 2:
            return float("nan")
        return float(merged["stock"].corr(merged["bench"]))

    def calculate_skewness(self) -> float:
        if self.returns is None:
            return float("nan")
        return float(stats.skew(self.returns.dropna()))

    def calculate_kurtosis(self) -> float:
        if self.returns is None:
            return float("nan")
        return float(stats.kurtosis(self.returns.dropna()))

    def calculate_var(self, confidence: float = 0.95) -> VaRResult:
        """
        Log-normal VaR methodology.

        1. Convert simple returns → log returns: r_log = ln(1 + r)
        2. Compute risk metrics on the log distribution (closer to Normal)
        3. Convert back to simple terms: r_simple = exp(r_log) − 1
        """
        if self.returns is None or len(self.returns) == 0:
            return VaRResult(float("nan"), float("nan"), float("nan"))

        r_simple = self.returns.dropna().values
        r_log    = np.log1p(r_simple)
        alpha    = 1 - confidence

        # Historical VaR
        log_hist   = np.percentile(r_log, alpha * 100)
        hist_var   = float(np.expm1(log_hist))

        # Parametric (log-normal)
        mu_log, sigma_log = r_log.mean(), r_log.std()
        z                 = stats.norm.ppf(alpha)
        log_param         = mu_log + z * sigma_log
        param_var         = float(np.expm1(log_param))

        # CVaR (Expected Shortfall)
        tail = r_log[r_log <= log_hist]
        cvar = float(np.expm1(tail.mean())) if len(tail) > 0 else hist_var

        return VaRResult(hist=hist_var, param=param_var, cvar=cvar)

    # ── Moving Averages ────────────────────────────────────────────────────────

    def get_moving_averages(self) -> dict[str, pd.Series]:
        close = self.data["Close"]
        return {
            "ma50":  close.rolling(50).mean(),
            "ma100": close.rolling(100).mean(),
            "ma200": close.rolling(200).mean(),
        }

    # ── Cumulative Returns ─────────────────────────────────────────────────────

    def get_cumulative_returns(self) -> tuple[pd.Series, pd.Series]:
        stock_cum = (1 + self.returns).cumprod() - 1
        bench_cum = (1 + self.benchmark_returns).cumprod() - 1
        return stock_cum, bench_cum

    # ── Fundamentals ──────────────────────────────────────────────────────────

    def get_fundamentals(self, mode: str = "basic") -> dict[str, str]:
        info = self.info
        sym  = self.get_currency_symbol()

        def safe(key, scale=1, is_pct=False, is_large=False):
            val = info.get(key)
            if val is None:
                return "N/A"
            try:
                v = float(val) / scale
                if is_pct:
                    return f"{v * 100:.2f}%"
                if is_large:
                    return self.format_large(v, prefix=sym)
                return f"{v:.2f}"
            except Exception:
                return "N/A"

        mktcap = info.get("marketCap")
        basic = {
            "Market Cap":     self.format_large(mktcap, prefix=sym) if mktcap else "N/A",
            "P/E Ratio":      safe("trailingPE"),
            "Dividend Yield": safe("dividendYield", is_pct=True),
            "ROE":            safe("returnOnEquity", is_pct=True),
        }

        if mode == "basic":
            return basic

        return {
            **basic,
            "Forward P/E":     safe("forwardPE"),
            "PEG Ratio":       safe("pegRatio"),
            "Price/Book":      safe("priceToBook"),
            "ROA":             safe("returnOnAssets", is_pct=True),
            "Profit Margin":   safe("profitMargins", is_pct=True),
            "Debt/Equity":     safe("debtToEquity"),
            "Current Ratio":   safe("currentRatio"),
            "Revenue Growth":  safe("revenueGrowth", is_pct=True),
            "Earnings Growth": safe("earningsGrowth", is_pct=True),
            "EPS (TTM)":       safe("trailingEps"),
            "52W High":        f"{sym}{info.get('fiftyTwoWeekHigh', 'N/A')}",
            "52W Low":         f"{sym}{info.get('fiftyTwoWeekLow',  'N/A')}",
        }

    # ── Period Performance ─────────────────────────────────────────────────────

    def get_period_performance(self) -> list[PeriodPerformance]:
        """
        Return return/volatility breakdown for 1M, 3M, 6M, 1Y, 3Y, 5Y.
        """
        periods = {
            "1 Month":  21,
            "3 Months": 63,
            "6 Months": 126,
            "1 Year":   252,
            "3 Years":  756,
            "5 Years":  1260,
        }
        results = []
        for label, days in periods.items():
            if len(self.returns) < days:
                continue
            sub   = self.returns.iloc[-days:]
            s_ret = float((1 + sub).prod() - 1)
            s_vol = float(sub.std() * np.sqrt(TRADING_DAYS))

            b_ret = float("nan")
            if len(self.benchmark_returns) >= days:
                b_sub = self.benchmark_returns.iloc[-days:]
                b_ret = float((1 + b_sub).prod() - 1)

            excess = s_ret - b_ret if not np.isnan(b_ret) else float("nan")
            results.append(PeriodPerformance(
                label=label,
                stock_return=s_ret,
                bench_return=b_ret,
                excess_return=excess,
                volatility=s_vol,
            ))
        return results

    # ── Convenience: compute everything at once ───────────────────────────────

    def compute_all_metrics(self) -> RiskMetrics:
        """Compute and return every risk metric in one call."""
        return RiskMetrics(
            beta              = self.calculate_beta(),
            annualized_return = self.calculate_annualized_return(),
            volatility        = self.calculate_volatility(),
            max_drawdown      = self.calculate_max_drawdown(),
            alpha             = self.calculate_alpha(),
            sharpe            = self.calculate_sharpe(),
            sortino           = self.calculate_sortino(),
            information_ratio = self.calculate_information_ratio(),
            calmar            = self.calculate_calmar(),
            correlation       = self.calculate_correlation(),
            skewness          = self.calculate_skewness(),
            kurtosis          = self.calculate_kurtosis(),
            var_90            = self.calculate_var(0.90),
            var_95            = self.calculate_var(0.95),
            var_99            = self.calculate_var(0.99),
        )
