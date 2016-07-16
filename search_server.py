from flask import Flask, request
app = Flask(__name__, static_folder='static/search/', static_url_path='')
import json
import sys

import coffeescript

from searcher import Searcher

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/search-api', methods=['POST'])
def search_api():
    return app.searcher.search(request.get_json())

def compile_assets():
    static = app.static_folder

    with open("{}/javascript/index.js".format(static), 'w') as f:
        infile = "{}/coffeescript/index.coffee".format(static)
        js = coffeescript.compile_file(infile)
        f.write(js)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    print('Compiling assets...')
    compile_assets()

    app.searcher = Searcher(sys.argv[1])
    app.run(debug=True)
