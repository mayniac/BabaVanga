import sys
sys.path.insert(0, 'lib')
from utils import dprint
import nlp_schema
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

class postgres(object):
    def __init__(self):
        dprint("Permanently connecting to postgres database Babavanga_Main")
        self._db_connection = psycopg2.connect("user=postgres dbname=babavanga_main")
        self._db_cur = self._db_connection.cursor()

    def __enter__(self):
        return self

    def query(self, query, params=''): # used only for retrieving data
        try:
            self._db_cur.execute(query,params)
        except Exception as error:
            dprint('Error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            result = self._db_cur.fetchall()
            return result

    def commit(self, query, params=''): #used only for comitting data to db
        try:
            result = self._db_cur.execute(query,params)
            self._db_connection.commit()
        except Exception as error:
            dprint('Error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result

    def __exit__(self, exc_type, exc_value, traceback):
        dprint("Closing postgres session")
        self._db_connection.close()




def setup_check(): #class postgres keeps connection open to specific db, this connects a layer above to check for existence of said db
    dprint("Temporarily connecting to postgres to check for BabaVanga_main")
    connection = psycopg2.connect("user = postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'babavanga_main')")
    exists_row = cursor.fetchone()
    exists = exists_row[0]

    if exists == False:
        dprint("No BabaVanga main database found, creating DB")
        cursor.execute("CREATE DATABASE babavanga_main")
        connection.close()
        db_setup()
    else:
        dprint("BabaVanga_Main found, moving on")
        connection.close()

def db_setup():
    commands = nlp_schema.schema
    with postgres() as db:
        dprint("Creating Main DB Tables - Ignore permanent connection message")
        for command in commands:
            #dprint(command)
            db.commit(command)
            time.sleep(1)
