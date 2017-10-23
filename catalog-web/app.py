from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from api.catalog import Catalog

app = Flask(__name__)

api = Api(app)

# Host static page index.html 
@app.route("/")
def static_index():
    return send_from_directory("static", "index.html")

api.add_resource(Catalog, '/catalog', '/catalog/search')

if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")