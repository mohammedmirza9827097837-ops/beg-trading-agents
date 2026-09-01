import os
import pyotp
from SmartApi import SmartConnect
from dotenv import load_dotenv

load_dotenv()

def get_smart_session():
        api_key = os.getenv("SMARTAPI_API_KEY", "").strip()
    client_id = os.getenv("SMARTAPI_CLIENT_ID", "").strip()
    password = os.getenv("SMARTAPI_PASSWORD", "").strip()
    totp_secret = os.getenv("SMARTAPI_TOTP_SECRET", "").strip()

    smart_api = SmartConnect(api_key)
    totp = pyotp.TOTP(totp_secret).now()
    session = smart_api.generateSession(client_id, password, totp)

    if not session.get("status"):
        print("Login FAILED:", session)
        return None

    print("Login successful!")
    return smart_api

def place_order(smart_api, symbol_token, trading_symbol, qty, side="BUY", paper_mode=True):
    if paper_mode:
        print(f"[PAPER TRADE] {side} {qty} of {trading_symbol}")
        return {"status": "paper", "side": side, "qty": qty}

    order_params = {
        "variety": "NORMAL",
        "tradingsymbol": trading_symbol,
        "symboltoken": symbol_token,
        "transactiontype": side,
        "exchange": "NSE",
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "quantity": qty
    }
    order_id = smart_api.placeOrder(order_params)
    return order_id

if __name__ == "__main__":
    smart_api = get_smart_session()
    if smart_api:
        result = place_order(smart_api, "2885", "RELIANCE-EQ", 1, side="BUY", paper_mode=True)
        print(result)
