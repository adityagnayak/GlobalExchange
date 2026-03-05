"""
engine/constants.py
All lookup tables for exchanges, currencies, and benchmarks.
"""

BENCHMARKS: dict[str, dict[str, str]] = {
    "US": {
        "SPY":   "S&P 500 (SPY)",
        "QQQ":   "NASDAQ 100 (QQQ)",
        "DIA":   "Dow Jones (DIA)",
        "IWM":   "Russell 2000 (IWM)",
        "^GSPC": "S&P 500 Index",
        "^DJI":  "Dow Jones Index",
        "^IXIC": "NASDAQ Index",
    },
    "India": {
        "^NSEI":  "Nifty 50",
        "^BSESN": "BSE Sensex",
    },
    "Global": {
        "^FTSE":   "FTSE 100 (UK)",
        "^N225":   "Nikkei 225 (Japan)",
        "^HSI":    "Hang Seng (HK)",
        "^AXJO":   "ASX 200 (Australia)",
        "^GSPTSE": "TSX (Canada)",
        "^FCHI":   "CAC 40 (France)",
        "^GDAXI":  "DAX (Germany)",
        "^SSMI":   "SMI (Switzerland)",
    },
}

ALL_BENCHMARKS: dict[str, str] = {
    k: v for region in BENCHMARKS.values() for k, v in region.items()
}

BENCHMARK_NAMES: dict[str, str] = {
    "^FTSE":   "FTSE 100",
    "^NSEI":   "Nifty 50",
    "^BSESN":  "BSE Sensex",
    "^N225":   "Nikkei 225",
    "^HSI":    "Hang Seng",
    "^AXJO":   "ASX 200",
    "^GSPTSE": "TSX",
    "^FCHI":   "CAC 40",
    "^GDAXI":  "DAX",
    "^SSMI":   "SMI",
    "SPY":     "S&P 500 (SPY)",
    "QQQ":     "NASDAQ 100 (QQQ)",
    "DIA":     "Dow Jones (DIA)",
    "IWM":     "Russell 2000 (IWM)",
    "^GSPC":   "S&P 500",
    "^DJI":    "Dow Jones",
    "^IXIC":   "NASDAQ",
}

CURRENCY_MAP: dict[str, str] = {
    "USD": "$",   "EUR": "€",    "GBP": "£",   "GBp": "p",
    "JPY": "¥",   "CNY": "¥",    "INR": "₹",   "AUD": "A$",
    "CAD": "C$",  "CHF": "CHF ", "HKD": "HK$", "SGD": "S$",
    "KRW": "₩",   "BRL": "R$",   "RUB": "₽",   "ZAR": "R",
    "MXN": "MX$", "SEK": "kr",   "NOK": "kr",  "DKK": "kr",
    "PLN": "zł",  "TRY": "₺",    "THB": "฿",   "IDR": "Rp",
    "MYR": "RM",  "PHP": "₱",    "NZD": "NZ$", "ILS": "₪",
    "AED": "AED ","SAR": "SAR ",
}

# Ticker suffix → suggested benchmark
EXCHANGE_BENCHMARK: dict[str, str] = {
    ".L":  "^FTSE",
    ".NS": "^NSEI",
    ".BO": "^BSESN",
    ".T":  "^N225",
    ".HK": "^HSI",
    ".AX": "^AXJO",
    ".TO": "^GSPTSE",
    ".PA": "^FCHI",
    ".DE": "^GDAXI",
    ".SW": "^SSMI",
}

# Ticker suffix → native currency
EXCHANGE_CURRENCY: dict[str, str] = {
    ".L":  "GBp",
    ".NS": "INR",
    ".BO": "INR",
    ".T":  "JPY",
    ".HK": "HKD",
    ".AX": "AUD",
    ".TO": "CAD",
    ".PA": "EUR",
    ".DE": "EUR",
    ".SW": "CHF",
}

# Ticker suffix → full exchange name
EXCHANGE_NAME: dict[str, str] = {
    ".L":  "London Stock Exchange",
    ".NS": "NSE India",
    ".BO": "BSE India",
    ".T":  "Tokyo Stock Exchange",
    ".HK": "Hong Kong Stock Exchange",
    ".AX": "Australian Securities Exchange",
    ".TO": "Toronto Stock Exchange",
    ".PA": "Euronext Paris",
    ".DE": "Deutsche Börse",
    ".SW": "SIX Swiss Exchange",
}

# World indices shown in the ticker bar
WORLD_INDICES: list[dict] = [
    {"name": "S&P 500",   "symbol": "^GSPC"},
    {"name": "NASDAQ",    "symbol": "^IXIC"},
    {"name": "DOW",       "symbol": "^DJI"},
    {"name": "FTSE 100",  "symbol": "^FTSE"},
    {"name": "DAX",       "symbol": "^GDAXI"},
    {"name": "CAC 40",    "symbol": "^FCHI"},
    {"name": "NIKKEI",    "symbol": "^N225"},
    {"name": "HANG SENG", "symbol": "^HSI"},
    {"name": "ASX 200",   "symbol": "^AXJO"},
    {"name": "SENSEX",    "symbol": "^BSESN"},
    {"name": "IBOVESPA",  "symbol": "^BVSP"},
    {"name": "TSX",       "symbol": "^GSPTSE"},
]

RISK_FREE_RATE: float = 0.05   # 5% annual risk-free rate assumption
TRADING_DAYS:   int   = 252
