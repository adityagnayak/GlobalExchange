"""
ui/market_data.py

Static curated market data for the GlobalIQ market intelligence sections.
Separating this from logic makes it trivial to swap in a live data feed later.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class StockEntry:
    ticker:   str
    name:     str
    exchange: str
    price:    str
    chg:      str
    up:       bool
    sector:   str    # tech | finance | health | energy | consumer
    region:   str    # us | eu | asia | em
    mkt_cap:  str
    pe:       str
    ai_score: int


@dataclass
class ETFEntry:
    rank:    int
    name:    str
    ticker:  str
    cat:     str
    aum:     str
    ret_1y:  str
    cagr_3y: str
    cagr_5y: str
    stars:   str
    expense: str


@dataclass
class BeatEntry:
    rank:   int
    name:   str
    region: str
    cagr:   str
    sp500:  str
    alpha:  str
    beats:  bool
    risk:   str


@dataclass
class NewsEntry:
    region:    str
    color:     str
    title:     str
    summary:   str
    time_ago:  str
    sentiment: str   # Bullish | Bearish | Neutral
    sent_cls:  str   # b-green | b-red | b-blue


# ── Stocks ─────────────────────────────────────────────────────────────────────
STOCKS: list[StockEntry] = [
    StockEntry("NVDA",     "NVIDIA Corporation",      "NASDAQ", "$874.20",     "+3.42%", True,  "tech",     "us",   "$2.1T",    "58x",  94),
    StockEntry("MSFT",     "Microsoft Corporation",   "NASDAQ", "$412.55",     "+0.87%", True,  "tech",     "us",   "$3.1T",    "35x",  91),
    StockEntry("AMZN",     "Amazon.com Inc.",         "NASDAQ", "$205.80",     "+1.24%", True,  "tech",     "us",   "$2.2T",    "42x",  89),
    StockEntry("GOOGL",    "Alphabet Inc.",           "NASDAQ", "$178.40",     "+0.56%", True,  "tech",     "us",   "$2.2T",    "26x",  87),
    StockEntry("META",     "Meta Platforms Inc.",     "NASDAQ", "$556.30",     "+2.11%", True,  "tech",     "us",   "$1.4T",    "29x",  88),
    StockEntry("ASML",     "ASML Holding NV",         "AMS",    "€812.40",     "+1.68%", True,  "tech",     "eu",   "€317B",    "34x",  90),
    StockEntry("SAP",      "SAP SE",                  "FWB",    "€233.80",     "+0.44%", True,  "tech",     "eu",   "€285B",    "32x",  82),
    StockEntry("NOVO-B",   "Novo Nordisk A/S",        "CPH",    "kr 680.50",   "-0.32%", False, "health",   "eu",   "kr 1.5T",  "28x",  85),
    StockEntry("LVMH",     "LVMH Moët Hennessy",     "EPA",    "€685.20",     "-0.18%", False, "consumer", "eu",   "€342B",    "22x",  80),
    StockEntry("TSM",      "Taiwan Semiconductor",    "TSE",    "NT$1,024",    "+2.88%", True,  "tech",     "asia", "NT$26.6T", "22x",  93),
    StockEntry("7203.T",   "Toyota Motor Corp.",      "TSE",    "¥3,284",      "+0.78%", True,  "consumer", "asia", "¥53T",     "9x",   78),
    StockEntry("005930",   "Samsung Electronics",     "KRX",    "₩74,200",     "+1.34%", True,  "tech",     "asia", "₩443T",    "18x",  81),
    StockEntry("RELIANCE.NS", "Reliance Industries",  "NSE",    "₹2,987",      "+0.92%", True,  "energy",   "em",   "₹20.2T",   "27x",  79),
    StockEntry("VALE3",    "Vale S.A.",               "B3",     "R$61.40",     "-0.55%", False, "energy",   "em",   "R$271B",   "6x",   72),
    StockEntry("JPM",      "JPMorgan Chase & Co.",    "NYSE",   "$234.70",     "+0.63%", True,  "finance",  "us",   "$672B",    "13x",  83),
    StockEntry("HSBA.L",   "HSBC Holdings plc",       "LSE",    "£7.84",       "+0.28%", True,  "finance",  "eu",   "£153B",    "9x",   74),
    StockEntry("LLY",      "Eli Lilly and Company",   "NYSE",   "$873.20",     "+1.48%", True,  "health",   "us",   "$830B",    "62x",  86),
    StockEntry("PFE",      "Pfizer Inc.",             "NYSE",   "$27.44",      "-0.72%", False, "health",   "us",   "$155B",    "11x",  68),
]

# ── ETFs ───────────────────────────────────────────────────────────────────────
ETFS: list[ETFEntry] = [
    ETFEntry(1, "Invesco QQQ Trust",          "QQQ",  "US Equity",       "$290B", "+26.4%", "+17.2%", "+22.8%", "★★★★★", "0.20%"),
    ETFEntry(2, "Vanguard S&P 500 ETF",       "VOO",  "US Equity",       "$480B", "+24.1%", "+14.6%", "+18.2%", "★★★★★", "0.03%"),
    ETFEntry(3, "iShares MSCI World ETF",     "URTH", "International",   "$4.2B", "+20.8%", "+12.4%", "+16.3%", "★★★★☆", "0.24%"),
    ETFEntry(4, "ARK Innovation ETF",         "ARKK", "Thematic",        "$6.8B", "+38.2%", "+8.4%",  "+14.9%", "★★★☆☆", "0.75%"),
    ETFEntry(5, "Vanguard Emerging Markets",  "VWO",  "Emerging Markets","$112B", "+14.6%", "+9.2%",  "+11.8%", "★★★★☆", "0.08%"),
    ETFEntry(6, "iShares Core MSCI Europe",   "IEUR", "International",   "$7.4B", "+18.2%", "+10.8%", "+13.4%", "★★★★☆", "0.09%"),
    ETFEntry(7, "SPDR Gold Shares",           "GLD",  "Commodities",     "$64B",  "+28.4%", "+11.6%", "+12.8%", "★★★★☆", "0.40%"),
    ETFEntry(8, "Vanguard Total Bond Market", "BND",  "Fixed Income",    "$316B", "+5.2%",  "+1.4%",  "+2.8%",  "★★★☆☆", "0.03%"),
]

# ── Beat S&P 500 ───────────────────────────────────────────────────────────────
BEAT_INDEX: list[BeatEntry] = [
    BeatEntry(1, "Invesco QQQ Trust",            "🇺🇸 US",       "22.8%", "14.8%", "+8.0%", True,  "Medium"),
    BeatEntry(2, "Vanguard S&P 500 ETF",         "🇺🇸 US",       "18.2%", "14.8%", "+3.4%", True,  "Low"),
    BeatEntry(3, "Mirae Asset Semiconductors",   "🌏 Asia",      "21.4%", "14.8%", "+6.6%", True,  "High"),
    BeatEntry(4, "iShares Core MSCI Europe",     "🇪🇺 Europe",   "13.4%", "14.8%", "-1.4%", False, "Low-Med"),
    BeatEntry(5, "ARK Innovation ETF",           "🇺🇸 US",       "14.9%", "14.8%", "+0.1%", True,  "Very High"),
    BeatEntry(6, "Vanguard Emerging Markets",    "🌍 Emerging",  "11.8%", "14.8%", "-3.0%", False, "High"),
    BeatEntry(7, "Nifty 50 Index Fund (India)",  "🇮🇳 India",    "16.8%", "14.8%", "+2.0%", True,  "Medium"),
    BeatEntry(8, "SPDR Gold Shares",             "🌐 Global",    "12.8%", "14.8%", "-2.0%", False, "Low-Med"),
]

# ── News ───────────────────────────────────────────────────────────────────────
NEWS: list[NewsEntry] = [
    NewsEntry(
        "🇺🇸 United States", "#00d4aa",
        "Fed holds rates steady amid mixed signals on inflation outlook",
        "Federal Reserve officials voted unanimously to maintain the benchmark rate, signalling patience as services inflation remains sticky. Markets rallied 0.7%.",
        "2h ago", "Neutral", "b-blue",
    ),
    NewsEntry(
        "🇪🇺 Europe", "#0091ff",
        "ECB signals possible rate cut in Q2 as Eurozone growth stalls",
        "ECB President hinted at policy easing following weaker PMI data. The euro weakened 0.4% against the dollar.",
        "4h ago", "Bearish", "b-red",
    ),
    NewsEntry(
        "🌏 Asia Pacific", "#f5c842",
        "China's export data beats forecasts; tech sector surges 3%",
        "China reported better-than-expected February export figures, boosting sentiment in Hong Kong and mainland markets. HSTECH led gains.",
        "6h ago", "Bullish", "b-green",
    ),
    NewsEntry(
        "🇺🇸 United States", "#00d4aa",
        "NVIDIA surpasses $2.1T market cap amid AI chip demand surge",
        "NVDA shares reached a new all-time high as enterprise AI spending accelerates. Analysts raised price targets citing data centre demand.",
        "8h ago", "Bullish", "b-green",
    ),
    NewsEntry(
        "🌍 Emerging Markets", "#f5a623",
        "Brazil's central bank raises rates; real weakens against dollar",
        "Banco Central do Brasil hiked rates by 25bps. BRL slipped and Ibovespa fell 0.6% on growth concerns.",
        "10h ago", "Bearish", "b-red",
    ),
    NewsEntry(
        "🇬🇧 United Kingdom", "#0091ff",
        "UK CPI falls to 2.8%; BoE rate cut expectations rise",
        "Britain's inflation gauge hit a multi-year low, raising bets on a Bank of England cut in May. FTSE 100 climbed 0.5%.",
        "12h ago", "Bullish", "b-green",
    ),
]

# ── World indices (static fallback — live data fetched in app.py via yfinance) ──
INDICES_FALLBACK: list[dict] = [
    {"name": "S&P 500",   "val": "5,842.47", "chg": "+0.68%", "up": True},
    {"name": "NASDAQ",    "val": "18,284.62","chg": "+1.04%", "up": True},
    {"name": "DOW",       "val": "43,128.36","chg": "-0.12%", "up": False},
    {"name": "FTSE 100",  "val": "8,624.90", "chg": "+0.34%", "up": True},
    {"name": "DAX",       "val": "22,541.88","chg": "+0.51%", "up": True},
    {"name": "NIKKEI",    "val": "37,892.15","chg": "+1.22%", "up": True},
    {"name": "HANG SENG", "val": "22,118.76","chg": "+2.14%", "up": True},
    {"name": "SENSEX",    "val": "74,882.10","chg": "+0.89%", "up": True},
]
