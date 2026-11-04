# Buat fungsi Python untuk mengambil berita terbaru dari RSS feed Yahoo News Japan.

import feedparser

def get_latest_news():
    url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
    feed = feedparser.parse(url)
    return feed.entries

# Panggil fungsi get_latest_news(), lalu buat perulangan untuk mengambil 5 berita pertama, dan print judul serta link-nya ke layar

latest_news = get_latest_news()
for i in range(min(5, len(latest_news))):
    news_item = latest_news[i]
    print(f"Judul: {news_item.title}")
    print(f"Link: {news_item.link}\n")

