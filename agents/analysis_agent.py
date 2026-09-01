import pandas as pd
import numpy as np

def calculate_rsi(close, period=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ema(close, period):
    return close.ewm(span=period, adjust=False).mean()

def calculate_vwap(high, low, close, volume):
    typical_price = (high + low + close) / 3
    return (typical_price * volume).cumsum() / volume.cumsum()

def analyze(df):
    """Indicators calculate karke ek raw signal deta hai"""
    close = df["Close"]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
    high = df["High"]
    if hasattr(high, "columns"):
        high = high.iloc[:, 0]
    low = df["Low"]
    if hasattr(low, "columns"):
        low = low.iloc[:, 0]
    volume = df["Volume"]
    if hasattr(volume, "columns"):
        volume = volume.iloc[:, 0]

    rsi = calculate_rsi(close)
    ema20 = calculate_ema(close, 20)
    vwap = calculate_vwap(high, low, close, volume)

    latest_rsi = float(rsi.iloc[-1])
    latest_close = float(close.iloc[-1])
    latest_ema20 = float(ema20.iloc[-1])
    latest_vwap = float(vwap.iloc[-1])

    if latest_rsi < 30 and latest_close > latest_ema20:
        signal = "BUY"
    elif latest_rsi > 70 and latest_close < latest_ema20:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "signal": signal,
        "rsi": round(latest_rsi, 2),
        "close": round(latest_close, 2),
        "ema20": round(latest_ema20, 2),
        "vwap": round(latest_vwap, 2)
    }

if __name__ == "__main__":
    from data_agent import fetch_data
    df = fetch_data()
    result = analyze(df)
    print(result)
