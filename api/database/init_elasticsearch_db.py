import json
from time import sleep

from requests import get, ConnectionError

from api.database.database_elasticsearch import ElasticsearchDatabase


def check_connection(host, port):
    try:
        response = get("http://{}:{}/_cluster/health".format(host, port))
    except ConnectionError:
        return False
    if not response.ok:
        return False
    json_status = response.json()
    return json_status["status"] != "red"


with open("../config.json") as config_file:
    sleep_time = 5
    config = json.load(config_file)
    host = "localhost"
    port = config["DATABASE_PORT"]
    while not check_connection(host, port):
        sleep(sleep_time)
        print("Waiting for database to start")

    es = ElasticsearchDatabase(host, port)
    es.init_db()
    print("Indices created")
