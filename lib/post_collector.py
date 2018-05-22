import requests
import xml.etree.ElementTree as ET
import sys
sys.path.insert(0, 'lib')
from utils import dprint,get_coin_name_list,get_coin_symbol_list,subject_analyser
import dbfunc
import market_observer

def enumerate_rss_feeds(db):
    rss_feed_tuple = db.query('SELECT source_id,source_rss_url FROM sources')
    return rss_feed_tuple

def post_updater(db):
    coin_name_list = get_coin_name_list(db)
    coin_symbol_list = get_coin_symbol_list(db)
    rss_feed_tuple = enumerate_rss_feeds(db)
    for rss_feed in rss_feed_tuple:

        source_id = rss_feed[0]
        source_rss_url = rss_feed[1]
        rss_feed_data= requests.get(source_rss_url).text
        root = ET.fromstring(rss_feed_data)

        for item in root.iter('item'):

            title = item.find('title').text
            description = item.find('description').text
            publication_date = item.find('pubDate').text
            url = item.find('link').text

            exists = db.query('SELECT * FROM posts WHERE post_url = %s',(url,))
            if not exists:
                potential_coin_focus = subject_analyser(db,title,coin_name_list,coin_symbol_list)
                if potential_coin_focus == '000':
                    potential_coin_focus = subject_analyser(db,description,coin_name_list,coin_symbol_list) #only worth analysing both if subject wasn't found in title
                print(title + ' - ' + potential_coin_focus)
                
                db.commit('INSERT INTO posts (post_url,post_datetime,source_id,coin_type_id,post_processed) VALUES (%s,%s,%s,%s,%s)',(url,publication_date,source_id,potential_coin_focus,False))
            #db.commit('UPDATE ')
            #print(item.find('link').text)
            #print(item.find('pubDate').text)
