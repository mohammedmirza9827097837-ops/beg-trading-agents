import feedparser
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from notifier_agent import notify

FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/marketreports.xml",
]

def get_top_news(limit=5):
    headlines = []
    for feed_url in FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            print("Feed status:", feed_url, "entries found:", len(feed.entries))
            for entry in feed.entries[:limit]:
                headlines.append(entry.title)
        except Exception as e:
            print("Feed error:", feed_url, e)
    return headlines[:limit]

def send_news_update():
    headlines = get_top_news()
    if not headlines:
        print("No news fetched.")
        return

    msg = "MARKET NEWS UPDATE\n\n"
    for i, h in enumerate(headlines, 1):
        msg += str(i) + ". " + h + "\n"

    result = notify(msg)
    print("Telegram response:", result)

if __name__ == "__main__":
    send_news_update()
