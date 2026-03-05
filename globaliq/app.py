"""
app.py — GlobalIQ main entrypoint

Thin orchestration layer.  This file only:
  1. Configures Streamlit
  2. Injects CSS
  3. Renders the world-indices ticker bar
  4. Routes between pages via the sidebar nav

All logic lives in engine/ (math) or ui/ (visuals).
"""

import streamlit as st
import yfinance as yf

from ui.styles import inject
from ui import components as C
from ui.market_data import INDICES_FALLBACK
from engine.constants import WORLD_INDICES
from ui.pages.market_pages import (
    render_home,
    render_stocks,
    render_etfs,
    render_beat_index,
    render_analyst,
    render_news,
)
from ui.pages.analysis import render_page as render_analysis_page

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GlobalIQ — AI Finance Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Theme ─────────────────────────────────────────────────────────────────────
inject()

# ─── World indices ticker bar ─────────────────────────────────────────────────

@st.cache_data(ttl=300)   # refresh every 5 minutes
def _fetch_indices() -> list[dict]:
    """Fetch live closing prices for world indices via yfinance."""
    from engine.constants import WORLD_INDICES as _SYMS
    results = []
    for idx in _SYMS:
        try:
            t    = yf.Ticker(idx["symbol"])
            hist = t.history(period="2d")
            if len(hist) >= 2:
                prev  = hist["Close"].iloc[-2]
                last  = hist["Close"].iloc[-1]
                chg   = (last - prev) / prev * 100
                results.append({
                    "name": idx["name"],
                    "val":  f"{last:,.2f}",
                    "chg":  f"{chg:+.2f}%",
                    "up":   chg >= 0,
                })
            else:
                raise ValueError("insufficient history")
        except Exception:
            # fall back to static data
            fb = next((f for f in INDICES_FALLBACK if f["name"] == idx["name"]), None)
            if fb:
                results.append(fb)
    return results


def _render_indices_bar() -> None:
    indices = _fetch_indices()
    items = ""
    for idx in indices:
        chg_cls = "idx-up" if idx["up"] else "idx-down"
        items += (
            f'<div class="index-item">'
            f'<span class="index-name">{idx["name"]}</span>'
            f'<span class="index-val">{idx["val"]}</span>'
            f'<span class="{chg_cls}">{idx["chg"]}</span>'
            f"</div>"
        )
    st.markdown(f'<div class="indices-bar">{items}</div>', unsafe_allow_html=True)


# ─── Sidebar navigation ────────────────────────────────────────────────────────

PAGES = {
    "🏠 Overview":           "home",
    "📈 Top Stocks":         "stocks",
    "🌐 Global ETFs":        "etfs",
    "🏆 Beat S&P 500":       "beat",
    "📊 Security Analysis":  "analysis",
    "🤖 AI Analyst":         "analyst",
    "📰 Market News":        "news",
}

with st.sidebar:
    st.markdown(
        '<div style="font-family:\'IBM Plex Mono\',monospace;font-size:1rem;'
        'font-weight:500;color:#00d4aa;margin-bottom:1.2rem;">Global<span style="color:#e8edf5">IQ</span></div>',
        unsafe_allow_html=True,
    )
    selection = st.radio(
        "Navigate",
        list(PAGES.keys()),
        label_visibility="collapsed",
        index=0,
    )
    current_page = PAGES[selection]

# ─── Indices bar (always visible) ─────────────────────────────────────────────
_render_indices_bar()

# ─── Route to page ────────────────────────────────────────────────────────────
if current_page == "home":
    render_home()
elif current_page == "stocks":
    render_stocks()
elif current_page == "etfs":
    render_etfs()
elif current_page == "beat":
    render_beat_index()
elif current_page == "analysis":
    render_analysis_page()
elif current_page == "analyst":
    render_analyst()
elif current_page == "news":
    render_news()

# ─── Fixed disclaimer ─────────────────────────────────────────────────────────
st.markdown(C.disclaimer(), unsafe_allow_html=True)
