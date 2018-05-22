import sys
sys.path.insert(0, 'lib')
from utils import dprint
import dbfunc
import market_observer

if __name__ == "__main__":
    dprint("BabaVanga Starting")
    dbfunc.setup_check() #script will halt if this errors out anywhere. probably
    with dbfunc.postgres() as db:

        market_observer.insert_current_coin_values(db)
