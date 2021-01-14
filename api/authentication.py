import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from api import database_interface
from api.user import User
from api.utils import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().get_user_by_id(user_id)


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        db = get_db()
        error = None
        user = db.get_user_by_email(email)

        if not email:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (user is not None):
            error = "User {0} is already registered.".format(email)

        if error is None:
            user_id = db.create_user(email, name, generate_password_hash(password))
            return log_user_in(user_id)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.get_user_by_email(email)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password_hash, password):
            error = "Incorrect password."

        if error is None:
            return log_user_in(user.uid)

    return render_template("auth/login.html")

def log_user_in(user_id):
    session.clear()
    session["user_id"] = user_id
    return redirect(url_for("product.create_product"))



@bp.route("/logout")
@login_required
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
