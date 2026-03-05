"""
ui/pages/market_pages.py

All GlobalIQ market intelligence pages:
  home, stocks, etfs, beat_index, analyst (AI chat), news
"""

from __future__ import annotations
import streamlit as st

from ui import components as C
from ui.market_data import STOCKS, ETFS, BEAT_INDEX, NEWS, StockEntry


# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════

def render_home() -> None:
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem 2rem;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.75rem;color:var(--accent);
                  border:1px solid rgba(0,212,170,0.25);border-radius:20px;
                  padding:5px 16px;display:inline-block;margin-bottom:1.4rem;letter-spacing:1px;">
        ◉ AI-Powered · Global Coverage · Institutional-Grade Analysis
      </div>
      <h1 style="font-family:'Georgia',serif;font-size:clamp(2rem,5vw,3.5rem);
                 font-weight:700;line-height:1.1;margin-bottom:1rem;">
        Smarter Investing Starts with<br>
        <em style="color:var(--accent)">Global Intelligence</em>
      </h1>
      <p style="color:var(--muted);font-size:1rem;max-width:540px;margin:0 auto 2rem;line-height:1.7;">
        AI-curated stock picks, global ETF rankings, institutional risk analytics,
        and real-time market intelligence — all in one platform.
      </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    stats = [
        ("50+",    "Exchanges"),
        ("12,000+","Stocks Tracked"),
        ("14+",    "Risk Metrics"),
        ("VaR",    "Risk Modelling"),
        ("Free",   "Always"),
    ]
    for col, (val, label) in zip(cols, stats):
        with col:
            st.markdown(
                f'<div style="text-align:center">'
                f'<span class="hero-stat-val">{val}</span>'
                f'<span class="hero-stat-label">{label}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        C.warn_box(
            "⚠️ <strong>Disclaimer:</strong> All data and AI analysis on GlobalIQ is for "
            "informational and educational purposes only. This is <strong>not</strong> investment advice. "
            "Please consult a licensed financial advisor before investing. "
            "Past performance is not indicative of future returns."
        ),
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# TOP STOCKS
# ══════════════════════════════════════════════════════════════════════════════

def render_stocks() -> None:
    st.markdown(
        C.section_header("AI-Curated Top Stocks", badge="March 2026",
                         sub="AI-scored picks across global markets · Updated weekly"),
        unsafe_allow_html=True,
    )

    # Region + sector filter
    REGIONS  = ["All", "🇺🇸 USA", "🇪🇺 Europe", "🌏 Asia", "🌍 Emerging"]
    REGION_MAP = {"🇺🇸 USA": "us", "🇪🇺 Europe": "eu", "🌏 Asia": "asia", "🌍 Emerging": "em"}
    SECTORS  = ["All", "Technology", "Finance", "Healthcare", "Energy", "Consumer"]
    SECTOR_MAP = {"Technology": "tech", "Finance": "finance", "Healthcare": "health", "Energy": "energy", "Consumer": "consumer"}

    col1, col2 = st.columns(2)
    with col1:
        region_sel = st.selectbox("Region", REGIONS, label_visibility="collapsed")
    with col2:
        sector_sel = st.selectbox("Sector", SECTORS, label_visibility="collapsed")

    region_key = REGION_MAP.get(region_sel)
    sector_key = SECTOR_MAP.get(sector_sel)

    filtered = [
        s for s in STOCKS
        if (region_key is None or s.region == region_key)
        and (sector_key is None or s.sector == sector_key)
    ]

    _render_stock_grid(filtered)


