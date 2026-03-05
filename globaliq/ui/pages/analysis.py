"""
ui/pages/analysis.py

Security Analysis page — renders the full institutional analysis dashboard.
Calls engine.analyzer for computation, engine.charts for Plotly figures,
and ui.components for HTML blocks.
"""

from __future__ import annotations

import numpy as np
import streamlit as st
from datetime import datetime, timedelta

from engine import (
    SecurityAnalyzer,
    build_price_chart,
    build_returns_chart,
    build_drawdown_chart,
    build_distribution_chart,
    build_rolling_metrics_chart,
    ALL_BENCHMARKS,
    BENCHMARK_NAMES,
)
from ui import components as C


# ─── Sidebar config ────────────────────────────────────────────────────────────

def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown("### ⚙️ Analysis Setup")
        st.markdown("---")

        mode = st.radio(
            "Analysis Mode",
            ["Basic", "Advanced"],
            index=0 if st.session_state.get("sa_mode", "Basic") == "Basic" else 1,
            help="Basic: 4 key metrics. Advanced: 14+ metrics including VaR, drawdown, distribution.",
        )
        st.session_state["sa_mode"] = mode
        st.markdown("---")

        ticker_input = st.text_input(
            "Ticker Symbol",
            value=st.session_state.get("sa_last_ticker", "AAPL"),
            placeholder="AAPL, RELIANCE.NS, ASML, 7203.T…",
            help="Enter any global ticker. Append exchange suffix for non-US stocks.",
        ).upper().strip()

        # Auto-suggest benchmark from ticker suffix
        suggested = _suggest_benchmark(ticker_input)
        default_bench = suggested or st.session_state.get("sa_last_bench", "SPY")

        st.markdown("**Benchmark**")
        bench_opts = list(ALL_BENCHMARKS.keys())
        try:
            def_idx = bench_opts.index(default_bench)
        except ValueError:
            def_idx = 0

        benchmark = st.selectbox(
            "Benchmark",
            bench_opts,
            index=def_idx,
            format_func=lambda x: f"{x}  —  {ALL_BENCHMARKS[x]}",
            label_visibility="collapsed",
        )

        if suggested and suggested != benchmark:
            st.markdown(
                C.info_box(f"💡 Suggested benchmark for this exchange: <strong>{suggested}</strong>"),
                unsafe_allow_html=True,
            )

        st.markdown("---")

        period_type = st.radio("Time Period", ["Preset", "Custom"], horizontal=True)
        start_date = end_date = None
        period = "5y"

        if period_type == "Preset":
            period = st.selectbox("Period", ["1y", "3y", "5y", "10y", "max"], index=2)
        else:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("From", value=datetime.now() - timedelta(days=365 * 5))
            with col2:
                end_date = st.date_input("To", value=datetime.now())

        st.markdown("---")

        var_conf = 0.95
        if mode == "Advanced":
            st.markdown("**VaR Confidence Level**")
            var_conf = st.select_slider(
                "Confidence",
                options=[0.90, 0.95, 0.99],
                value=0.95,
                format_func=lambda x: f"{int(x * 100)}%",
                label_visibility="collapsed",
            )
            st.markdown("---")

        analyze = st.button("📊 Analyse", type="primary", use_container_width=True)
        st.markdown("---")
        st.markdown(
            '<div style="font-size:0.72rem;color:var(--muted);text-align:center;">'
            "Data via Yahoo Finance<br>Up to 30-min delay</div>",
            unsafe_allow_html=True,
        )

    return {
        "ticker":     ticker_input,
        "benchmark":  benchmark,
        "period":     period,
        "start_date": start_date,
        "end_date":   end_date,
        "mode":       mode,
        "var_conf":   var_conf,
        "analyze":    analyze,
    }


def _suggest_benchmark(ticker: str) -> str | None:
    from engine.constants import EXCHANGE_BENCHMARK
    for suffix, bench in EXCHANGE_BENCHMARK.items():
        if suffix in ticker:
            return bench
    return None


# ─── Error display ─────────────────────────────────────────────────────────────

