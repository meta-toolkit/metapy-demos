from flask import Flask, request
app = Flask(__name__, static_folder='static/nlp/', static_url_path='')
import json
import sys

import coffeescript, sass

from nlp import NLP

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/nlp-api', methods=['POST'])
def nlp_api():
    return app.nlp.run(request.get_json())

def compile_assets():
    static = app.static_folder

    with open("{}/javascript/index.js".format(static), 'w') as f:
        infile = "{}/coffeescript/index.coffee".format(static)
        js = coffeescript.compile_file(infile)
        f.write(js)

    with open('{}/css/tagged-text.css'.format(app.static_folder), 'w') as f:
        infile = "{}/scss/tagged-text.scss".format(static)
        css = sass.compile(filename=infile)
        f.write(css)

def server(config):
    print('Compiling assets...')
    compile_assets()

    print('Loading NLP models...')
    app.nlp = NLP(config)

    return app

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    server(sys.argv[1]).run(debug=True)
