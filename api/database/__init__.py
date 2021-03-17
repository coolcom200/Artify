from time import sleep

from api.database.database_elasticsearch import ElasticsearchDatabase
from api.database.database_interface import DatabaseInterface
from api.database.database_postgres import PostgresDatabase
from api.database.init_elasticsearch_db import init_elasticsearch_indices
from api.models import sql_alchemy_db


def get_database(app) -> DatabaseInterface:
    if app.config["DATABASE_TYPE"].lower() == "elasticsearch":
        db = ElasticsearchDatabase(app.config["DATABASE_HOST"], app.config["DATABASE_PORT"])
        init_elasticsearch_indices(db)
        return db

    elif app.config["DATABASE_TYPE"].lower() == "postgresql":
        if "SQLALCHEMY_DATABASE_URI" not in app.config:
            app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://" \
                                                    f"{app.config['DATABASE_USER']}:" \
                                                    f"{app.config['DATABASE_PASSWORD']}@" \
                                                    f"{app.config['DATABASE_HOST']}:" \
                                                    f"{app.config['DATABASE_PORT']}/" \
                                                    f"{app.config['DATABASE_NAME']}"

            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

        # TODO: Change to wait for the database to be running before initializing the application
        sleep(10)
        sql_alchemy_db.init_app(app)
        sql_alchemy_db.create_all(app=app)
        return PostgresDatabase(sql_alchemy_db)
    else:
        raise Exception("Invalid Database Configuration")
