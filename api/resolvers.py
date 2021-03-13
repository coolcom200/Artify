from functools import wraps

from ariadne import QueryType, MutationType
from flask import session, g
from graphql import GraphQLError
from werkzeug.security import check_password_hash, generate_password_hash

from models import FileWithPath

query = QueryType()
mutation = MutationType()


def log_user_in(user_id):
    session.clear()
    session["user_id"] = user_id


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user" not in g or g.user is None:
            raise GraphQLError("Authentication Error")
        return fn(*args, **kwargs)

    return wrapper


@query.field("search")
def resolve_search(_, info, searchQuery=None, minPrice=None, maxPrice=None):
    database = info.context["database"]
    result = database.get_products(searchQuery, minPrice, maxPrice)
    tmp = [product.__dict__ for product in result]
    return tmp


@query.field("me")
@login_required
def resolve_me(obj, info):
    if "user" not in g or g.user is None:
        return None
    else:
        return g.user.__dict__


@mutation.field("login")
def resolve_login(_, info, input):
    error = None
    email = input["email"]
    password = input["password"]
    database = info.context["database"]

    user = database.get_user_by_email(email)
    if user is None:
        error = "Incorrect username."
    elif not check_password_hash(user.password_hash, password):
        error = "Incorrect password."

    if error is None:
        log_user_in(user.uid)

    return {"error": error}


@mutation.field("register")
def resolve_register(_, info, input):
    email = input["email"]
    password = input["password"]
    name = input["name"]
    database = info.context["database"]

    user = database.get_user_by_email(email)
    error = None
    if not email:
        error = "Email is required."
    elif not password:
        error = "Password is required."
    elif not name:
        error = "Name is required."
    elif user is not None:
        error = "User already exists"

    if error is None:
        user_id = database.create_user(email, name,
                                       generate_password_hash(password))
        log_user_in(user_id)

    return {"error": error}


@mutation.field("createProduct")
@login_required
def resolve_create_product(_, info, input):
    database = info.context["database"]
    image_manager = info.context["image_manager"]

    title = input["product_name"]
    price = input["price"]
    vis = input["is_visible"]
    desc = input["description"]
    files = input["files"]

    list_image_details = []
    for file in files:
        if "image" in file.mimetype:
            file_path = image_manager.save_image(file)
            list_image_details.append(FileWithPath(file.filename, file_path))
        else:
            raise GraphQLError("Files must be images")

    result = database.create_product_details(session["user_id"], title, desc,
                                             vis, price, list_image_details)
    return result.__dict__


@mutation.field("logout")
@login_required
def resolve_logout(_, info):
    session.clear()
    return {}
