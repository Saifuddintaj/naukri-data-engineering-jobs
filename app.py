from flask import Flask, render_template
import naukri_api

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/get_data')
def get_data():
    data = naukri_api.load(1)
    return data


if __name__ == '__main__':
    app.debug = True
    app.run()
