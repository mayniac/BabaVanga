import sys
sys.path.insert(0, 'lib')
import time
from utils import dprint
import dbfunc
import market_observer
import article_scrapers
import nlp_chunker
import post_collector
import schedule
import settings




if __name__ == "__main__":
    dprint("BabaVanga Starting")
    dbfunc.setup_check() #script will halt if this errors out anywhere. probably
    with dbfunc.postgres() as db:

        #insert something to debug here
