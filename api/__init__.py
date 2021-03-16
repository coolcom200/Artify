import json
from os import path

from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, gql, upload_scalar
from ariadne.constants import PLAYGROUND_HTML, DATA_TYPE_MULTIPART
from ariadne.exceptions import HttpBadRequestError
from ariadne.file_uploads import combine_multipart_data
from flask import Flask, g, session, request, jsonify, send_file, abort

from api.database import get_database
from api.image_manager import get_image_manager
from api.resolvers.mutation_resolvers import mutation
from api.resolvers.product_resolvers import product
from api.resolvers.query_resolvers import query
from api.resolvers.user_resolvers import user

HTTP_NOT_FOUND = 404
HTTP_SUCCESS = 200
HTTP_BAD_REQUEST = 400

app = Flask(__name__)
app.config.from_json("./config.json")

database = get_database(app)
image_manager = get_image_manager(app)

type_defs = load_schema_from_path("./schema.graphql")
gql(type_defs)  # gql verification
schema = make_executable_schema(type_defs, query, mutation, upload_scalar, product, user)


def handle_upload(form):
    """Based on Specification:
    https://github.com/jaydenseric/graphql-multipart-request-spec"""
    try:
        operations = json.loads(form["operations"])
    except (KeyError, ValueError):
        raise HttpBadRequestError("Request 'operations' multipart field is not a valid JSON")
    try:
        files_map = json.loads(form["map"])
    except (KeyError, ValueError):
        raise HttpBadRequestError("Request 'map' multipart field is not a valid JSON")

    return combine_multipart_data(operations, files_map, request.files)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, HTTP_SUCCESS


@app.route("/image/<image_id>/", methods=["GET"])
def get_image(image_id):
    image_path = image_manager.get_image(image_id)
    if not path.exists(image_path):
        abort(HTTP_NOT_FOUND)
    else:
        return send_file(image_path)


@app.route("/graphql", methods=["POST"])
def graphql_server():
    if DATA_TYPE_MULTIPART in request.content_type:
        data = handle_upload(request.form)
    else:
        data = request.get_json()

    success, result = graphql_sync(schema, data, debug=app.debug,
                                   context_value={"request": request, "database": database,
                                                  "image_manager": image_manager})
    status_code = HTTP_SUCCESS if success else HTTP_BAD_REQUEST
    return jsonify(result), status_code


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = database.get_user_by_id(user_id)
