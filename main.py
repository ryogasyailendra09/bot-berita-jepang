import feedparser
import random
import time
from google import genai
from flask import Flask, render_template, request
from types import SimpleNamespace


app = Flask(__name__)
SENTIMEN_VALID = ("Positif", "Negatif", "Netral")


def get_latest_news():
    url = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
    feed = feedparser.parse(url)
    return feed.entries


def buat_sentimen_dummy():
    time.sleep(0.5)
    return random.choice(SENTIMEN_VALID)


def lengkapi_berita(berita, jumlah=15):
    berita = list(berita[:jumlah])
    berita_dummy = [
        ("市場が回復基調、企業活動に明るい兆し", "https://example.com/dummy-1"),
        ("政府が新たな経済対策を発表", "https://example.com/dummy-2"),
        ("国内消費に変化、専門家が分析", "https://example.com/dummy-3"),
        ("観光業界、訪日客増加に期待", "https://example.com/dummy-4"),
        ("新技術の普及で産業構造が変化", "https://example.com/dummy-5"),
        ("企業の設備投資、慎重な動き続く", "https://example.com/dummy-6"),
        ("円相場の変動、輸入業者に影響", "https://example.com/dummy-7"),
        ("地域経済を支える新サービス開始", "https://example.com/dummy-8"),
        ("消費者の節約志向が広がる", "https://example.com/dummy-9"),
        ("専門家、今後の市場動向を注視", "https://example.com/dummy-10"),
        ("物流業界で効率化に向けた取り組み", "https://example.com/dummy-11"),
        ("再生可能エネルギーへの投資が拡大", "https://example.com/dummy-12"),
        ("企業と自治体が地域活性化で連携", "https://example.com/dummy-13"),
        ("新たな雇用創出に向けた計画を発表", "https://example.com/dummy-14"),
        ("市場関係者、安定した成長に期待", "https://example.com/dummy-15"),
    ]

    for judul, link in berita_dummy:
        if len(berita) >= jumlah:
            break
        berita.append(SimpleNamespace(title=judul, link=link))
    return berita


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    api_key = request.form.get("api_key", "").strip()
    gunakan_dummy = False
    try:
        client = genai.Client(api_key=api_key)
    except Exception:
        client = None
        gunakan_dummy = True

    latest_news = lengkapi_berita(get_latest_news(), jumlah=15)
    if len(latest_news) < 15:
        raise RuntimeError("Berita tidak dapat dilengkapi hingga 15 item.")
    gunakan_dummy = gunakan_dummy or any(
        item.link.startswith("https://example.com/dummy-")
        for item in latest_news
    )
    data_berita = []

    for news_item in latest_news:
        judul = news_item.title
        if gunakan_dummy or client is None:
            sentimen = buat_sentimen_dummy()
        else:
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash-lite',
                    contents=(
                        "Baca judul berita Jepang ini, balas HANYA dengan "
                        "satu kata (Positif, Negatif, atau Netral): " + judul
                    ),
                    config=genai.types.GenerateContentConfig(
                        max_output_tokens=5,
                        temperature=0.1
                    )
                )
                sentimen = response.text.strip()
                if sentimen not in SENTIMEN_VALID:
                    sentimen = buat_sentimen_dummy()
                    gunakan_dummy = True
            except Exception:
                sentimen = buat_sentimen_dummy()
                gunakan_dummy = True

        data_berita.append(
            {
                "judul": judul,
                "link": news_item.link,
                "sentimen": sentimen,
            }
        )
        time.sleep(2)

    total_berita = len(data_berita) or 1
    persen_positif = round(
        sum(item["sentimen"] == "Positif" for item in data_berita)
        / total_berita
        * 100
    )
    persen_negatif = round(
        sum(item["sentimen"] == "Negatif" for item in data_berita)
        / total_berita
        * 100
    )
    persen_netral = round(
        sum(item["sentimen"] == "Netral" for item in data_berita)
        / total_berita
        * 100
    )

    return render_template(
        "dashboard.html",
        berita=data_berita,
        persen_positif=persen_positif,
        persen_negatif=persen_negatif,
        persen_netral=persen_netral,
        mode_demo=gunakan_dummy,
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
