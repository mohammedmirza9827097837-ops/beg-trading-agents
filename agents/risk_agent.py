def risk_check(capital, signal_data, india_vix, max_risk_pct=2, vix_limit=22):
    """Position size decide karta hai, ya trade skip karne ka reason deta hai"""
    if india_vix > vix_limit:
        return {"approved": False, "reason": f"VIX too high ({india_vix})", "size": 0}

    if signal_data["signal"] == "HOLD":
        return {"approved": False, "reason": "No clear signal", "size": 0}

    risk_amount = capital * (max_risk_pct / 100)
    stop_loss_distance = signal_data["close"] * 0.01   # 1% SL assumption
    qty = int(risk_amount / stop_loss_distance)

    return {"approved": True, "reason": "OK", "size": qty}

if __name__ == "__main__":
    from data_agent import fetch_data, fetch_india_vix
    from analysis_agent import analyze

    df = fetch_data()
    signal_data = analyze(df)
    vix = fetch_india_vix()
    result = risk_check(capital=100000, signal_data=signal_data, india_vix=vix)
    print("Signal:", signal_data)
    print("Risk Check:", result)
