import sys
import time
sys.path.append("agents")

from data_agent import fetch_data, fetch_india_vix
from analysis_agent import analyze
from risk_agent import risk_check
from decision_agent import get_final_decision
from execution_agent import get_smart_session, place_order
from notifier_agent import notify
from nifty_scalper import run_nifty_scalper

CAPITAL = 100000

STOCKS = [
    {"symbol": "ICICIBANK.NS", "trading_symbol": "ICICIBANK-EQ", "token": "4963"},
    {"symbol": "MARUTI.NS", "trading_symbol": "MARUTI-EQ", "token": "10999"},
    {"symbol": "BEL.NS", "trading_symbol": "BEL-EQ", "token": "383"},
    {"symbol": "TVSMOTOR.NS", "trading_symbol": "TVSMOTOR-EQ", "token": "8479"},
    {"symbol": "PAYTM.NS", "trading_symbol": "PAYTM-EQ", "token": "6705"},
    {"symbol": "SUNPHARMA.NS", "trading_symbol": "SUNPHARMA-EQ", "token": "3351"},
    {"symbol": "MARICO.NS", "trading_symbol": "MARICO-EQ", "token": "4067"},
    {"symbol": "DIXON.NS", "trading_symbol": "DIXON-EQ", "token": "21690"},
    {"symbol": "POLYCAB.NS", "trading_symbol": "POLYCAB-EQ", "token": "9590"},
    {"symbol": "ASTRAL.NS", "trading_symbol": "ASTRAL-EQ", "token": "14418"},
    {"symbol": "SBICARD.NS", "trading_symbol": "SBICARD-EQ", "token": "17971"},
    {"symbol": "AUROPHARMA.NS", "trading_symbol": "AUROPHARMA-EQ", "token": "275"},
    {"symbol": "IDEA.NS", "trading_symbol": "IDEA-EQ", "token": "14366"},
    {"symbol": "M&M.NS", "trading_symbol": "M&M-EQ", "token": "2031"},
    {"symbol": "CAMS.NS", "trading_symbol": "CAMS-EQ", "token": "342"},
    {"symbol": "MCX.NS", "trading_symbol": "MCX-EQ", "token": "31181"},
    {"symbol": "INDHOTEL.NS", "trading_symbol": "INDHOTEL-EQ", "token": "1512"},
    {"symbol": "BAJAJ-AUTO.NS", "trading_symbol": "BAJAJ-AUTO-EQ", "token": "16669"},
]

def run_for_stock(stock, vix, smart_api):
    print(f"\n===== {stock['symbol']} =====")
    df = fetch_data(stock["symbol"])
    signal_data = analyze(df)
    risk_data = risk_check(CAPITAL, signal_data, vix)
    decision = get_final_decision(signal_data, risk_data, vix)

    print(f"Signal: {signal_data['signal']} | RSI: {signal_data['rsi']}")
    print(f"Decision: {decision}")

    executed = False
    if "EXECUTE" in decision.upper() and risk_data["approved"]:
        executed = True
        if smart_api:
            place_order(smart_api, stock["token"], stock["trading_symbol"],
                        risk_data["size"], side=signal_data["signal"], paper_mode=True)
        notify(f"[{stock['symbol']}] EXECUTE: {signal_data['signal']} | "
               f"RSI {signal_data['rsi']} | {decision}")
    else:
        print("Skipping execution.")

    return executed

def run_nifty():
    print("\n===== NIFTY SCALPER =====")
    result = run_nifty_scalper()
    if result:
        msg = (f"NIFTY SIGNAL: {result['signal']}\n"
               f"Entry: {result['entry']}\n"
               f"Target: {result['target']}\n"
               f"Stop Loss: {result['stop_loss']}\n"
               f"(Manual execution needed for options)")
        print(msg)
        notify(msg)

def run_pipeline():
    print("Fetching India VIX (ek baar sabke liye)...")
    vix = fetch_india_vix()
    print("VIX:", vix)

    run_nifty()

    smart_api = get_smart_session()

    executed_count = 0
    for stock in STOCKS:
        try:
            if run_for_stock(stock, vix, smart_api):
                executed_count += 1
        except Exception as e:
            print(f"Error with {stock['symbol']}: {e}")
        time.sleep(2)

    print("\nAll stocks processed!")

    notify(f"BEG Bot run complete. {len(STOCKS)} stocks scanned, "
           f"{executed_count} EXECUTE signal(s), VIX: {vix}")

if __name__ == "__main__":
    run_pipeline()
