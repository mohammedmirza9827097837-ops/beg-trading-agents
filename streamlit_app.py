import streamlit as st
import json
import os

st.set_page_config(page_title="BEG Trading Agents", layout="centered")

st.title("BEG Trading Agents — Live Team View")

STATUS_FILE = "status.json"
CHART_FILE = "dashboard_chart.png"

if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        status = json.load(f)
else:
    status = {}

agent_status = status.get("agent_status", "unknown")
signal = status.get("signal", "NONE")

st.caption("Last updated: " + status.get("updated_at", "Waiting for first run..."))
st.divider()

agents = [
    {
        "name": "Data Agent",
        "desc": "Fetches live Nifty price data every run",
        "active": True,
        "detail": "Nifty Close: " + str(status.get("nifty_close", status.get("entry", "-")))
    },
    {
        "name": "Analysis Agent",
        "desc": "Calculates EMA5/EMA13 crossover + volume",
        "active": True,
        "detail": "EMA Fast: " + str(status.get("ema_fast", "-")) + " | EMA Slow: " + str(status.get("ema_slow", "-"))
    },
    {
        "name": "Signal Agent",
        "desc": "Decides BUY CALL / BUY PUT / wait",
        "active": agent_status == "signal_sent",
        "detail": "Current signal: " + signal
    },
    {
        "name": "Chart Agent",
        "desc": "Draws candlestick chart with entry/target/SL",
        "active": os.path.exists(CHART_FILE),
        "detail": "Chart ready" if os.path.exists(CHART_FILE) else "No chart yet"
    },
    {
        "name": "Notifier Agent",
        "desc": "Sends alerts to Telegram",
        "active": agent_status == "signal_sent",
        "detail": "Sent" if agent_status == "signal_sent" else "Idle (no signal to send)"
    },
    {
        "name": "News Agent",
        "desc": "Sends market news headlines every run",
        "active": True,
        "detail": "Runs every scheduled cycle"
    },
]

for agent in agents:
    icon = "🟢" if agent["active"] else "⚪"
    with st.container(border=True):
        col1, col2 = st.columns([1, 5])
        col1.markdown("### " + icon)
        col2.markdown("**" + agent["name"] + "**")
        col2.caption(agent["desc"])
        col2.write(agent["detail"])

st.divider()

if agent_status == "signal_sent":
    st.success("LATEST SIGNAL: " + signal)
    col1, col2, col3 = st.columns(3)
    col1.metric("Entry", status.get("entry", "-"))
    col2.metric("Target", status.get("target", "-"))
    col3.metric("Stop Loss", status.get("stop_loss", "-"))
elif agent_status == "outside_window":
    st.warning("Outside trading window (9:15 AM - 12:00 PM IST)")
elif agent_status == "already_traded":
    st.info("Already traded today")
else:
    st.info("Agents active, watching for a crossover signal")

if os.path.exists(CHART_FILE):
    st.subheader("Latest Chart")
    st.image(CHART_FILE)

st.divider()
st.caption("Auto-updates every time the GitHub Actions bot runs (every 15 min during market hours).")

if st.button("Refresh"):
    st.rerun()

st.markdown(
    "<meta http-equiv='refresh' content='30'>",
    unsafe_allow_html=True
)
