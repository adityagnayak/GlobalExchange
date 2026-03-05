# GlobalIQ — AI-Powered Global Finance Intelligence

> Institutional-grade security analysis + global market intelligence, powered by Claude AI.

---

## Features

| Module | Description |
|--------|-------------|
| **World Indices Bar** | Live quotes for 12 global indices (auto-refreshed every 5 min) |
| **Top Stocks** | AI-curated picks across US, Europe, Asia & Emerging Markets |
| **Global ETFs** | 5Y CAGR-ranked ETF table with expense ratios |
| **Beat S&P 500** | Funds that outperformed the S&P 500 over 3Y & 5Y |
| **Security Analysis** | Full institutional dashboard — Beta, Alpha, Sharpe, Sortino, VaR, drawdown, distribution, rolling metrics, fundamentals |
| **AI Analyst** | Claude-powered chat for any global finance question |
| **Market News** | AI-summarised news with sentiment tagging |

---

## Architecture

```
globaliq/
├── app.py                       # Streamlit entrypoint — routing only
├── requirements.txt
├── .streamlit/config.toml       # Dark theme + server config
│
├── engine/                      # ── MATH LAYER (no Streamlit imports) ──
│   ├── __init__.py
│   ├── constants.py             # Benchmarks, currencies, exchange maps
│   ├── analyzer.py              # SecurityAnalyzer class + all metric calculations
│   └── charts.py                # Plotly chart factory functions
│
└── ui/                          # ── VISUAL LAYER ──
    ├── __init__.py
    ├── styles.py                # All CSS in one place (inject() helper)
    ├── components.py            # Reusable HTML component builders
    ├── market_data.py           # Static curated data (stocks, ETFs, news)
    └── pages/
        ├── __init__.py
        ├── analysis.py          # Security Analysis page (sidebar + render)
        └── market_pages.py      # Home, Stocks, ETFs, Beat, Analyst, News
```

**Separation principle:** `engine/` contains zero Streamlit imports. Every function in `engine/` can be unit-tested independently. The `ui/` layer calls `engine/` to get data and figures, then renders them.

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/globaliq.git
cd globaliq

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 5. Run
streamlit run app.py
```

---

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (make it public or connect your account).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Set:
   - **Repository:** `your-username/globaliq`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
5. Click **Deploy**. Done.

> The app will be live at `https://your-username-globaliq-app-xxxx.streamlit.app`

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Powers the AI Analyst and any AI-driven analysis |

On Streamlit Cloud set via **Settings → Secrets**. Locally use `export` or a `.env` file (never commit `.env`).

---

## Extending the Engine

All metric logic lives in `engine/analyzer.py`. To add a new metric:

```python
# engine/analyzer.py

def calculate_omega_ratio(self, threshold: float = 0.0) -> float:
    """Omega Ratio — probability-weighted ratio of gains vs losses."""
    if self.returns is None:
        return float("nan")
    excess = self.returns - threshold / TRADING_DAYS
    gains  = excess[excess > 0].sum()
    losses = abs(excess[excess < 0].sum())
    return float(gains / losses) if losses != 0 else float("nan")
```

Then surface it in `ui/pages/analysis.py` — no other files need to change.

---

## Adding a New Chart

```python
# engine/charts.py

def build_omega_chart(analyzer: SecurityAnalyzer) -> go.Figure:
    # ... pure Plotly, no st.* calls
    return fig
```

```python
# ui/pages/analysis.py  (inside render_analysis)
from engine.charts import build_omega_chart
st.plotly_chart(build_omega_chart(analyzer), use_container_width=True)
```

---

## Data Sources

- **Price & fundamentals:** [Yahoo Finance](https://finance.yahoo.com) via `yfinance`
- **AI analysis:** [Anthropic Claude](https://anthropic.com) (`claude-sonnet-4-6`)
- **Market data tables:** Curated in `ui/market_data.py` (swap for a live API as needed)

---

## Disclaimer

GlobalIQ is an **educational platform** only. Nothing on this platform constitutes investment advice.
Data may be delayed by up to 30 minutes. Always consult a licensed financial advisor before making investment decisions.

---

## License

MIT
