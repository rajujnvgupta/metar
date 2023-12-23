
from redis import StrictRedis as Redis

def BaseCache(host='localhost', port=6379, db=0, password=None, socket_timeout=None):
    """ redis connection with credential """
    return Redis(host, port, db, password, socket_timeout)



