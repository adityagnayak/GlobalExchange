"""
ui/components.py

Reusable HTML component builders.
All functions return raw HTML strings — rendered via st.markdown(..., unsafe_allow_html=True).
"""

from __future__ import annotations
import numpy as np


def metric_card(label: str, value: str, tooltip: str = "", color: str = "") -> str:
    cls = f"metric-card {color}".strip()
    tip = f'<div class="metric-tip">{tooltip}</div>' if tooltip else ""
    return f"""
    <div class="{cls}">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      {tip}
    </div>"""


def color_class(val: float, positive_good: bool = True) -> str:
    """Return a CSS class based on value sign."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return ""
    if positive_good:
        return "green" if val > 0 else "red"
    return "red" if val > 0 else "green"


def company_cards(name: str, sector: str, industry: str, currency: str, exchange: str = "") -> str:
    items = [
        ("Company",  name),
        ("Sector",   sector),
        ("Industry", industry),
    ]
    if exchange:
        items.append(("Exchange", exchange))
    items.append(("Currency", currency))
    cards = "".join(
        f"""<div class="company-card">
              <div class="company-card-label">{label}</div>
              <div class="company-card-value" title="{val}">{val}</div>
            </div>"""
        for label, val in items
    )
    return f'<div class="company-cards-row">{cards}</div>'


def price_cards(
    sym: str,
    current: float | None,
    high_52: float | None,
    low_52: float | None,
    pct_from_high: float | None,
    market_cap: str = "",
) -> str:
    def _fmt(v):
        return f"{sym}{v:,.2f}" if v is not None else "N/A"

    pct_color = "#ef4444" if (pct_from_high is not None and pct_from_high < 0) else "#22c55e"
    pct_str   = f"{pct_from_high:+.2f}%" if pct_from_high is not None else "N/A"

    cards = f"""
    <div class="price-card">
      <div class="price-card-label">Current Price</div>
      <div class="price-card-value">{_fmt(current)}</div>
    </div>
    <div class="price-card">
      <div class="price-card-label">52-Week High</div>
      <div class="price-card-value">{_fmt(high_52)}</div>
    </div>
    <div class="price-card">
      <div class="price-card-label">52-Week Low</div>
      <div class="price-card-value">{_fmt(low_52)}</div>
    </div>
    <div class="price-card highlight">
      <div class="price-card-label">% From 52W High</div>
      <div class="price-card-value" style="color:{pct_color}">{pct_str}</div>
    </div>"""

    if market_cap:
        cards += f"""
    <div class="price-card">
      <div class="price-card-label">Market Cap</div>
      <div class="price-card-value" style="font-size:1rem">{market_cap}</div>
    </div>"""

    return f'<div class="price-cards-row">{cards}</div>'


def var_table(var_90, var_95, var_99) -> str:
    """Render the Value at Risk table."""
    def fv(v):
        return f"{v * 100:.3f}%" if v is not None and not np.isnan(v) else "N/A"

    rows = ""
    for conf, r in [("90%", var_90), ("95%", var_95), ("99%", var_99)]:
        rows += (
            f"<tr>"
            f"<td><strong>{conf}</strong></td>"
            f'<td style="color:#ef4444;font-weight:700">{fv(r.hist)}</td>'
            f'<td style="color:#f59e0b;font-weight:700">{fv(r.param)}</td>'
            f'<td style="color:#dc2626;font-weight:700">{fv(r.cvar)}</td>'
            f"</tr>"
        )
    return f"""
    <div class="var-wrapper">
      <table class="var-table">
        <thead>
          <tr>
            <th>Confidence</th>
            <th>Historical VaR</th>
            <th>Parametric VaR</th>
            <th>CVaR (Expected Shortfall)</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p style="font-size:0.72rem;color:var(--muted);margin-top:4px;">
      VaR = maximum expected daily loss at the given confidence level.
      CVaR (Expected Shortfall) = average loss when VaR is exceeded.
    </p>"""


def fund_table(pairs: list[tuple[str, str]]) -> str:
    rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in pairs)
    return f'<table class="fund-table">{rows}</table>'


def perf_table(rows: list, bench_name: str) -> str:
    headers = ["Period", "Return", bench_name, "Excess Return", "Volatility"]
    th = "".join(f"<th>{h}</th>" for h in headers)
    tbody = ""
    for r in rows:
        def cell(v, default="N/A"):
            if v is None or (isinstance(v, float) and np.isnan(v)):
                return f'<td style="color:var(--muted)">{default}</td>'
            pct = v * 100
            clr = "#22c55e" if pct > 0 else "#ef4444"
            return f'<td style="color:{clr};font-weight:700">{pct:.1f}%</td>'

        tbody += (
            f"<tr>"
            f'<td style="color:var(--muted)">{r.label}</td>'
            f"{cell(r.stock_return)}"
            f"{cell(r.bench_return)}"
            f"{cell(r.excess_return)}"
            f'<td class="t-mono">{r.volatility * 100:.1f}%</td>'
            f"</tr>"
        )
    return f"""
    <div class="perf-wrapper">
      <table class="perf-table">
        <thead><tr>{th}</tr></thead>
        <tbody>{tbody}</tbody>
      </table>
    </div>"""


def warn_box(html: str) -> str:
    return f'<div class="warn-box">{html}</div>'


def info_box(html: str) -> str:
    return f'<div class="info-box">{html}</div>'


def section_header(title: str, badge: str = "", sub: str = "") -> str:
    badge_html = f'<span class="section-badge">{badge}</span>' if badge else ""
    sub_html   = f'<div class="section-sub">{sub}</div>' if sub else ""
    return (
        f'<div class="section-title">{title} {badge_html}</div>'
        f"{sub_html}"
    )


def sub_header(title: str) -> str:
    return f'<div class="sub-header">{title}</div>'


def mode_badge(mode: str) -> str:
    cls = "mode-advanced" if mode == "Advanced" else "mode-basic"
    return f'<span class="mode-badge {cls}">{mode.upper()} MODE</span>'


def disclaimer() -> str:
    return (
        '<div class="disclaimer">'
        "⚠️ DISCLAIMER: GlobalIQ is an educational platform — not financial advice. "
        "Data may be delayed up to 30 minutes. Consult a registered financial advisor before investing."
        "</div>"
    )
