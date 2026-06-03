import os
import requests
import feedparser

TOKEN = os.getenv("8719789450:AAGMU1j5bQx6RdWiYco0GICQB5wVe8cbqQM")
CHAT_ID = os.getenv("Future Path News")

feeds = {
    "🟢 ગુજરાત": ("https://news.google.com/rss/search?q=ગુજરાત", 3),
    "🔵 ભારત": ("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en", 4),
    "🌍 વિશ્વ": ("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", 3)
}

message = "📰 Daily News Update\n\n"

for category, (url, count) in feeds.items():
    message += f"{category}\n\n"

    feed = feedparser.parse(url)

    for news in feed.entries[:count]:
        message += f"• {news.title}\n"
        message += f"{news.link}\n\n"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message[:4000]
    }
)

print("News Sent Successfully")
