import os
import time
from html import escape

import feedparser
import google.generativeai as genai


def get_latest_news():
    url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
    feed = feedparser.parse(url)
    return feed.entries


def analisis_berita(teks_jepang):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Variabel lingkungan GOOGLE_API_KEY belum diatur."
        )

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Baca judul berita Jepang ini, lalu balas HANYA dengan satu kata: "
        f"Positif, Negatif, atau Netral: {teks_jepang}"
    )
    hasil = model.generate_content(prompt).text.strip()

    if hasil in {"Positif", "Negatif", "Netral"}:
        return hasil
    raise ValueError(
        f"Respons model tidak valid: {hasil!r}. "
        "Respons harus Positif, Negatif, atau Netral."
    )


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


def main():
    latest_news = get_latest_news()
    berita_untuk_dianalisis = latest_news[:10]

    data_berita = []
    for news_item in berita_untuk_dianalisis:
        data_berita.append(
            {
                "judul": news_item.title,
                "link": news_item.link,
                "sentimen": analisis_berita(news_item.title),
            }
        )
        time.sleep(2)

    create_index_html(latest_news)
    print("File index.html berhasil dibuat.")


if __name__ == "__main__":
    main()
