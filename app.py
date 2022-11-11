from flask import Flask, render_template, jsonify, request
import naukri_api

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        data = 'hello world'
    return jsonify({'data' : data})


@app.route('/get_data/<int:no_of_pages>', methods=['GET'])
def get_data(no_of_pages):
    data = naukri_api.load(no_of_pages)
    return data


if __name__ == '__main__':
    app.debug = True
    app.run()
