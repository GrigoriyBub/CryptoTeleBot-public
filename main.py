import requests
from bs4 import BeautifulSoup
import config
import dbworker
import mes


bot = config.bot


def db_us_verification(message):
    us_id = int(message.from_user.id)
    us_name = str(message.from_user.first_name)
    if dbworker.table_value(us_id):
        pass
    else:
        dbworker.add_new_user(us_id, us_name, config.States.S_NOSTAT.value)
        bot.send_message(config.ROOT_USER, 'Новая запись в БД: \n' + str(message.chat.id))


def binance_get_price_symbol(symbol):
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=' + symbol.upper()
    data = requests.get(url).json()
    return data['price']


def coinbace_get_price_symbol(symbol):
    url = 'https://api.coinbase.com/v2/prices/' + symbol.upper() + '/spot'
    req = requests.get(url)
    data = req.json()
    price = data["data"]["amount"]
    return price


@bot.message_handler(commands=['exit'])
def cmd_exit(message):
    if config.autor(message.chat.id):
        dbworker.set_state(message.from_user.id, config.States.S_NOSTAT.value)
        bot.send_message(message.chat.id, message.from_user.first_name + ', начни с начала:',
                         reply_markup=config.kb_help)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        bot.send_message(message.chat.id, 'Привет, ' + message.from_user.first_name + ' !!\n' + mes.start,
                         reply_markup=config.kb_help)
    else:
        db_us_verification(message)
        config.not_autor(message)


@bot.message_handler(commands=['help'])
def cmd_help(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        user_name = message.from_user.first_name
        bot.send_message(message.chat.id, user_name + ', правильно! В любой не понятной ситуации - жми /help')
        dbworker.set_state(message.from_user.id, config.States.S_HELP.value)
        bot.send_message(message.chat.id, mes.help)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['conversion'])
def cmd_conversion(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        dbworker.set_state(message.from_user.id, config.States.S_CONVERSION.value)
        bot.send_message(message.chat.id, 'Что отдаёте?', reply_markup=config.kb_conversion)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['CoinbaseList'])
