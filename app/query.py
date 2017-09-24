from db import db
from werkzeug.contrib.cache import SimpleCache
from utils import dateToJS
import json

cache = SimpleCache()

# query the data and store it in the cache
def query(userkey):
    with db:
        statistics = db.fetchall('data',
                                 fields=['datetime','download','upload','ping',
                                         'ip', 'provider'],
                                 where=('api = %s', [userkey]),
                                 order=['datetime', 'ASC'])

    # Convert the dump to JS-friendly format
    ups = []
    downs = []
    pings = []

    for record in statistics:
        date = dateToJS(record[0]) # TO DO: timezone correction (currently GMT)
        down = float(record[1])
        up = float(record[2])
        pi = float(record[3])

        # Three different series of data for the graph purpose
        downs.append([date, down])
        ups.append([date, up])
        pings.append([date, pi])

    ip = statistics[len(statistics)-1][4]
    provider = statistics[len(statistics)-1][5]

    results = [downs, ups, pings, ["1234", provider]]

    # save to cache
    cache.set('results', results, 0)
