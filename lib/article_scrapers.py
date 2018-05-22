import requests
from bs4 import BeautifulSoup
import sys
import os.path
sys.path.insert(0, 'lib')
from utils import dprint
import dbfunc

def find_posts_to_be_processed(db):
    unprocessed_posts = db.query('SELECT * FROM posts WHERE post_processed=False')
    possibles = globals().copy()
    for unprocessed in unprocessed_posts:
        id = unprocessed[0]
        url = unprocessed[1]
        date = unprocessed[2]
        source_id = unprocessed[3]
        coin_focus = unprocessed[4]
        source = db.query('SELECT source_name FROM sources WHERE source_id = %s',(source_id,))[0][0]

        scraper = possibles.get(source)
        if not scraper:
            dprint("No article scraper implemented for - " + source)
        else:
            scraper(db,id,url)

def CoinDesk(db,id,url):
    post_html = requests.get(url).text
    html_soup = BeautifulSoup(post_html,'html.parser')
    article_text_with_html = html_soup.find("div", {"class": "article-content-container noskimwords"})
    article_text_with_html.script.decompose()
    article_text = ''.join(article_text_with_html.findAll(text=True))

    write_article_to_file(id,article_text)



def write_article_to_file(id,article_text):
    #path = os.path.join('tmp/',str(id))
    file = open('tmp/'+str(id),'w')
    file.write(article_text)
    file.close()
