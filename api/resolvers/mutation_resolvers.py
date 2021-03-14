import re

from ariadne import MutationType
from flask import session
from graphql import GraphQLError
from werkzeug.security import check_password_hash, generate_password_hash

from api.models.common_models import FileWithPath, AuthResponse
from api.resolvers import log_user_in, login_required

mutation = MutationType()

EMAIL_REGEX = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"


@mutation.field("login")
def resolve_login(_, info, input):
    message = None
    email = input["email"]
    password = input["password"]
    database = info.context["database"]

    user = database.get_user_by_email(email)
    if user is None:
        message = "Incorrect username"
    elif not check_password_hash(user.passwordHash, password):
        message = "Incorrect password"

    if message is None:
        log_user_in(user.uid)
        message = "Success"

    return AuthResponse(message)


@mutation.field("register")
def resolve_register(_, info, input):
    email = input["email"]
    password = input["password"]
    name = input["name"]
    database = info.context["database"]

    user = database.get_user_by_email(email)
    message = None
    if not email:
        message = "Email is required"
    elif not re.search(EMAIL_REGEX, email):
        message = "Invalid email format"
    elif not password:
        message = "Password is required"
    elif not name:
        message = "Name is required"
    elif user is not None:
        message = "User already exists"

    if message is None:
        user_id = database.create_user(email, name, generate_password_hash(password))
        log_user_in(user_id)
        message = "Success"

    return AuthResponse(message)


@mutation.field("createProduct")
@login_required
def resolve_create_product(_, info, input):
    database = info.context["database"]
    image_manager = info.context["image_manager"]

    title = input["productName"]
    price = input["price"]
    vis = input["isVisible"]
    desc = input["description"]
    files = input["files"]

    if price < 0:
        raise GraphQLError("Invalid Price")

    list_image_details = []
    for file in files:
        if "image" in file.mimetype:
            file_path = image_manager.save_image(file)
            list_image_details.append(FileWithPath(file.filename, file_path))
        else:
            raise GraphQLError("Files must be images")

    result = database.create_product_details(session["user_id"], title, desc, vis, price,
                                             list_image_details)
    return result


@mutation.field("logout")
@login_required
def resolve_logout(_, info):
    session.clear()
    return AuthResponse("Success")
