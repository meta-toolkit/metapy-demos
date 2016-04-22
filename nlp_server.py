from flask import Flask, request
app = Flask(__name__, static_folder='static/nlp/', static_url_path='')
import json
import sys

from nlp import NLP

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/nlp-api', methods=['POST'])
def nlp_api():
    return app.nlp.run(request.get_json())

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)
    app.nlp = NLP(sys.argv[1])
    app.run(debug=True)