def render_error(ticker: str) -> None:
    st.markdown(f"""
    <div style="padding:1.5rem;border:1px solid var(--border);border-radius:8px;margin:1rem 0;">
      <h3 style="color:#ef4444;margin:0 0 0.8rem;">❌ Could not load data for '{ticker}'</h3>
      <p style="color:var(--muted);">Common formats:</p>
      <ul style="color:var(--muted);margin-left:1.2rem;line-height:2;">
        <li>US stocks: <code>AAPL</code>, <code>TSLA</code>, <code>NVDA</code></li>
        <li>UK stocks: <code>HSBA.L</code>, <code>BP.L</code></li>
        <li>Indian stocks: <code>RELIANCE.NS</code>, <code>TCS.BO</code></li>
        <li>Japanese stocks: <code>7203.T</code>, <code>9984.T</code></li>
        <li>HK stocks: <code>0700.HK</code>, <code>9988.HK</code></li>
        <li>European stocks: <code>ASML</code>, <code>SAP.DE</code></li>
      </ul>
    </div>
    """, unsafe_allow_html=True)


# ─── Welcome state ─────────────────────────────────────────────────────────────

def render_welcome() -> None:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;color:var(--muted);">
      <div style="font-size:3rem;margin-bottom:1rem;">📈</div>
      <h2 style="font-weight:400;font-style:italic;color:var(--muted);">
        Enter a ticker symbol in the sidebar to begin your analysis.
      </h2>
      <p style="margin-top:1rem;font-size:0.92rem;">
        Supports 30+ currencies · Global exchanges · Dual-mode interface
      </p>
      <div style="margin-top:1.8rem;display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;font-size:0.88rem;">
        <span>🇺🇸 US: AAPL, MSFT, NVDA</span>
        <span>🇬🇧 UK: HSBA.L, BP.L</span>
        <span>🇮🇳 India: RELIANCE.NS, TCS.BO</span>
        <span>🇯🇵 Japan: 7203.T, 9984.T</span>
        <span>🇪🇺 Europe: ASML, SAP.DE</span>
        <span>🇭🇰 HK: 0700.HK, 9988.HK</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Main analysis render ──────────────────────────────────────────────────────

