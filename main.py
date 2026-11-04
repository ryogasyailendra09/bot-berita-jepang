# Buat fungsi Python untuk mengambil berita terbaru dari RSS feed Yahoo News Japan.

def get_latest_news():
    url = "https://news.yahoo.co.jp/rss"
    feed = feedparser.parse(url)
    return feed.entries

