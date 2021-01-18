from flask import Flask, g, session, request, abort
from database_elasticsearch import ElasticsearchDatabase
from image_manager_local import ImageManagerLocal
from flask_restful import Resource, Api
import resources


app = Flask(__name__)
app.config.from_json("config.json")
api = Api(app)

database = ElasticsearchDatabase(app.config["DATABASE_HOST"], app.config["DATABASE_PORT"])
image_manager = ImageManagerLocal(app.config["FILE_SAVE_LOCATION"], app.config["FOLDER_DEPTH"])


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = database.get_user_by_id(user_id)



api.add_resource(resources.Register, "/register")
api.add_resource(resources.Login, "/login")
api.add_resource(resources.Logout, "/logout")
api.add_resource(resources.CreateProduct, "/create")
api.add_resource(resources.Search, "/search")
api.add_resource(resources.GetImage, "/image/<image_id>/")