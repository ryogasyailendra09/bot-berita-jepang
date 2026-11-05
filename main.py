import feedparser
import time
from google import genai
from flask import Flask, render_template, request


app = Flask(__name__)


def get_latest_news():
    url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
    feed = feedparser.parse(url)
    return feed.entries


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.form['api_key'].strip()
    client = genai.Client(api_key=api_key)

    latest_news = get_latest_news()[:5]
    data_berita = []

    for news_item in latest_news:
        judul = news_item.title
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash-lite',
                contents="Baca judul berita Jepang ini, balas HANYA dengan satu kata "
                "(Positif, Negatif, atau Netral): " + judul
            )
            sentimen = response.text.strip()
        except Exception:
            sentimen = "Gagal Diproses (Server Sibuk)"

        data_berita.append(
            {
                "judul": judul,
                "link": news_item.link,
                "sentimen": sentimen,
            }
        )
        time.sleep(2)

    return render_template("dashboard.html", berita=data_berita)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
