import sys
sys.path.append("agents")

from nifty_scalper import run_nifty_scalper
from news_agent import send_news_update

def run_pipeline():
    print("Running Nifty Scalper...")
    result = run_nifty_scalper()
    print("Result:", result)

    print("Sending news update...")
    send_news_update()

if __name__ == "__main__":
    run_pipeline()
