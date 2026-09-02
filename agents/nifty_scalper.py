import os
import json
import datetime
import pandas as pd
import yfinance as yf

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "nifty_trade_state.json")

TARGET_POINTS = 12    # 10-15 range ka beech
SL_POINTS = 4.5        # 4-5 range ka beech
START_TIME = datetime.time(9, 15)
END_TIME = datetime.time(12, 0)

def already_traded_today():
    if not os.path.exists(STATE_FILE):
        return False
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
    today = datetime.date.today().isoformat()
    return state.get("last_trade_date") == today

def mark_traded_today(details):
    today = datetime.date.today().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump({"last_trade_date": today, "details": details}, f)

def in_trading_window():
    now = datetime.datetime.now().time()
    return START_TIME <= now <= END_TIME

def calculate_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def get_nifty_signal():
    df = yf.download("^NSEI", period="2d", interval="5m", progress=False)
    df.dropna(inplace=True)

    close = df["Close"]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
    volume = df["Volume"]
    if hasattr(volume, "columns"):
        volume = volume.iloc[:, 0]

    ema9 = calculate_ema(close, 9)
    ema21 = calculate_ema(close, 21)
    avg_volume = volume.rolling(window=20).mean()

    latest_close = float(close.iloc[-1])
    latest_ema9 = float(ema9.iloc[-1])
    latest_ema21 = float(ema21.iloc[-1])
    prev_ema9 = float(ema9.iloc[-2])
    prev_ema21 = float(ema21.iloc[-2])
    latest_volume = float(volume.iloc[-1])
    latest_avg_volume = float(avg_volume.iloc[-1])

    volume_confirmed = latest_volume > latest_avg_volume

    signal = "NONE"
    if prev_ema9 <= prev_ema21 and latest_ema9 > latest_ema21 and volume_confirmed:
        signal = "BUY CALL"
    elif prev_ema9 >= prev_ema21 and latest_ema9 < latest_ema21 and volume_confirmed:
        signal = "BUY PUT"

    return {
        "signal": signal,
        "close": round(latest_close, 2),
        "ema9": round(latest_ema9, 2),
        "ema21": round(latest_ema21, 2),
        "volume_confirmed": volume_confirmed
    }

def run_nifty_scalper():
    if not in_trading_window():
        print("Outside trading window (9:15 AM - 12:00 PM). Skipping.")
        return None

    if already_traded_today():
        print("Already traded today. One trade per day limit reached.")
        return None

    data = get_nifty_signal()
    print("Nifty data:", data)

    if data["signal"] == "NONE":
        print("No clear EMA crossover signal right now.")
        return None

    entry = data["close"]
    if data["signal"] == "BUY CALL":
        target = round(entry + TARGET_POINTS, 2)
        sl = round(entry - SL_POINTS, 2)
    else:
        target = round(entry - TARGET_POINTS, 2)
        sl = round(entry + SL_POINTS, 2)

    result = {
        "signal": data["signal"],
        "entry": entry,
        "target": target,
        "stop_loss": sl
    }

    mark_traded_today(result)
    return result

if __name__ == "__main__":
    result = run_nifty_scalper()
    print("Result:", result)
