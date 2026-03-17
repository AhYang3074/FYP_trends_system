from flask import Flask, render_template, request
from modules.data_collector import fetch_trends_data
from modules.trend_engine import aggregate_and_score

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    query = request.args.get('q')
    category = request.args.get('category', 18)
    date = request.args.get('date', 'today 1-m')

    raw_data = fetch_trends_data(query, category, date)
    processed_list = aggregate_and_score(raw_data)

    return render_template('result.html', query=query, results=processed_list)


if __name__ == '__main__':
    app.run(debug=True)
