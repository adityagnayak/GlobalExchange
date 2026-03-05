"""
ui/styles.py
All CSS injected via st.markdown().  One source of truth for the visual theme.
"""

GLOBAL_CSS = """
<style>
  :root {
    --bg:           #07090f;
    --bg2:          #0d1117;
    --bg3:          #131820;
    --card:         #111722;
    --border:       rgba(255,255,255,0.07);
    --accent:       #00d4aa;
    --accent2:      #0091ff;
    --text:         #e8edf5;
    --muted:        #6b7a96;
    --danger:       #ff4d6d;
    --success:      #00d4aa;
    --gold:         #f5c842;
    --red:          #ef4444;
    --green:        #22c55e;
    --blue:         #60a5fa;
  }

  /* ── Streamlit chrome overrides ── */
  #MainMenu, footer, .stDeployButton { display: none !important; }
  .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; max-width: 1280px; }
  [data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid var(--border); }
  [data-testid="stSidebar"] label {
    font-size: 0.78rem !important; color: var(--muted) !important;
    font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em;
  }
  html, body, [class*="css"] {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
  }
  h1, h2, h3, h4 { color: var(--text) !important; }
  p, li { color: var(--muted) !important; }
  .stButton > button {
    font-family: inherit !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
  }

  /* ── Section titles ── */
  .section-title {
    font-size: 1.6rem; font-weight: 700; color: var(--text);
    margin-bottom: 0.3rem; letter-spacing: -0.02em;
  }
  .section-sub { font-size: 0.82rem; color: var(--muted); margin-bottom: 1.2rem; }
  .section-badge {
    font-size: 0.65rem; color: var(--muted); border: 1px solid var(--border);
    border-radius: 4px; padding: 2px 7px; letter-spacing: 0.8px;
    text-transform: uppercase; vertical-align: middle; margin-left: 8px;
    font-family: 'IBM Plex Mono', monospace;
  }
  .sub-header {
    font-size: 0.72rem; font-weight: 700; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.12em;
    border-bottom: 1px solid var(--border); padding-bottom: 6px; margin: 1.4rem 0 0.9rem;
  }

  /* ── Company cards (dark slate) ── */
  .company-cards-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1.2rem; }
  .company-card {
    flex: 1; min-width: 130px;
    background: #111d2a; border: 1px solid #1e3348;
    border-left: 3px solid #3b6ea5; border-radius: 6px;
    padding: 0.75rem 1rem;
  }
  .company-card-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; margin-bottom: 3px; font-weight: 600; }
  .company-card-value { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  /* ── Price cards ── */
  .price-cards-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1rem; }
  .price-card {
    flex: 1; min-width: 130px;
    background: #111d2a; border: 1px solid #1e3348;
    border-radius: 6px; padding: 0.75rem 1rem;
  }
  .price-card.highlight { border-left: 3px solid var(--gold); }
  .price-card-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: #94a3b8; margin-bottom: 3px; font-weight: 600; }
  .price-card-value { font-size: 1.3rem; font-weight: 700; color: #f1f5f9; line-height: 1.1; font-family: 'IBM Plex Mono', monospace; }

  /* ── Metric cards ── */
  .metric-card {
    background: var(--card); border: 1px solid var(--border);
    border-left: 3px solid var(--blue); border-radius: 6px;
    padding: 0.85rem 1rem; transition: box-shadow 0.2s;
  }
  .metric-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.35); }
  .metric-card.green { border-left-color: var(--green); }
  .metric-card.red   { border-left-color: var(--red); }
  .metric-card.blue  { border-left-color: var(--blue); }
  .metric-card.gold  { border-left-color: var(--gold); }
  .metric-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); margin-bottom: 3px; font-weight: 600; }
  .metric-value { font-size: 1.5rem; font-weight: 700; color: var(--text); line-height: 1.1; font-family: 'IBM Plex Mono', monospace; }
  .metric-tip   { font-size: 0.68rem; color: var(--muted); margin-top: 3px; line-height: 1.4; }

  /* ── Mode badge ── */
  .mode-badge { display: inline-block; padding: 2px 9px; border-radius: 3px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.8rem; }
  .mode-basic    { background: rgba(255,255,255,0.06); color: var(--muted); border: 1px solid var(--border); }
  .mode-advanced { background: rgba(0,145,255,0.12); color: var(--blue); border: 1px solid rgba(0,145,255,0.3); }

  /* ── VaR table ── */
  .var-wrapper { overflow-x: auto; border-radius: 6px; border: 1px solid var(--border); }
  .var-table { width: 100%; border-collapse: collapse; font-size: 0.84rem; min-width: 400px; }
  .var-table th { background: var(--bg3); color: var(--muted); padding: 9px 12px; text-align: center; border-bottom: 1px solid var(--border); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.68rem; }
  .var-table td { padding: 8px 12px; text-align: center; border-bottom: 1px solid var(--border); color: var(--text); }
  .var-table tr:last-child td { border-bottom: none; }
  .var-table tr:hover td { background: rgba(255,255,255,0.02); }

  /* ── Fund / perf tables ── */
  .fund-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  .fund-table tr { border-bottom: 1px solid var(--border); }
  .fund-table tr:last-child { border-bottom: none; }
  .fund-table td { padding: 7px 9px; color: var(--text); }
  .fund-table td:first-child { color: var(--muted); width: 55%; font-size: 0.78rem; }
  .fund-table td:last-child { font-weight: 700; text-align: right; font-family: 'IBM Plex Mono', monospace; }

  .perf-wrapper { overflow-x: auto; border-radius: 6px; border: 1px solid var(--border); }
  .perf-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; min-width: 480px; }
  .perf-table th { background: var(--bg3); color: var(--muted); padding: 9px 12px; text-align: left; border-bottom: 1px solid var(--border); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.68rem; }
  .perf-table td { padding: 8px 12px; border-bottom: 1px solid var(--border); color: var(--text); }
  .perf-table tr:last-child td { border-bottom: none; }
  .perf-table tr:hover td { background: rgba(255,255,255,0.02); }

  /* ── Warn / info boxes ── */
  .warn-box {
    background: rgba(245,166,35,0.07); border: 1px solid rgba(245,166,35,0.2);
    border-left: 3px solid var(--gold); border-radius: 6px;
    padding: 10px 14px; margin: 0.6rem 0; font-size: 0.82rem;
    color: rgba(245,166,35,0.9); line-height: 1.6;
  }
  .info-box {
    background: rgba(0,145,255,0.06); border: 1px solid rgba(0,145,255,0.18);
    border-left: 3px solid var(--blue); border-radius: 6px;
    padding: 10px 14px; margin: 0.6rem 0; font-size: 0.82rem;
    color: var(--blue); line-height: 1.6;
  }

  /* ── Fixed disclaimer ── */
  .disclaimer {
    position: fixed; bottom: 0; left: 0; right: 0;
    background: #cc0000; color: #fff; font-weight: 700;
    font-size: 0.72rem; padding: 6px 20px; text-align: center;
    z-index: 9999; letter-spacing: 0.02em;
  }

  /* ── Indices ticker bar ── */
  .indices-bar { display: flex; gap: 28px; overflow-x: auto; padding: 8px 0; white-space: nowrap; border-bottom: 1px solid var(--border); margin-bottom: 1.4rem; }
  .index-item { display: inline-flex; align-items: center; gap: 8px; flex-shrink: 0; font-size: 0.8rem; }
  .index-name { color: var(--muted); font-weight: 600; font-size: 0.72rem; }
  .index-val  { font-family: 'IBM Plex Mono', monospace; color: var(--text); }
  .idx-up   { color: #22c55e; font-family: 'IBM Plex Mono', monospace; }
  .idx-down { color: #ef4444; font-family: 'IBM Plex Mono', monospace; }

  /* ── Stock card grid ── */
  .stock-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px,1fr)); gap: 12px; }
  .stock-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; transition: border-color 0.2s; cursor: default; }
  .stock-card:hover { border-color: rgba(0,212,170,0.3); }
  .stock-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }
  .stock-ticker { font-family: 'IBM Plex Mono', monospace; font-size: 0.9rem; font-weight: 600; color: var(--text); }
  .stock-exchange { font-size: 0.65rem; color: var(--muted); margin-top: 2px; }
  .s-up   { color: #22c55e; font-family: 'IBM Plex Mono', monospace; font-size: 0.85rem; }
  .s-down { color: #ef4444; font-family: 'IBM Plex Mono', monospace; font-size: 0.85rem; }
  .stock-name { font-size: 0.75rem; color: var(--muted); margin-bottom: 10px; }
  .stock-tag { display: inline-block; background: rgba(255,255,255,0.04); border: 1px solid var(--border); border-radius: 3px; padding: 2px 6px; font-size: 0.65rem; color: var(--muted); margin-right: 4px; }
  .score-row { display: flex; align-items: center; gap: 8px; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--border); }
  .score-label { font-size: 0.65rem; color: var(--muted); }
  .score-bar { flex: 1; height: 3px; background: var(--bg); border-radius: 2px; overflow: hidden; }
  .score-fill { height: 100%; border-radius: 2px; background: linear-gradient(90deg, var(--accent2), var(--accent)); }
  .score-num  { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: var(--accent); font-weight: 600; }

  /* ── ETF / beat tables ── */
  .data-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  .data-table th { background: var(--bg3); color: var(--muted); padding: 9px 12px; text-align: left; border-bottom: 1px solid var(--border); font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; font-size: 0.65rem; white-space: nowrap; }
  .data-table td { padding: 9px 12px; border-bottom: 1px solid var(--border); color: var(--text); white-space: nowrap; }
  .data-table tr:last-child td { border-bottom: none; }
  .data-table tr:hover td { background: rgba(255,255,255,0.025); }
  .t-mono { font-family: 'IBM Plex Mono', monospace; }
  .t-muted { color: var(--muted); }
  .t-up   { color: #22c55e; font-family: 'IBM Plex Mono', monospace; }
  .t-down { color: #ef4444; font-family: 'IBM Plex Mono', monospace; }
  .badge { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 0.68rem; font-weight: 600; }
  .b-green { background: rgba(0,212,170,0.1);  color: #00d4aa; }
  .b-blue  { background: rgba(0,145,255,0.1);  color: #0091ff; }
  .b-red   { background: rgba(255,77,109,0.1); color: #ff4d6d; }
  .b-gold  { background: rgba(245,200,66,0.1); color: #f5c842; }
  .alpha-pill { display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; font-family: 'IBM Plex Mono', monospace; }
  .ap-pos { background: rgba(0,212,170,0.1); color: #00d4aa; border: 1px solid rgba(0,212,170,0.25); }
  .ap-neg { background: rgba(255,77,109,0.1); color: #ff4d6d; border: 1px solid rgba(255,77,109,0.25); }
  .stars { color: #f5c842; }

  /* ── News cards ── */
  .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap: 12px; }
  .news-card { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; }
  .news-region { font-size: 0.65rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 7px; }
  .news-title   { font-size: 0.84rem; font-weight: 600; color: var(--text); line-height: 1.45; margin-bottom: 7px; }
  .news-summary { font-size: 0.75rem; color: var(--muted); line-height: 1.55; margin-bottom: 10px; }
  .news-meta    { display: flex; justify-content: space-between; align-items: center; }
  .news-time    { font-size: 0.68rem; color: var(--muted); font-family: 'IBM Plex Mono', monospace; }

  /* ── AI chat ── */
  .ai-bubble { background: var(--bg3); border: 1px solid var(--border); border-radius: 10px 10px 10px 0; padding: 12px 16px; font-size: 0.85rem; line-height: 1.65; color: var(--text); margin-bottom: 12px; }
  .user-bubble { background: rgba(0,212,170,0.08); border: 1px solid rgba(0,212,170,0.15); border-radius: 10px 10px 0 10px; padding: 12px 16px; font-size: 0.85rem; line-height: 1.65; color: var(--text); margin-bottom: 12px; }

  /* ── Hero ── */
  .hero-stat-val { font-family: 'IBM Plex Mono', monospace; font-size: 1.6rem; font-weight: 600; color: var(--text); display: block; }
  .hero-stat-label { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.5px; }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 5px; height: 5px; }
  ::-webkit-scrollbar-track { background: var(--bg); }
  ::-webkit-scrollbar-thumb { background: #2a3347; border-radius: 3px; }
</style>
"""


def inject() -> None:
    """Call this once at the top of every page to apply the theme."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
