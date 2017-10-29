from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from api.catalog import Catalog
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)

api = Api(app)

# Host static page index.html 
# @app.route("/")
# def static_index():
#     return send_from_directory("static", "index.html")

@app.route('/')
@app.route('/index')
def index():
    # user = {'nickname': 'Miguel'}  # fake user
    api_host_ip = "34.210.54.118"
    return render_template('index.html',
                           title='Home',
                           api_host_ip=api_host_ip)

api.add_resource(Catalog, '/catalog', '/catalog/search')

if __name__ == '__main__':
    app.run(debug=True, port=8000, host="0.0.0.0")

