import sys
sys.path.append("agents")
from token_lookup import find_token

if len(sys.argv) < 2:
    print("Usage: py search_stock.py STOCKNAME")
    sys.exit()

name = sys.argv[1]
results = find_token(name)
for r in results[:10]:
    print(r["symbol"], "-", "Token:", r["token"])