def cmd_coinbaselist(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        for el in config.symbol_list_coinbase:
            url = 'https://api.coinbase.com/v2/prices/' + el.upper() + '/spot'
            req = requests.get(url)
            data = req.json()
            price = f'{el.upper()} --> {data["data"]["amount"]}'
            bot.send_message(message.chat.id, price)

    else:
        config.not_autor(message)


@bot.message_handler(commands=['binance'])
def cmd_bin(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        dbworker.set_state(message.from_user.id, config.States.S_PRICE_BINANCE.value)
        bot.send_message(message.chat.id, mes.for_binance_symbol, reply_markup=config.kb_exit)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['coinbase'])
def cmd_coinbace(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        dbworker.set_state(message.from_user.id, config.States.S_PRICE_COINBASE.value)
        bot.send_message(message.chat.id, mes.for_coinbace_symbol, reply_markup=config.kb_exit)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['BinanceList'])
def cmd_binancelist(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        for el in config.symbol_list_binance:
            url = 'https://api.binance.com/api/v3/ticker/price?symbol=' + el.upper()
            req = requests.get(url)
            data = req.json()
            price_symbol_list = f"{data['symbol']} -->  {float(data['price'])}"
            bot.send_message(message.chat.id, price_symbol_list)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['pricechange24h'])
def cmd_PriceChange24h(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        symbol_list = ['BTCUSDT', 'LTCUSDT', 'ETHUSDT', 'ETCUSDT', 'USDTRUB']
        for el in symbol_list:
            url = 'https://api.binance.com/api/v3/ticker/24hr?symbol=' + el.upper()
            req = requests.get(url)
            data = req.json()
            price_list_message = f"{data['symbol']}: \n" \
                                 f" open: {float(data['openPrice'])} hight: {float(data['highPrice'])} \n" \
                                 f" change: {float(data['priceChange'])}  ({float(data['priceChangePercent'])})"
            bot.send_message(message.chat.id, price_list_message, reply_markup=config.kb_help)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['bestchUSDTBTC'])
def cmd_bestchusdtbtc(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        filtered = []
        url = 'https://www.bestchange.ru/tether-trc20-to-bitcoin.html'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        allprice = soup.findAll('td', class_='bi')
        for el in allprice:
            if el.find('div', class_='fs'):
                filtered.append(el.text)
        for data in filtered[:10]:
            bot.send_message(message.chat.id, data)
    else:
        config.not_autor(message)


@bot.message_handler(commands=['bestchBTCUSDT'])
def cmd_bestchbtcusdt(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        filtered = []
        url = 'https://www.bestchange.ru/bitcoin-to-tether-trc20.html'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")
        allprice = soup.findAll('td', class_='bi')
        for el in allprice:
            if el.text:
                filtered.append(el.text)
        for data in filtered[:20]:
            bot.send_message(message.chat.id, data)
    else:
        config.not_autor(message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    db_us_verification(message)
    if config.autor(message.chat.id):
        if dbworker.get_state(message.from_user.id) == config.States.S_HELP.value:
            bot.send_message(message.chat.id, mes.help)
        elif dbworker.get_state(message.from_user.id) == config.States.S_NOSTAT.value:
            bot.send_message(message.chat.id, message.text)
        elif dbworker.get_state(message.from_user.id) == config.States.S_PRICE_BINANCE.value:
            try:
                bot.send_message(message.chat.id, str(binance_get_price_symbol(message.text)), reply_markup=config.kb_exit)
            except:
                bot.send_message(message.chat.id, 'что-то не так(')
        elif dbworker.get_state(message.from_user.id) == config.States.S_PRICE_COINBASE.value:
            try:
                bot.send_message(message.chat.id, str(coinbace_get_price_symbol(message.text)), reply_markup=config.kb_exit)
            except:
                bot.send_message(message.chat.id, 'что-то не так(')
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION.value:
            if message.text == 'BTC':
                bot.send_message(message.chat.id, mes.what_get, reply_markup=config.kb_conversion_btc)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_BTC.value)
            elif message.text == 'ETH':
                bot.send_message(message.chat.id, mes.what_get, reply_markup=config.kb_conversion_eth)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_ETH.value)
            elif message.text == 'USDT':
                bot.send_message(message.chat.id, mes.what_get, reply_markup=config.kb_conversion_usdt)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_USDT.value)
            elif message.text == 'RUB':
                bot.send_message(message.chat.id, mes.what_get, reply_markup=config.kb_conversion_rub)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_RUB.value)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_BTC.value:
            if message.text == 'ETH':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_BTCETH.value)
            elif message.text == 'USDT':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_BTCUSDT.value)
            elif message.text == 'RUB':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_BTCRUB.value)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_ETH.value:
            if message.text == 'BTC':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_ETHBTC.value)
            elif message.text == 'USDT':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_ETHUSDT.value)
            elif message.text == 'RUB':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_ETHRUB.value)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_USDT.value:
            if message.text == 'BTC':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_USDTBTC.value)
            elif message.text == 'ETH':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_USDTETH.value)
            elif message.text == 'RUB':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_USDTRUB.value)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_RUB.value:
            if message.text == 'BTC':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_RUBBTC.value)
            elif message.text == 'ETH':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_RUBETH.value)
            elif message.text == 'USDT':
                bot.send_message(message.chat.id, mes.what_amount, reply_markup=config.kb_exit)
                dbworker.set_state(message.from_user.id, config.States.S_CONVERSION_RUBUSDT.value)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_BTCETH.value:
            try:
                sum_btceth = float(binance_get_price_symbol('WBTCETH')) * float(message.text)
                bot.send_message(message.chat.id, str(sum_btceth) + ' ETH',
                                 reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_BTCUSDT.value:
            try:
                sum_btcusdt = float(binance_get_price_symbol('BTCUSDT')) * float(message.text)
                bot.send_message(message.chat.id, str(sum_btcusdt) + ' USDT', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_BTCRUB.value:
            try:
                sum_btcrub = float(binance_get_price_symbol('BTCRUB')) * float(message.text)
                bot.send_message(message.chat.id, str(sum_btcrub) + ' RUB', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_ETHBTC.value:
            try:
                sum_ethbtc = float(binance_get_price_symbol('ETHBTC')) * float(message.text)
                bot.send_message(message.chat.id, str(sum_ethbtc) + ' BTC', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_ETHUSDT.value:
            try:
                sum_ethusdt = float(binance_get_price_symbol('ETHUSDT')) * float(message.text)
                bot.send_message(message.chat.id, str(sum_ethusdt) + ' USDT', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_ETHRUB.value:
            try:
                sum_ethrub = float(binance_get_price_symbol('ETHRUB')) * float(message.text)
                bot.send_message(message.chat.id, str(sum_ethrub) + ' RUB', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_USDTBTC.value:
            try:
                sum_usdtbtc = round(float(message.text) / float(binance_get_price_symbol('BTCUSDT')), 6)
                bot.send_message(message.chat.id, str(sum_usdtbtc) + ' BTC', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_USDTETH.value:
            try:
                sum_usdteth = round(float(message.text) / float(binance_get_price_symbol('ETHUSDT')), 6)
                bot.send_message(message.chat.id, str(sum_usdteth) + ' ETH', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_USDTRUB.value:
            try:
                sum_usdtrub = round(float(message.text) * float(binance_get_price_symbol('USDTRUB')), 6)
                bot.send_message(message.chat.id, str(sum_usdtrub) + ' RUB', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_RUBBTC.value:
            try:
                sum_rubbtc = round(float(message.text) / float(binance_get_price_symbol('BTCRUB')), 6)
                bot.send_message(message.chat.id, str(sum_rubbtc) + ' BTC', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_RUBETH.value:
            try:
                sum_rubeth = round(float(message.text) / float(binance_get_price_symbol('ETHRUB')), 6)
                bot.send_message(message.chat.id, str(sum_rubeth) + ' ETH', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
        elif dbworker.get_state(message.from_user.id) == config.States.S_CONVERSION_RUBUSDT.value:
            try:
                sum_rubusdt = round(float(message.text) / float(binance_get_price_symbol('USDTRUB')), 6)
                bot.send_message(message.chat.id, str(sum_rubusdt) + ' USDT', reply_markup=config.kb_conversion_exit)
            except:
                bot.send_message(message.chat.id, mes.data_entry_error)
    else:
        config.not_autor(message)


bot.polling(none_stop=True)
