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
        schedule.every(settings.coin_price_interval).minutes.do(market_observer.insert_current_coin_values,db)
        schedule.every(settings.rss_feed_interval).minutes.do(post_collector.post_updater,db)
        schedule.every(settings.article_scraper_interval).minutes.do(article_scrapers.find_posts_to_be_processed,db)
        schedule.every(settings.nlp_chunker_interval).minutes.do(nlp_chunker.chunk_articles,db)

        while True:
            schedule.run_pending()
            time.sleep(1)
