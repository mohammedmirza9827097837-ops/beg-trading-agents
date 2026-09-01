import yfinance as yf
import pandas as pd

def fetch_data(symbol="RELIANCE.NS", period="5d", interval="15m"):
    """NSE stock ka recent OHLCV data laata hai"""
    df = yf.download(symbol, period=period, interval=interval, progress=False)
    df.dropna(inplace=True)
    return df

def fetch_india_vix():
    """India VIX current value laata hai risk filter ke liye"""
    vix = yf.download("^INDIAVIX", period="2d", interval="15m", progress=False)
    close = vix["Close"]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
    return float(close.iloc[-1])    

if __name__ == "__main__":
    df = fetch_data()
    print(df.tail())
    print("India VIX:", fetch_india_vix())

