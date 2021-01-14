from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from api.utils import get_image_manager, get_db
from api.file_with_path import FileWithPath
from api.authentication import login_required

bp = Blueprint("product", __name__, url_prefix="/product")


@bp.route("/create_product", methods=("GET", "POST"))
@login_required
def create_product():
    if request.method == "POST":
        files = request.files.getlist("files")
        title = request.form['title']
        desc = request.form['description']
        price = request.form['price']

        if len(files) == 0:
            return redirect(request.url)
        
        list_image_details = []
        for file in files:
            file_path = get_image_manager().save_image(file)
            list_image_details.append(FileWithPath(file.filename, file_path))

        res = get_db().create_product_details(session['user_id'], title, desc, True, price, list_image_details)

    return render_template("product_page/create_product.html")