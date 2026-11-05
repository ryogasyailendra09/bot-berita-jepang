# Japanese News Sentiment Analyzer

Japanese News Sentiment Analyzer is a Flask web application that fetches Japanese news from an RSS feed and uses the Google Gemini API to analyze market sentiment in real time.

## Features

- Fetches the latest Japanese news from Yahoo! Japan News RSS.
- Analyzes the sentiment of up to five news headlines with Google Gemini.
- Displays each headline, source link, and sentiment in a Bootstrap dashboard.
- Handles temporary Gemini API failures with a clear fallback status.

## Tech Stack

- Python
- Flask
- Bootstrap 5
- Google GenAI API

## How It Works

1. Open the Flask application in a browser.
2. Enter a Gemini API key.
3. The application retrieves the latest Japanese news headlines.
4. Gemini classifies each headline as positive, negative, or neutral.
5. The results are displayed in a dashboard table.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

Then open `http://127.0.0.1:5000` in your browser.