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


# insert into data (datetime, download, upload, ping, api, ip, provider) values ('2017-09-20 22:50:40', 31.29, 2.78, 22.371, '3', '109.173.147.181', 'INEA');
