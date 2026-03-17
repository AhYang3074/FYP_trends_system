from flask import Flask, render_template, request
from modules.data_collector import fetch_multi_seed
from modules.trend_engine import aggregate_topics, calculate_final_scores
from modules.news_validation import validate_topics
from utils.config import DEFAULT_CATEGORY, DEFAULT_DATE_RANGE, CATEGORY_SEEDS

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORY_SEEDS)


@app.route("/search")
def search():
    category = str(request.args.get("category", DEFAULT_CATEGORY))
    date = request.args.get("date", DEFAULT_DATE_RANGE)

    cat_info = CATEGORY_SEEDS.get(category, CATEGORY_SEEDS[DEFAULT_CATEGORY])
    seeds = cat_info["seeds"]
    cat_name = cat_info["name"]

    all_raw = fetch_multi_seed(seeds, category, date)

    aggregated = aggregate_topics(all_raw, cat_name, seeds)

    topic_names = list(aggregated.keys())
    news_data = validate_topics(topic_names[:15])

    results = calculate_final_scores(aggregated, news_data)

    try:
        from modules.clustering import cluster_topics
        if len(results) >= 3:
            names = [r["topic"] for r in results]
            clusters = cluster_topics(names)
            for r in results:
                r["cluster"] = clusters.get(r["topic"], 0)
        else:
            for r in results:
                r["cluster"] = 0
    except ImportError:
        for r in results:
            r["cluster"] = 0

    top_results = results[:15]

    return render_template(
        "result.html",
        category_name=cat_name,
        results=top_results,
        total_seeds=len(seeds),
        total_topics=len(results),
    )


if __name__ == "__main__":
    app.run(debug=True)
