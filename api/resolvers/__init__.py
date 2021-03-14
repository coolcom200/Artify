from functools import wraps

from flask import session, g
from graphql import GraphQLError


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
