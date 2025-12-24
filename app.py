from Flask import flask, request, jsonify
import requests
from summarizer import summarize_text
import os

app = Flask(__name__)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


@app.route("/news", methods=["GET"])
def get_news():
    category = request.args.get("category", "technology")
    country = request.args.get("country", "in")

    params = {
        "apiKey": NEWS_API_KEY,
        "category": category,
        "country": country,
        "pageSize": 5
    }

    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch news"}), 500

    articles = response.json().get("articles", [])
    summarized_news = []

    for article in articles:
        content = article.get("content") or article.get("description", "")
        summary = summarize_text(content)

        summarized_news.append({
            "title": article.get("title"),
            "source": article.get("source", {}).get("name"),
            "summary": summary,
            "url": article.get("url")
        })

    return jsonify({
        "category": category,
        "count": len(summarized_news),
        "articles": summarized_news
    })


if __name__ == "__main__":
    app.run(debug=True)
