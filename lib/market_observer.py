import datetime
import requests
import json
import sys
sys.path.insert(0, 'lib')
from utils import dprint,get_coin_symbol_list

def insert_current_coin_values(db):
    dprint("Adding current coin values to db")
    coin_symbol_list = get_coin_symbol_list(db)
    ticker_json = requests.get("https://api.coinmarketcap.com/v1/ticker/").text
    ticker = json.loads(ticker_json)
    for tick in ticker:
        if tick['symbol'] in coin_symbol_list:
            db.commit('INSERT INTO coin_history (coin_type_id,price) VALUES (%s,%s)',(tick['symbol'],tick['price_usd']))
