import logging
from pymongo import *
import settings

def connect(dbname, host=settings.MONGO_ADDRESS, port=int(settings.MONGO_PORT)):
    logging.debug("connecting to magicbus mongodb")
    conn = connection.Connection(host, port)
    db = database.Database(conn, dbname)
    return db
