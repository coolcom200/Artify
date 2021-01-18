from functools import wraps
from flask_restful import Resource, abort
from flask import jsonify, g, request, session, send_file
from models import FileWithPath
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import api
import logging

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user" not in g or g.user is None:
            abort(403)
        return fn(*args, **kwargs)

    return wrapper

def get_or_none(key: any, from_dict: dict):
    if key in from_dict:
        return from_dict[key]
    else:
        return None

# ---------------------- #
#     Authentication     #
# ---------------------- #

def log_user_in(user_id):
    session.clear()
    session["user_id"] = user_id
    return "", 200

class Register(Resource):
    def post(self):
        data = request.json
        email = get_or_none("email", data)
        password = get_or_none("password", data)
        name =  get_or_none("name", data)
        db = api.database
        user = db.get_user_by_email(email)

        error = None
        if not email:
            error = "Email is required."
        elif not password:
            error = "Password is required."
        elif not name:
            error = "Name is required."
        elif (user is not None):
            error = "User already exists"

        if error is None:
            user_id = db.create_user(email, name, generate_password_hash(password))
            return log_user_in(user_id)

        return abort(400, error_message=error)

class Login(Resource):
    def post(self):
        data = request.json
        email = data["email"]
        password = data["password"]
        db = api.database
        error = None
        user = db.get_user_by_email(email)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password_hash, password):
            error = "Incorrect password."

        if error is None:
            return log_user_in(user.uid)

        abort(403)

class Logout(Resource):
    @login_required
    def get(self):
        session.clear()
        return "", 200

# ---------------------- #
#        Product         #
# ---------------------- #

class CreateProduct(Resource):
    @login_required
    def post(self):
        files = request.files.getlist("files")
        form_data = request.form
        title = get_or_none("title", form_data)
        desc = get_or_none("description", form_data)
        price = get_or_none("price", form_data)
        vis = get_or_none("visibility", form_data)
        error = None

        if title is None or title == "":
            error = "A title is required"
        elif desc is None or desc == "":
            error = "A description is required"
        elif price is None or price == "":
            error = "A price is required"
        elif vis is None or vis.lower() not in ["public", "private"]:
            error = "A visibility type is required"
        elif len(files) == 0:
            error = "At least one image is required"
        
        if error is not None:
            abort(400, error_message=error)
        
        is_visible = True if vis.lower() == "public" else False
        list_image_details = []
        for file in files:
            if "image" in file.mimetype:
                file_path = api.image_manager.save_image(file)
                list_image_details.append(FileWithPath(file.filename, file_path))
            else:
                abort(400, error_message="All files must be images")

        result = api.database.create_product_details(session["user_id"], title, desc, is_visible, price, list_image_details)
        return "", 200

class Search(Resource):
    def get(self):
        price_min = request.args.get("price_min")
        price_max = request.args.get("price_max")
        if price_min is not None:
            price_min = float(price_min)
        else:
            price_min = 0
        
        if price_max is not None:
            price_max = float(price_max)

        query = request.args.get("query")
        result = api.database.get_products(query, price_min, price_max)
        return jsonify([product.__dict__ for product in result])

class GetImage(Resource):
    def get(self, image_id):
        return send_file(api.image_manager.get_image(image_id))
