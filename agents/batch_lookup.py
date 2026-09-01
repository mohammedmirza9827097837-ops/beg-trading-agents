import sys
sys.path.append("agents")
from token_lookup import find_token

STOCK_NAMES = [
    "ATHERENERG", "BALRAMCHIN", "ICICIBANK", "ASHOKA", "LENSKART",
    "GROWW", "NORTHARC", "SHIPROCKET", "MCX", "OLAELEC",
    "FMGOETZE", "NIACL", "MANALIPETC", "IDEA", "M&M",
    "DHOOTTRANS", "MOREPENLAB", "TMCV", "OFSS", "MARUTI",
    "PCJEWELLER", "TEJASNET", "BEL", "TARIL", "DIFFNKG",
    "SUNSHINE", "TVSMOTOR", "PAYTM", "SAGILITY", "BAJAJ-AUTO",
    "AUROPHARMA", "RATNAVEER", "SBICARD", "ASTRAL", "POLYCAB",
    "SUNPHARMA", "BAJAJHIND", "SBIFUNDS", "ECLERX", "VENKEYS",
    "DIXON", "AZAD", "WELCORP", "VINCOFE", "CAMS",
    "TDPOWERSYS", "SHILPAMED", "URBANCO", "MARICO", "INDHOTEL"
]

print("STOCKS = [")
for name in STOCK_NAMES:
    results = find_token(name)
    exact_match = None
    for r in results:
        if r["symbol"] == f"{name}-EQ":
            exact_match = r
            break
    if exact_match:
        print(f'    {{"symbol": "{name}.NS", "trading_symbol": "{exact_match["symbol"]}", "token": "{exact_match["token"]}"}},')
    else:
        print(f'    # NOT FOUND: {name} -- check manually')
print("]")
