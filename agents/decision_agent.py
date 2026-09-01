import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_final_decision(signal_data, risk_data, vix):
    prompt = f"""
Tum ek disciplined NSE trading strategist ho jo risk-first sochta hai aur overtrading avoid karta hai.

Data:
- Signal: {signal_data['signal']}
- RSI: {signal_data['rsi']}
- Close: {signal_data['close']}, EMA20: {signal_data['ema20']}, VWAP: {signal_data['vwap']}
- India VIX: {vix}
- Risk Agent approved: {risk_data['approved']} ({risk_data['reason']})
- Position size suggested: {risk_data['size']}

Final decision do: EXECUTE ya SKIP, aur 2 line mein reasoning do.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    from data_agent import fetch_data, fetch_india_vix
    from analysis_agent import analyze
    from risk_agent import risk_check

    df = fetch_data()
    signal_data = analyze(df)
    vix = fetch_india_vix()
    risk_data = risk_check(capital=100000, signal_data=signal_data, india_vix=vix)

    decision = get_final_decision(signal_data, risk_data, vix)
    print("Signal:", signal_data)
    print("Risk:", risk_data)
    print("\nDecision:\n", decision)
