import datetime

#any method called by more than one file goes in here

def dprint(message):
    date_time = datetime.datetime.now()
    print('[' + date_time.strftime('%Y/%m/%d %H:%M') + '] - ' + message)

def get_coin_symbol_list(db):
    coin_symbol_tuple = db.query('SELECT coin_symbol FROM coin_types WHERE coin_symbol != \'000\'')
    coin_symbol_list = list()
    for coin in coin_symbol_tuple:
        coin_symbol_list.append(coin[0])
    return coin_symbol_list

def get_coin_name_list(db):
    coin_name_tuple = db.query('SELECT coin_name FROM coin_types WHERE coin_symbol != \'000\'')
    coin_name_list = list()
    for coin in coin_name_tuple:
        coin_name_list.append(coin[0])
    return coin_name_list

def coin_symbol_to_coin_name(db,coin_symbol):
    return db.query('SELECT coin_name FROM coin_types WHERE coin_symbol=\'' + coin_symbol + '\'')[0][0]

def coin_name_to_coin_symbol(db,coin_name):
    return db.query('SELECT coin_symbol FROM coin_types WHERE coin_name=\'' + coin_name + '\'')[0][0]



def subject_analyser(db,text,coin_name_list,coin_symbol_list):
    found_coins = 0
    found_symbols = 0
    coin_subject = ''
    multiple = '000'
    none = '999'
    multi_coin_list = ['other digital currencies','blockchains','other such currencies','other currencies','other coins','altcoins','cryptocurrencies'] #not exhaustive, doesn't matter
    for coin_name in coin_name_list:
        if coin_name.lower() in text.lower():
            coin_subject = coin_name_to_coin_symbol(db,coin_name)
            if found_coins > 0:
                return multiple
            found_coins += 1

    for coin_symbol in coin_symbol_list:
        if coin_symbol.lower() in text.lower():
            coin_subject = coin_symbol
            if found_symbols > 0:
                return multiple
            found_symbols += 1

    for multi_coin in multi_coin_list:
        if multi_coin in text.lower():
            return multiple #filters out some of the shittyness such as "cryptocurrencies LIKE bitcoin" where article focus is not solely on bitcoin

    if found_coins == 1 or found_symbols == 1:
        return coin_subject #if only one coin name was found, it's very likely correct
    elif found_coins == 0 and found_symbols == 0:
        return none
    else:
        return multiple #otherwise return multi as placeholder
    #print(title)

#def clunk_coin_encode(clunk,)
