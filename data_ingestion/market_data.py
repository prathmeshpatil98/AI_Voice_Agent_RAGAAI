import requests
import os

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
YF_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"

def fetch_market_data(symbol: str):
    av_url = (
        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}"
        f"&interval=5min&apikey={ALPHA_VANTAGE_API_KEY}"
    )
    av_data = requests.get(av_url).json()
    yf_data = requests.get(YF_QUOTE_URL, params={"symbols": symbol}).json()
    return {"alphavantage": av_data, "yahoo_finance": yf_data}
