import logging
from pymongo import *

def connect(dbname, host='localhost', port=27017):
    logging.debug("connecting to magicbus mongodb")
    conn = connection.Connection(host, port)
    db = database.Database(conn, dbname)
    return db
