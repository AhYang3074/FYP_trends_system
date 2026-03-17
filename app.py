from flask import Flask, render_template, request
from services import fetch_trends_data
from processor import TrendProcessor

app = Flask(__name__)
processor = TrendProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    category = request.args.get('category', 18) # 默认 18
    date = request.args.get('date', 'today 1-m') # 默认一个月
    
    # 1. 传参数给 service
    raw_data = fetch_trends_data(query, category, date)
    
    # 2. 处理数据
    processed_list = processor.process_results(raw_data)
    
    # 3. 渲染页面
    return render_template('results.html', query=query, results=processed_list)

if __name__ == '__main__':
    app.run(debug=True)