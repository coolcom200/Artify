from time import sleep

from requests import get, ConnectionError

from api.database.database_elasticsearch import ElasticsearchDatabase

TIME_SLEEP = 2


def check_connection(host, port):
    try:
        response = get("http://{}:{}/_cluster/health".format(host, port))
    except ConnectionError:
        return False
    if not response.ok:
        return False
    json_status = response.json()
    return json_status["status"] != "red"


def init_elasticsearch_indices(db: ElasticsearchDatabase):
    while not check_connection(db.host, db.port):
        sleep(TIME_SLEEP)
    db.init_db()