def _render_stock_grid(stocks: list[StockEntry]) -> None:
    """Render stocks 3 per row."""
    for i in range(0, len(stocks), 3):
        row = stocks[i: i + 3]
        cols = st.columns(3)
        for col, s in zip(cols, row):
            with col:
                chg_cls  = "s-up" if s.up else "s-down"
                st.markdown(f"""
                <div class="stock-card">
                  <div class="stock-top">
                    <div>
                      <div class="stock-ticker">{s.ticker}</div>
                      <div class="stock-exchange">{s.exchange}</div>
                    </div>
                    <div style="text-align:right">
                      <div class="{chg_cls}">{s.price}</div>
                      <div class="{chg_cls}" style="font-size:0.72rem">{s.chg}</div>
                    </div>
                  </div>
                  <div class="stock-name">{s.name}</div>
                  <div>
                    <span class="stock-tag">MCap: {s.mkt_cap}</span>
                    <span class="stock-tag">P/E: {s.pe}</span>
                    <span class="stock-tag">{s.sector.capitalize()}</span>
                  </div>
                  <div class="score-row">
                    <span class="score-label">AI Score</span>
                    <div class="score-bar"><div class="score-fill" style="width:{s.ai_score}%"></div></div>
                    <span class="score-num">{s.ai_score}/100</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL ETFs
# ══════════════════════════════════════════════════════════════════════════════

def render_etfs() -> None:
    st.markdown(
        C.section_header("Top Global ETFs", badge="5Y Performance",
                         sub="Risk-adjusted returns across global ETF universe · Ranked by 5Y CAGR"),
        unsafe_allow_html=True,
    )

    rows = ""
    for e in ETFS:
        r1y_cls = "t-up" if e.ret_1y.startswith("+") else "t-down"
        r3y_cls = "t-up" if e.cagr_3y.startswith("+") else "t-down"
        rows += f"""
        <tr>
          <td class="t-mono t-muted">{e.rank}</td>
          <td><strong>{e.name}</strong></td>
          <td class="t-mono">{e.ticker}</td>
          <td><span class="badge b-blue">{e.cat}</span></td>
          <td class="t-mono">{e.aum}</td>
          <td class="t-mono {r1y_cls}">{e.ret_1y}</td>
          <td class="t-mono {r3y_cls}">{e.cagr_3y}</td>
          <td class="t-mono t-up"><strong>{e.cagr_5y}</strong></td>
          <td class="stars">{e.stars}</td>
          <td class="t-mono t-muted">{e.expense}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;border-radius:10px;border:1px solid var(--border)">
      <table class="data-table">
        <thead><tr>
          <th>#</th><th>ETF Name</th><th>Ticker</th><th>Category</th>
          <th>AUM</th><th>1Y Return</th><th>3Y CAGR</th><th>5Y CAGR</th>
          <th>Rating</th><th>Expense Ratio</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# BEAT S&P 500
# ══════════════════════════════════════════════════════════════════════════════

def render_beat_index() -> None:
    st.markdown(
        C.section_header("Funds That Beat S&P 500", badge="AI Ranked",
                         sub="S&P 500 · 5Y CAGR: ~14.8%"),
        unsafe_allow_html=True,
    )
    st.markdown(
        C.info_box(
            "📊 Only funds that have <strong>consistently outperformed</strong> the S&P 500 across "
            "3Y and 5Y periods are shown. <strong>Alpha</strong> = excess return above S&P 500 "
            "5Y CAGR (14.8%). Multi-region comparison."
        ),
        unsafe_allow_html=True,
    )

    rows = ""
    for f in BEAT_INDEX:
        ap_cls   = "ap-pos" if f.beats else "ap-neg"
        beat_badge = '<span class="badge b-green">▲ Beats</span>' if f.beats else '<span class="badge b-red">▼ Lags</span>'
        rows += f"""
        <tr>
          <td class="t-mono t-muted">{f.rank}</td>
          <td><strong>{f.name}</strong></td>
          <td>{f.region}</td>
          <td class="t-mono t-up"><strong>{f.cagr}</strong></td>
          <td class="t-mono t-muted">{f.sp500}</td>
          <td><span class="alpha-pill {ap_cls}">{f.alpha}</span></td>
          <td>{beat_badge}</td>
          <td class="t-muted">{f.risk}</td>
        </tr>"""

    st.markdown(f"""
    <div style="overflow-x:auto;border-radius:10px;border:1px solid var(--border)">
      <table class="data-table">
        <thead><tr>
          <th>#</th><th>Fund / ETF</th><th>Region</th><th>5Y CAGR</th>
          <th>S&amp;P 5Y</th><th>Alpha</th><th>vs S&amp;P</th><th>Risk Grade</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# AI ANALYST
# ══════════════════════════════════════════════════════════════════════════════

def render_analyst() -> None:
    import anthropic

    st.markdown(
        C.section_header("AI Analyst", badge="Claude AI",
                         sub="Ask anything about global markets, stocks, ETFs, macro trends, or valuations"),
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:0.72rem;'
        'color:var(--muted);border:1px solid var(--border);border-radius:4px;'
        'padding:3px 10px;display:inline-block;margin-bottom:1.2rem;">'
        "🤖 Powered by Anthropic · claude-sonnet-4-6</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        topic = st.selectbox(
            "Topic",
            ["", "Stock Analysis", "ETF Comparison", "Market Outlook",
             "Sector Analysis", "DCF Valuation", "Portfolio Advice",
             "Macro Economics", "Currency & FX"],
            label_visibility="collapsed",
        )
    with col2:
        region = st.selectbox(
            "Region",
            ["All Regions", "North America", "Europe", "Asia Pacific",
             "Emerging Markets", "Latin America", "Middle East & Africa"],
            label_visibility="collapsed",
        )

    # Chat state
    if "analyst_history" not in st.session_state:
        st.session_state["analyst_history"] = []

    # Display history
    if not st.session_state["analyst_history"]:
        st.markdown(
            '<div class="ai-bubble">Hello! I\'m your GlobalIQ AI Analyst, powered by Claude. '
            "I can help you analyse stocks across any global market, compare ETFs, discuss macro trends, "
            "perform valuations, or give you a sector deep-dive. What would you like to explore today?</div>",
            unsafe_allow_html=True,
        )
    else:
        for msg in st.session_state["analyst_history"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("e.g. Analyse TSMC vs Samsung for a 5-year hold…")
    if user_input:
        st.session_state["analyst_history"].append({"role": "user", "content": user_input})
        st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)

        system = (
            "You are GlobalIQ's AI Analyst, a world-class global finance intelligence assistant "
            "powered by Claude. You have deep expertise in international equity markets, ETFs, macro "
            "economics, currencies, commodities, and multi-region investing.\n\n"
            "Provide sharp, insightful, data-driven analysis. Reference global context, give balanced "
            "bull/bear perspectives, mention key risks and catalysts. Be concise but substantive.\n"
            "Always end with: 'This is informational only, not investment advice.'"
            + (f"\nTopic focus: {topic}" if topic else "")
            + (f"\nRegion focus: {region}" if region != "All Regions" else "")
        )

        with st.spinner("Analysing global markets…"):
            try:
                client = anthropic.Anthropic()
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    system=system,
                    messages=st.session_state["analyst_history"],
                )
                reply = response.content[0].text
            except Exception as e:
                reply = f"⚠️ Error: {e}"

        st.session_state["analyst_history"].append({"role": "assistant", "content": reply})
        st.markdown(f'<div class="ai-bubble">{reply}</div>', unsafe_allow_html=True)

    if st.button("🗑️ Clear conversation"):
        st.session_state["analyst_history"] = []
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# NEWS
# ══════════════════════════════════════════════════════════════════════════════

def render_news() -> None:
    st.markdown(
        C.section_header("Global Market News", badge="Live",
                         sub="AI-summarised · March 2026"),
        unsafe_allow_html=True,
    )

    for i in range(0, len(NEWS), 3):
        row  = NEWS[i: i + 3]
        cols = st.columns(3)
        for col, n in zip(cols, row):
            with col:
                st.markdown(f"""
                <div class="news-card">
                  <div class="news-region" style="color:{n.color}">{n.region}</div>
                  <div class="news-title">{n.title}</div>
                  <div class="news-summary">{n.summary}</div>
                  <div class="news-meta">
                    <span class="news-time">{n.time_ago}</span>
                    <span class="badge {n.sent_cls}">{n.sentiment}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
