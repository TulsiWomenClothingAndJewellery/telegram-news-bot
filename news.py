import os
import requests
import feedparser

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SENT_FILE = "sent_news.txt"

# પહેલેથી મોકલેલી ન્યૂઝ લોડ કરો
sent_links = set()
if os.path.exists(SENT_FILE):
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        sent_links = set(line.strip() for line in f)

feeds = {
    "🟢 ગુજરાત": ("https://news.google.com/rss/search?q=ગુજરાત", 3),
    "🔵 ભારત": ("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en", 4),
    "🌍 વિશ્વ": ("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", 3)
}

message = "📰 Daily News Update\n\n"
new_links = []

for category, (url, count) in feeds.items():
    message += f"{category}\n\n"

    feed = feedparser.parse(url)

    added = 0
    for news in feed.entries:
        link = news.link

        if link in sent_links:
            continue

        message += f"• {news.title}\n"
        message += f"{link}\n\n"

        new_links.append(link)
        added += 1

        if added >= count:
            break

# જો નવી ન્યૂઝ હોય તો જ મોકલો
if new_links:
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message[:4000]
        }
    )

    print(response.text)

    with open(SENT_FILE, "a", encoding="utf-8") as f:
        for link in new_links:
            f.write(link + "\n")

else:
    print("No new news found.")
