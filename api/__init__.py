from flask import Flask, g
from flask import request
from flask import render_template
from flask import send_file
from flask_cors import CORS
import json
import os
from .utils import get_db, get_image_manager
from . import authentication
from . import product


def create_app():

    app = Flask(__name__)
    CORS(app)
    app.config.from_json("../config.json")


    @app.route('/')
    def home():
        products = get_db().get_visible_products()
        return render_template("index.html", products=products['hits']['hits'])
    
    @app.route('/search', methods=["GET"])
    def search():
        price_min = request.args.get('price_min') 
        price_max = request.args.get('price_max')
        query = request.args.get('query')
        return get_db().search(query, price_min, price_max)

    @app.route('/image/<image_id>/')
    def get_image(image_id):
        return send_file(get_image_manager().get_image(image_id))

    app.register_blueprint(authentication.bp)
    app.register_blueprint(product.bp)
    app.add_url_rule("/", endpoint="index")
   
    return app
