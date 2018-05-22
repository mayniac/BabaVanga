from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk.data
from os import listdir,remove
from os.path import isfile, join
import sys
sys.path.insert(0, 'lib')
from utils import dprint,subject_analyser,get_coin_name_list,get_coin_symbol_list
import dbfunc

#not going to lie, almost everything here is from https://dev.to/davidisrawi/build-a-quick-summarizer-with-python-and-nltk
#hopefully I will optimise it at some point

def article_summariser(article_text,stop_words):
    words = word_tokenize(article_text)
    freq_table = dict()
    for word in words:
        word = word.lower()
        if word not in stop_words:
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

    sentences = sent_tokenize(article_text)
    sentence_value = dict()

    for sentence in sentences:
        for word,value in freq_table.items():
            if word in sentence.lower():
                if sentence[:12] in sentence_value:
                    sentence_value[sentence[:12]] += value
                else:
                    sentence_value[sentence[:12]] = value

    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]

    # Average value of a sentence from original text
    average = int(sum_values/ len(sentence_value))
    summary = ''

    article_word_count = len(article_text.split())
    multiplier = 1.25 #put this in settings at some point? Probably should be dynamic based on article length

    for sentence in sentences:
        if sentence[:12] in sentence_value and sentence_value[sentence[:12]] > (multiplier * average):
            summary +=  " " + sentence
    return summary

def summary_to_db(summary,post_id,db): #this tries to get the coin subjects of sentences correct
    coin_name_list = get_coin_name_list(db)
    coin_symbol_list = get_coin_symbol_list(db)

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    summary_sentences = tokenizer.tokenize(summary)

    coin_subjects = []

    for s in summary_sentences:
        s = s.replace('\n','').replace('\t','')
        s_coin_type = subject_analyser(db,s,coin_name_list,coin_symbol_list)
        coin_subjects.append([s,s_coin_type])

    #logic: if one sentence in the article references a single coin, but none of the other sentences do, it is likely
    #that the article started by specifying the coin then used filler words like "it" which won't get picked up by subject_analyser.
    #however, sentences in the article containing multiple coins still should be identified as separate to avoid cross-contamination of sentiment
    not_none = []
    for cs in coin_subjects:
        if cs[1] != 'None':
            if cs[1] not in not_none:
                not_none.append(cs[1])

    #print(not_none)
    if len(not_none) == 1:
        for cs in coin_subjects:
            if cs[1] == 'None':
                cs[1] = not_none[0]

    for cs in coin_subjects:
        chunk = cs[0]
        chunk_subject = cs[1]
        db.commit('INSERT INTO chunks (chunk,post_id,coin_id) VALUES (%s,%s,%s)',(chunk,post_id,chunk_subject))

    cleanup_file = 'tmp/' + post_id
    try:
        remove(cleanup_file)
    except:
        dprint("Couldn't remove " + cleanup_file) 

def chunk_articles(db):
    stop_words = set(stopwords.words("english"))
    article_list = [f for f in listdir('tmp') if isfile(join('tmp',f))]
    for article_filename in article_list:
        with open('tmp/' + article_filename, 'r') as article_file:
            article_text = str(article_file.read())
            article_summary = article_summariser(article_text,stop_words)
            summary_to_db(article_summary,article_filename,db)
            #print('filename - ' + article_filename + '  original - ' + str(len(article_text.split())) + '  summary - ' + str(len(article_summary.split())))
