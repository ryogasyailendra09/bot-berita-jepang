import feedparser
from deep_translator import GoogleTranslator
from html import escape
from textblob import TextBlob


def get_latest_news():
    url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
    feed = feedparser.parse(url)
    return feed.entries


def analisis_sentimen(teks):
    teks_inggris = GoogleTranslator(source="ja", target="en").translate(teks)
    polarity = TextBlob(teks_inggris).sentiment.polarity

    if polarity > 0:
        return "Positif"
    if polarity < 0:
        return "Negatif"
    return "Netral"


def create_index_html(news_items):
    news_list = "\n".join(
        f'            <li><a href="{escape(news_item.link, quote=True)}">'
        f"{escape(news_item.title)}</a></li>"
        for news_item in news_items[:5]
    )

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Berita Terbaru Jepang</title>
</head>
<body>
    <h1>5 Berita Terbaru Jepang</h1>
    <ul>
{news_list}
    </ul>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as index_file:
        index_file.write(html_content)


latest_news = get_latest_news()
data_berita = []
for news_item in latest_news[:10]:
    data_berita.append(
        {
            "judul": news_item.title,
            "link": news_item.link,
            "sentimen": analisis_sentimen(news_item.title),
        }
    )

create_index_html(latest_news)
print("File index.html berhasil dibuat.")
