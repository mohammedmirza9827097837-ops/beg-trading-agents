import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nifty_scalper import get_nifty_signal, make_chart, CHART_FILE
from notifier_agent import notify_with_photo

data = get_nifty_signal()
entry = data["close"]

fake_signal = "BUY CALL"
target = round(entry + 12, 2)
sl = round(entry - 4.5, 2)

make_chart(data["df"], data["ema9_series"], data["ema21_series"],
           fake_signal, entry, target, sl)

msg = "[TEST] NIFTY SIGNAL: " + fake_signal + "\n"
msg += "Entry: " + str(entry) + "\n"
msg += "Target: " + str(target) + "\n"
msg += "Stop Loss: " + str(sl) + "\n"
msg += "(Ye ek TEST hai, real signal nahi)"

result = notify_with_photo(msg, CHART_FILE)
print("Telegram result:", "OK" if result.get("ok") else result)
