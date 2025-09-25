import yfinance as yf
import requests
from bs4 import BeautifulSoup

# === Major indices ETFs ===
INDICES = {
    "S&P 500 ETF (SPY)": {"symbol": "SPY", "sector": "Broad Market", "exchange": "NYSE Arca"},
    "Dow Jones ETF (DIA)": {"symbol": "DIA", "sector": "Broad Market", "exchange": "NYSE Arca"},
    "Nasdaq 100 ETF (QQQ)": {"symbol": "QQQ", "sector": "Broad Market", "exchange": "NASDAQ"}
}

# === Sector ETFs ===
SECTOR_ETFS = {
    "Technology (XLK)": {"symbol": "XLK", "sector": "Technology", "exchange": "NYSE Arca"},
    "Healthcare (XLV)": {"symbol": "XLV", "sector": "Healthcare", "exchange": "NYSE Arca"},
    "Financials (XLF)": {"symbol": "XLF", "sector": "Financials", "exchange": "NYSE Arca"},
    "Consumer Discretionary (XLY)": {"symbol": "XLY", "sector": "Consumer Discretionary", "exchange": "NYSE Arca"},
    "Consumer Staples (XLP)": {"symbol": "XLP", "sector": "Consumer Staples", "exchange": "NYSE Arca"},
    "Energy (XLE)": {"symbol": "XLE", "sector": "Energy", "exchange": "NYSE Arca"},
    "Industrials (XLI)": {"symbol": "XLI", "sector": "Industrials", "exchange": "NYSE Arca"},
    "Materials (XLB)": {"symbol": "XLB", "sector": "Materials", "exchange": "NYSE Arca"},
    "Utilities (XLU)": {"symbol": "XLU", "sector": "Utilities", "exchange": "NYSE Arca"},
    "Real Estate (XLRE)": {"symbol": "XLRE", "sector": "Real Estate", "exchange": "NYSE Arca"}
}

# === Fetch quote using yfinance ===
def get_yf_quote(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")
        price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2] if len(data) > 1 else price
        change = price - prev_close
        percent_change = (change / prev_close) * 100 if prev_close != 0 else 0
        name = ticker.info.get("shortName", symbol)
        return {
            "name": name,
            "price": f"{price:.2f}",
            "change": f"{change:+.2f}",
            "percent_change": f"{percent_change:+.2f}"
        }
    except Exception as e:
        return {"error": str(e)}

# === Fetch top market news using BeautifulSoup ===
NEWS_API_KEY = "abf6235621af44c48e5ab549447e8e10"  # User's NewsAPI key

def get_market_news(count=5):
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize={count}&apiKey={NEWS_API_KEY}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("status") != "ok":
            return [{"title": f"NewsAPI error: {data.get('message', 'Unknown error')}", "url": ""}]
        headlines = []
        for article in data.get("articles", []):
            title = article.get("title", "No Title")
            link = article.get("url", "")
            headlines.append({"title": title, "url": link})
        return headlines
    except Exception as e:
        return [{"title": f"Error: {e}", "url": ""}]

# === Pretty print ===
def pretty_row(title, symbol, sector, price, change, percent):
    return f"{title:<30} | {symbol:<6} | {sector:<22} | Price: {price:>8} | Change: {change:>8} | % Change: {percent:>7}"

if __name__ == "__main__":
    print("="*120)
    print("{:^120}".format("MAJOR INDICES"))
    print("="*120)
    for name, info in INDICES.items():
        idx = get_yf_quote(info["symbol"])
        if "error" in idx:
            print(f"{name:<30} | {info['symbol']:<6} | {info['sector']:<22} | Error: {idx['error']}")
        else:
            print(pretty_row(idx["name"], info["symbol"], info["sector"], idx["price"], idx["change"], idx["percent_change"]))

    print("\n" + "="*120)
    print("{:^120}".format("SECTOR BREAKDOWN"))
    print("="*120)
    for name, info in SECTOR_ETFS.items():
        idx = get_yf_quote(info["symbol"])
        if "error" in idx:
            print(f"{name:<30} | {info['symbol']:<6} | {info['sector']:<22} | Error: {idx['error']}")
        else:
            print(pretty_row(idx["name"], info["symbol"], info["sector"], idx["price"], idx["change"], idx["percent_change"]))

    print("\n" + "="*120)
    print("{:^120}".format("TOP MARKET NEWS"))
    print("="*120)
    for article in get_market_news():
        print(f"\n{article['title']}".center(120, '-'))
        print(f"URL: {article['url']}")
        print("-"*120)
