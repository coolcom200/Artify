from flask import current_app, g
from flask.cli import with_appcontext
import json
from .database_elasticsearch import ElasticsearchDatabase
from .database_interface import DatabaseInterface
from .image_manager_interface import ImageManagerInterface
from .image_manager_local import ImageManagerLocal

def get_db() -> DatabaseInterface:
    if 'db' not in g:
        g.db = ElasticsearchDatabase(current_app.config['DATABASE_HOST'],
                                     current_app.config['DATABASE_PORT'])

    return g.db

def get_image_manager() -> ImageManagerInterface:
    if 'image_manager' not in g:
        g.image_manager = ImageManagerLocal()

    return g.image_manager