def render_analysis(analyzer: SecurityAnalyzer, mode: str, var_conf: float) -> None:
    sym = analyzer.get_currency_symbol()

    # ── Mode badge
    st.markdown(C.mode_badge(mode), unsafe_allow_html=True)

    # ── Benchmark mismatch warning
    mismatch = analyzer.check_benchmark_mismatch()
    if mismatch:
        st.markdown(
            C.warn_box(
                f"⚠️ <b>Benchmark mismatch:</b> {mismatch.exchange} — "
                f"suggested: <b>{mismatch.suggested_name} ({mismatch.suggested})</b>, "
                f"currently using <b>{mismatch.current}</b>.<br>"
                "💡 Cross-exchange pairs often lack overlapping trading days, "
                "making Beta/correlation unreliable."
            ),
            unsafe_allow_html=True,
        )
        if st.button(f"✨ Switch to {mismatch.suggested} & Re-analyse", type="primary"):
            st.session_state["force_benchmark"] = mismatch.suggested
            st.session_state["force_ticker"]    = analyzer.ticker
            st.session_state["force_analyze"]   = True
            st.rerun()

    if analyzer.benchmark_warning:
        st.markdown(C.warn_box(f"⚠️ {analyzer.benchmark_warning}"), unsafe_allow_html=True)

    # ── Block 1: Company cards
    info     = analyzer.info
    name     = info.get("longName") or info.get("shortName") or analyzer.ticker
    sector   = info.get("sector")   or "—"
    industry = info.get("industry") or "—"
    currency = analyzer.get_currency()
    exchange = info.get("exchange") or ""

    st.markdown(C.sub_header("Company Information"), unsafe_allow_html=True)
    st.markdown(
        C.company_cards(name, sector, industry, currency, exchange),
        unsafe_allow_html=True,
    )

    # ── Block 2: Price overview
    data   = analyzer.data
    cp     = float(data["Close"].iloc[-1]) if data is not None and not data.empty else None
    h52    = info.get("fiftyTwoWeekHigh") or (data["Close"].rolling(252).max().iloc[-1] if data is not None else None)
    l52    = info.get("fiftyTwoWeekLow")  or (data["Close"].rolling(252).min().iloc[-1] if data is not None else None)
    pfh    = ((cp - h52) / h52 * 100) if (cp and h52) else None
    mktcap = analyzer.format_large(info.get("marketCap"), prefix=sym)

    st.markdown(C.sub_header("💰 Price Overview"), unsafe_allow_html=True)
    st.markdown(C.price_cards(sym, cp, h52, l52, pfh, mktcap), unsafe_allow_html=True)

    # ── Block 3: Price chart
    st.markdown(C.sub_header("Price History & Moving Averages"), unsafe_allow_html=True)
    st.plotly_chart(build_price_chart(analyzer), use_container_width=True)

    # ── Pre-compute metrics
    metrics = analyzer.compute_all_metrics()

    # ── Block 4: Key risk metrics
    st.markdown(C.sub_header("Key Risk Metrics"), unsafe_allow_html=True)
    cols = st.columns(4)
    basic_metrics = [
        ("Beta",              _fmt(metrics.beta, "num2"),       "Sensitivity to benchmark. Beta=1 = market-neutral.",   "" if np.isnan(metrics.beta) else ("red" if metrics.beta > 1.5 else "green" if metrics.beta < 0.8 else "")),
        ("Annualized Return", _fmt(metrics.annualized_return, "pct1"), "Average yearly return over the selected period.", C.color_class(metrics.annualized_return)),
        ("Volatility (Ann.)", _fmt(metrics.volatility, "pct1"), "Annualized std dev of daily returns.",                 "red" if not np.isnan(metrics.volatility) and metrics.volatility > 0.3 else "green"),
        ("Max Drawdown",      _fmt(metrics.max_drawdown, "pct1"), "Worst peak-to-trough decline in the period.",        "red"),
    ]
    for col, (lbl, val, tip, clr) in zip(cols, basic_metrics):
        with col:
            st.markdown(C.metric_card(lbl, val, tip, clr), unsafe_allow_html=True)

    # ── Block 5: Advanced (opt-in)
    if mode == "Advanced":
        st.markdown(C.sub_header("Advanced Risk & Performance"), unsafe_allow_html=True)

        adv_row1 = [
            ("Alpha (Ann.)",      _fmt(metrics.alpha, "pct"),          "Excess return above CAPM expectation.",                  C.color_class(metrics.alpha)),
            ("Sharpe Ratio",      _fmt(metrics.sharpe, "num3"),         "Risk-adjusted return (total risk). >1 is good.",         C.color_class(metrics.sharpe)),
            ("Sortino Ratio",     _fmt(metrics.sortino, "num3"),        "Risk-adjusted return (downside risk only). >1 is good.", C.color_class(metrics.sortino)),
            ("Information Ratio", _fmt(metrics.information_ratio, "num3"), "Active return per unit of tracking error.",           C.color_class(metrics.information_ratio)),
        ]
        cols2 = st.columns(4)
        for col, (lbl, val, tip, clr) in zip(cols2, adv_row1):
            with col:
                st.markdown(C.metric_card(lbl, val, tip, clr), unsafe_allow_html=True)

        adv_row2 = [
            ("Calmar Ratio",    _fmt(metrics.calmar, "num3"),      "Annualized return / max drawdown.",                  C.color_class(metrics.calmar)),
            ("Correlation",     _fmt(metrics.correlation, "num3"), "Correlation with benchmark (−1 to +1).",             "blue"),
            ("Skewness",        _fmt(metrics.skewness, "num3"),    "Negative = left tail risk. Positive = right tail.",  ""),
            ("Excess Kurtosis", _fmt(metrics.kurtosis, "num3"),    ">0 = fat tails (more extreme events than normal).", ""),
        ]
        cols3 = st.columns(4)
        for col, (lbl, val, tip, clr) in zip(cols3, adv_row2):
            with col:
                st.markdown(C.metric_card(lbl, val, tip, clr), unsafe_allow_html=True)

        # ── Block 6: VaR
        st.markdown(C.sub_header("Value at Risk Analysis"), unsafe_allow_html=True)
        st.markdown(
            C.var_table(metrics.var_90, metrics.var_95, metrics.var_99),
            unsafe_allow_html=True,
        )

        # ── Block 7: Cumulative returns + drawdown
        bench_name = BENCHMARK_NAMES.get(analyzer.benchmark, analyzer.benchmark)
        st.markdown(
            f'<p style="font-size:0.78rem;color:var(--muted);">Benchmark: {bench_name}</p>',
            unsafe_allow_html=True,
        )
        col_ret, col_dd = st.columns(2)
        with col_ret:
            st.markdown(C.sub_header("Cumulative Returns"), unsafe_allow_html=True)
            st.plotly_chart(build_returns_chart(analyzer), use_container_width=True)
        with col_dd:
            st.markdown(C.sub_header("Drawdown from Peak"), unsafe_allow_html=True)
            st.plotly_chart(build_drawdown_chart(analyzer), use_container_width=True)

        # ── Block 8: Distribution + rolling metrics
        col_dist, col_roll = st.columns(2)
        with col_dist:
            st.markdown(C.sub_header("Daily Returns Distribution"), unsafe_allow_html=True)
            st.plotly_chart(build_distribution_chart(analyzer), use_container_width=True)
        with col_roll:
            st.markdown(C.sub_header("Rolling 90-Day Sharpe & Beta"), unsafe_allow_html=True)
            st.plotly_chart(build_rolling_metrics_chart(analyzer, window=90), use_container_width=True)

        # ── Block 9: Performance summary
        st.markdown(C.sub_header("Performance Summary"), unsafe_allow_html=True)
        perf_rows = analyzer.get_period_performance()
        if perf_rows:
            st.markdown(
                C.perf_table(perf_rows, bench_name),
                unsafe_allow_html=True,
            )

    # ── Block 10: Fundamentals
    st.markdown(C.sub_header("Fundamental Metrics"), unsafe_allow_html=True)
    fund_mode = "advanced" if mode == "Advanced" else "basic"
    fundamentals = analyzer.get_fundamentals(mode=fund_mode)
    items = list(fundamentals.items())
    mid   = len(items) // 2 or 2
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(C.fund_table(items[:mid]), unsafe_allow_html=True)
    with col_b:
        st.markdown(C.fund_table(items[mid:]), unsafe_allow_html=True)


