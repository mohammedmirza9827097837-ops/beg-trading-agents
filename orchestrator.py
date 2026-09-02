import sys
sys.path.append("agents")

from nifty_scalper import run_nifty_scalper

def run_pipeline():
    print("Running Nifty Scalper...")
    result = run_nifty_scalper()
    print("Result:", result)

if __name__ == "__main__":
    run_pipeline()
