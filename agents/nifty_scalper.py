import os
import sys
import json
import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import yfinance as yf
import mplfinance as mpf

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from notifier_agent import notify_with_photo

IST = ZoneInfo("Asia/Kolkata")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "nifty_trade_state.json")
CHART_FILE = os.path.join(BASE_DIR, "nifty_chart.png")

TARGET_POINTS = 12
SL_POINTS = 4.5
START_TIME = datetime.time(9, 15)
END_TIME = datetime.time(12, 0)

def already_traded_today():
    if not os.path.exists(STATE_FILE):
        return False
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
    today = datetime.datetime.now(IST).date().isoformat()
    return state.get("last_trade_date") == today

def mark_traded_today(details):
    today = datetime.datetime.now(IST).date().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump({"last_trade_date": today, "details": details}, f)

def in_trading_window():
    now = datetime.datetime.now(IST).time()
    return START_TIME <= now <= END_TIME

def calculate_ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def make_chart(df, ema9, ema21, signal, entry, target, sl):
    plot_df = df.tail(60).copy()
    plot_df.columns = [c[0] if isinstance(c, tuple) else c for c in plot_df.columns]

    ema9_plot = ema9.tail(60)
    ema21_plot = ema21.tail(60)

    addplots = [
        mpf.make_addplot(ema9_plot, color="blue", width=1),
        mpf.make_addplot(ema21_plot, color="orange", width=1),
    ]

    hlines = dict(
        hlines=[entry, target, sl],
        colors=["green", "lime", "red"],
        linestyle="--",
        linewidths=1
    )

    mc = mpf.make_marketcolors(up="green", down="red", inherit=True)
    style = mpf.make_mpf_style(marketcolors=mc, gridstyle="--")

    mpf.plot(
        plot_df,
        type="candle",
        style=style,
        addplot=addplots,
        hlines=hlines,
        title="NIFTY Scalper Signal",
        ylabel="Price",
        savefig=dict(fname=CHART_FILE, dpi=120, bbox_inches="tight")
    )

def get_nifty_signal():
    df = yf.download("^NSEI", period="2d", interval="5m", progress=False)
    df.dropna(inplace=True)

    close = df["Close"]
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]
    volume = df["Volume"]
    if hasattr(volume, "columns"):
        volume = volume.iloc[:, 0]

    ema9 = calculate_ema(close, 5)
    ema21 = calculate_ema(close, 13)
    avg_volume = volume.rolling(window=20).mean()

    latest_close = float(close.iloc[-1])
    latest_ema9 = float(ema9.iloc[-1])
    latest_ema21 = float(ema21.iloc[-1])
    prev_ema9 = float(ema9.iloc[-2])
    prev_ema21 = float(ema21.iloc[-2])
    latest_volume = float(volume.iloc[-1])
    latest_avg_volume = float(avg_volume.iloc[-1])

    volume_confirmed = latest_volume > (latest_avg_volume * 0.8)

    signal = "NONE"
    if prev_ema9 <= prev_ema21 and latest_ema9 > latest_ema21 and volume_confirmed:
        signal = "BUY CALL"
    elif prev_ema9 >= prev_ema21 and latest_ema9 < latest_ema21 and volume_confirmed:
        signal = "BUY PUT"

    return {
        "signal": signal,
        "close": round(latest_close, 2),
        "df": df,
        "ema9_series": ema9,
        "ema21_series": ema21
    }

def run_nifty_scalper():
    if not in_trading_window():
        print("Outside trading window (9:15 AM - 12:00 PM IST). Skipping.")
        return None

    if already_traded_today():
        print("Already traded today. One trade per day limit reached.")
        return None

    data = get_nifty_signal()
    print("Nifty data:", {"signal": data["signal"], "close": data["close"]})

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

    make_chart(data["df"], data["ema9_series"], data["ema21_series"],
               data["signal"], entry, target, sl)

    result = {
        "signal": data["signal"],
        "entry": entry,
        "target": target,
        "stop_loss": sl
    }

    msg = "NIFTY SIGNAL: " + result["signal"] + "\n"
    msg += "Entry: " + str(result["entry"]) + "\n"
    msg += "Target: " + str(result["target"]) + "\n"
    msg += "Stop Loss: " + str(result["stop_loss"]) + "\n"
    msg += "(Manual execution needed for options)"
    notify_with_photo(msg, CHART_FILE)

    mark_traded_today(result)
    return result

if __name__ == "__main__":
    result = run_nifty_scalper()
    print("Result:", result)