# ─── Page entry point ──────────────────────────────────────────────────────────

def render_page() -> None:
    st.markdown(
        C.section_header(
            "Security Analysis",
            badge="Institutional Grade",
            sub="Risk metrics, VaR modelling, performance analytics & fundamentals — powered by live data",
        ),
        unsafe_allow_html=True,
    )

    # Init session state
    for key, default in [
        ("sa_mode", "Basic"), ("sa_analyzer", None),
        ("sa_last_ticker", "AAPL"), ("sa_last_bench", "SPY"),
        ("force_analyze", False), ("force_ticker", None), ("force_benchmark", None),
    ]:
        if key not in st.session_state:
            st.session_state[key] = default

    config = render_sidebar()
    ticker    = config["ticker"]
    benchmark = config["benchmark"]
    mode      = config["mode"]
    period    = config["period"]
    analyze   = config["analyze"]

    # Handle forced re-analyse (from mismatch switch)
    if st.session_state.get("force_analyze"):
        ticker    = st.session_state["force_ticker"]
        benchmark = st.session_state["force_benchmark"]
        st.session_state["force_analyze"] = False
        analyze = True

    if analyze and ticker:
        with st.spinner(f"Fetching data for {ticker}…"):
            az = SecurityAnalyzer(ticker, benchmark)
            ok = az.fetch_data(
                period     = period,
                start_date = str(config["start_date"]) if config["start_date"] else None,
                end_date   = str(config["end_date"])   if config["end_date"]   else None,
            )
        if ok:
            st.session_state["sa_analyzer"]    = az
            st.session_state["sa_last_ticker"] = ticker
            st.session_state["sa_last_bench"]  = benchmark
        else:
            render_error(ticker)
            return

    elif analyze and not ticker:
        st.warning("Please enter a valid ticker symbol.")
        return

    az = st.session_state.get("sa_analyzer")
    if az is None:
        render_welcome()
    else:
        render_analysis(az, mode, config["var_conf"])


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _fmt(val: float, fmt: str) -> str:
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    if fmt == "pct":
        return f"{val * 100:.2f}%"
    if fmt == "pct1":
        return f"{val * 100:.1f}%"
    if fmt == "num2":
        return f"{val:.2f}"
    if fmt == "num3":
        return f"{val:.3f}"
    return str(val)
