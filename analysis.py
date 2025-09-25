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
        data = ticker.history(period="1d")
        price = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2] if len(data) > 1 else price
        change = round(price - prev_close, 2)
        percent_change = round((change / prev_close) * 100, 2) if prev_close != 0 else 0
        name = ticker.info.get("shortName", symbol)
        return {
            "name": name,
            "price": price,
            "change": change,
            "percent_change": percent_change
        }
    except Exception as e:
        return {"error": str(e)}

# === Fetch top market news using BeautifulSoup ===
def get_market_news(count=5):
    url = "https://finance.yahoo.com/"
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        headlines = []
        for item in soup.select("h3 a")[:count]:
            title = item.get_text(strip=True)
            link = "https://finance.yahoo.com" + item['href']
            headlines.append({"title": title, "url": link})
        return headlines
    except Exception as e:
        return [{"title": f"Error: {e}", "url": ""}]

# === Pretty print ===
def pretty_row(title, symbol, sector, price, change, percent):
    return f"{title:<30} | {symbol:<6} | {sector:<22} | Price: {price:>8} | Change: {change:>8} | % Change: {percent:>8}"

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

    print("\n" + "="*70)
    print("{:^70}".format("TOP MARKET NEWS"))
    print("="*70)
    for article in get_market_news():
        print(f"\n{article['title']}".center(70, '-'))
        print(f"URL: {article['url']}")
        print("-"*70)
