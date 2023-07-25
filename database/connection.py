from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.auth import PlainTextAuthProvider

from ssl import SSLContext, PROTOCOL_TLSv1_2, CERT_REQUIRED
from configparser import ConfigParser

from database.config import SCYLLA_HOST, SCYLLA_PORT, REDIS_HOST, REDIS_PORT, REDIS_DB


def config(filename='database/db_config.ini', section=None):
    if section is None:
        raise Exception('section must be specified')
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect_cassandra():
    try:
        # ssl_context = SSLContext(PROTOCOL_TLSv1_2)
        # ssl_context.load_verify_locations('./sf-class2-root.crt')
        # ssl_context.verify_mode = CERT_REQUIRED
        # cfg = config(section='cassandra_auth')
        cfg = {
            'username': '',
            'password': '',
        }
        auth_provider = PlainTextAuthProvider(**cfg)
        cluster = Cluster(
            [
                *SCYLLA_HOST,
            ],
            port=SCYLLA_PORT,
            # ssl_context=ssl_context,
            control_connection_timeout=10,
            auth_provider=auth_provider
        )
        session = cluster.connect()
        return connection.register_connection('cluster1', session=session)

    except Exception as e:
        print(e.__str__())
        return {"success": False, "error": e.__str__()}


def get_redis_cfg():
    return {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': REDIS_DB
    }
