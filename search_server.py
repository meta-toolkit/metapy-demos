from flask import Flask, request
app = Flask(__name__, static_folder='static/search/', static_url_path='')
import json
import sys

from searcher import Searcher

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/search-api', methods=['POST'])
def search_api():
    return app.searcher.search(request.get_json())

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    app.searcher = Searcher(sys.argv[1])
    app.run(debug=True)
