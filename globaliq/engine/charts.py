"""
engine/charts.py

Plotly chart factory functions.
Each function accepts an analyzer (or raw data) and returns a go.Figure.
No Streamlit imports — charts are passed to st.plotly_chart() in the UI layer.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats

from engine.analyzer import SecurityAnalyzer
from engine.constants import BENCHMARK_NAMES

# ─── Shared layout defaults ────────────────────────────────────────────────────

_LAYOUT = dict(
    font_family  = "Helvetica, 'Helvetica Neue', Arial, sans-serif",
    plot_bgcolor = "rgba(0,0,0,0)",
    paper_bgcolor= "rgba(0,0,0,0)",
    xaxis        = dict(showgrid=True, gridcolor="rgba(128,128,128,0.10)", zeroline=False),
    yaxis        = dict(showgrid=True, gridcolor="rgba(128,128,128,0.10)", zeroline=False),
    margin       = dict(l=10, r=10, t=40, b=10),
    legend       = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    hovermode    = "x unified",
    font_color   = "#94a3b8",
)

_COLORS = dict(
    primary   = "#c94040",   # stock line / negative
    secondary = "#4a7ec4",   # benchmark
    ma50      = "#4a7ec4",
    ma100     = "#c48a1a",
    ma200     = "#4a9e42",
    up        = "#4a9e42",
    down      = "#c94040",
    fill_red  = "rgba(201,64,64,0.15)",
    fill_blue = "rgba(74,126,196,0.12)",
)


# ─── Price History & Volume ────────────────────────────────────────────────────

def build_price_chart(analyzer: SecurityAnalyzer) -> go.Figure:
    """Candlestick / line + moving averages + volume sub-plot."""
    data = analyzer.data
    mas  = analyzer.get_moving_averages()
    name = analyzer.ticker
    sym  = analyzer.get_currency_symbol()

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.03,
    )

    # Price line
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Close"], name=name,
        line=dict(color=_COLORS["primary"], width=1.8),
        hovertemplate="%{y:.2f}<extra></extra>",
    ), row=1, col=1)

    # Moving averages
    for period, color, label in [
        (50,  _COLORS["ma50"],  "MA50"),
        (100, _COLORS["ma100"], "MA100"),
        (200, _COLORS["ma200"], "MA200"),
    ]:
        fig.add_trace(go.Scatter(
            x=data.index, y=mas[f"ma{period}"],
            name=label, line=dict(color=color, width=1, dash="dot"),
            hovertemplate=f"{label}: %{{y:.2f}}<extra></extra>",
        ), row=1, col=1)

    # 52-week high/low bands
    high_52 = data["Close"].rolling(252).max()
    low_52  = data["Close"].rolling(252).min()
    for series, label, color in [
        (high_52, "52W High", "rgba(74,158,66,0.35)"),
        (low_52,  "52W Low",  "rgba(201,64,64,0.35)"),
    ]:
        fig.add_trace(go.Scatter(
            x=data.index, y=series, name=label,
            line=dict(color=color, width=0.8, dash="dash"),
            hovertemplate=f"{label}: %{{y:.2f}}<extra></extra>",
        ), row=1, col=1)

    # Volume bars (colour by day direction)
    vol_colors = [
        _COLORS["up"] if c >= o else _COLORS["down"]
        for c, o in zip(data["Close"], data["Open"])
    ]
    fig.add_trace(go.Bar(
        x=data.index, y=data["Volume"],
        name="Volume", marker_color=vol_colors, opacity=0.6,
        hovertemplate="Vol: %{y:,.0f}<extra></extra>",
    ), row=2, col=1)

    fig.update_layout(
        **_LAYOUT,
        title=f"{name} — Price History & Volume",
        height=500,
    )
    fig.update_yaxes(title_text=f"Price ({sym})", row=1, col=1)
    fig.update_yaxes(title_text="Volume",          row=2, col=1)
    return fig


# ─── Cumulative Returns ────────────────────────────────────────────────────────

def build_returns_chart(analyzer: SecurityAnalyzer) -> go.Figure:
    """Cumulative return % vs benchmark over the analysis period."""
    stock_cum, bench_cum = analyzer.get_cumulative_returns()
    bench_name = BENCHMARK_NAMES.get(analyzer.benchmark, analyzer.benchmark)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=stock_cum.index, y=stock_cum * 100,
        name=analyzer.ticker,
        line=dict(color=_COLORS["primary"], width=2),
        hovertemplate="%{y:.1f}%<extra>" + analyzer.ticker + "</extra>",
    ))
    fig.add_trace(go.Scatter(
        x=bench_cum.index, y=bench_cum * 100,
        name=bench_name,
        line=dict(color=_COLORS["secondary"], width=2, dash="dot"),
        hovertemplate="%{y:.1f}%<extra>" + bench_name + "</extra>",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(128,128,128,0.4)")
    fig.update_layout(**_LAYOUT, title="Cumulative Returns (%)", height=380)
    fig.update_yaxes(title_text="Return (%)")
    return fig


# ─── Drawdown ─────────────────────────────────────────────────────────────────

def build_drawdown_chart(analyzer: SecurityAnalyzer) -> go.Figure:
    """Peak-to-trough drawdown over time."""
    dd = analyzer.calculate_drawdown_series() * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dd.index, y=dd,
        name="Drawdown",
        fill="tozeroy",
        line=dict(color=_COLORS["primary"], width=1),
        fillcolor=_COLORS["fill_red"],
        hovertemplate="%{y:.2f}%<extra></extra>",
    ))
    fig.update_layout(**_LAYOUT, title="Drawdown from Peak (%)", height=300)
    fig.update_yaxes(title_text="Drawdown (%)")
    return fig


# ─── Returns Distribution ─────────────────────────────────────────────────────

def build_distribution_chart(analyzer: SecurityAnalyzer) -> go.Figure:
    """Daily returns histogram with normal-distribution overlay."""
    r          = analyzer.returns.dropna() * 100
    mu, sigma  = r.mean(), r.std()
    x_range    = np.linspace(r.min(), r.max(), 300)
    normal_pdf = stats.norm.pdf(x_range, mu, sigma)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=r, nbinsx=60,
        name="Daily Returns",
        marker_color=_COLORS["secondary"],
        opacity=0.7,
        histnorm="probability density",
        hovertemplate="%{x:.2f}%: %{y:.4f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x_range, y=normal_pdf,
        name="Normal Distribution",
        line=dict(color=_COLORS["primary"], width=2),
        hovertemplate="%{y:.4f}<extra></extra>",
    ))
    fig.add_vline(
        x=mu,
        line_dash="dash",
        line_color="rgba(200,160,0,0.8)",
        annotation_text=f"Mean: {mu:.2f}%",
    )
    fig.update_layout(**_LAYOUT, title="Daily Returns Distribution", height=340)
    fig.update_xaxes(title_text="Daily Return (%)")
    fig.update_yaxes(title_text="Probability Density")
    return fig


# ─── Rolling Metrics ──────────────────────────────────────────────────────────

def build_rolling_metrics_chart(analyzer: SecurityAnalyzer, window: int = 90) -> go.Figure:
    """Rolling Sharpe and Beta over a configurable window."""
    from engine.constants import RISK_FREE_RATE, TRADING_DAYS

    daily_rf = RISK_FREE_RATE / TRADING_DAYS
    merged   = pd.concat(
        [analyzer.returns, analyzer.benchmark_returns], axis=1, join="inner"
    ).dropna()
    merged.columns = ["stock", "bench"]

    roll = merged.rolling(window)
    roll_sharpe = (
        (merged["stock"] - daily_rf).rolling(window).mean()
        / merged["stock"].rolling(window).std()
        * np.sqrt(TRADING_DAYS)
    )
    roll_beta = roll.cov()["stock"].xs("bench", level=1) / roll.var()["bench"]

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.05,
                        subplot_titles=["Rolling Sharpe", "Rolling Beta"])
    fig.add_trace(go.Scatter(
        x=roll_sharpe.index, y=roll_sharpe,
        name="Sharpe", line=dict(color=_COLORS["secondary"], width=1.5),
    ), row=1, col=1)
    fig.add_hline(y=1, line_dash="dash", line_color="rgba(128,128,128,0.4)", row=1, col=1)

    fig.add_trace(go.Scatter(
        x=roll_beta.index, y=roll_beta,
        name="Beta", line=dict(color=_COLORS["primary"], width=1.5),
    ), row=2, col=1)
    fig.add_hline(y=1, line_dash="dash", line_color="rgba(128,128,128,0.4)", row=2, col=1)

    fig.update_layout(
        **_LAYOUT,
        title=f"Rolling {window}-Day Metrics",
        height=420,
        showlegend=False,
    )
    return fig
