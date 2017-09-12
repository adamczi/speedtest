from db import db
from werkzeug.contrib.cache import SimpleCache
from utils import dateToJS

cache = SimpleCache()

# query the data and store it in the cache
def query(userkey):
    with db:
        statistics = db.fetchall('data',
                                 fields=['datetime','download','upload','ping'],
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

    results = [downs, ups, pings]

    # save to cache
    cache.set('results', results)
