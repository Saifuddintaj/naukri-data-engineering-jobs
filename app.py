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

@app.route('/load_data/<int:no_of_pages>', methods=['GET'])
def load_data(no_of_pages):
  df = naukri_api.create_dataframe(no_of_pages)
  naukri_api.write_df_to_table(df)
  return print(f"loaded {no_of_pages} of naukri data to database")


if __name__ == '__main__':
  app.debug = True
  app.run()
