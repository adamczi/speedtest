import pg_simple
from config import host, port, database

pool = pg_simple.config_pool(host=host,
                           port=port,
                           database=database,
                           user="docker",
                           password="docker")

# logging in uses it's own initialization of PgSimple, this one is left for
# `stats`. `login` page needs to reestablish connection after logging out, but
# `stats` gets it only once and it doesn't get cleared in the meantime. `login`
# one does though, because it gets the session cleared?
db = pg_simple.PgSimple()
