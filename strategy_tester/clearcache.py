import os
from diskcache import Cache

cwd = os.path.dirname(os.path.realpath(__file__))
cachedir = os.path.join(cwd, 'cache')
cache = Cache(cachedir)
cache.clear()
#del cache['get_portfolio']