import pg_simple
from config import host, port, database

pool = pg_simple.config_pool(host=host,
                           port=port,
                           database=database,
                           user="docker",
                           password="docker")

db = pg_simple.PgSimple()
