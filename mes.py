start = """
✅ Цена с Binance
✅ Изменение цены за 24 часа
✅ Цена с Coinbase
✅ Парсинг bestchaing USDTBTC
✅ Калькулятор (конвертер) BTC ETH USDT RUB💸
"""
help = """
Список основных команд
/start - Список того что я умею
/help - сейчас ты тут
/conversion - калькулятор (конвертер)

Цена по биржам:

/binance - курс любой биржевой пары Binance
/BinanceList - лист цены с Binance
/coinbase - курс любой биржевой пары Coinbase
/CoinbaseList - лист цены с Coinbase
/pricechange24h - изменение цены 24ч Binance

Парсинг предложений обменников:
с сайта "bestchange.ru"

/bestchUSDTBTC - предложения по USDT->BTC
/bestchBTCUSDT - предложения по BTC->USDT
"""
tz = '''
❌ Топ 3 криптобирж
❌ Лучший курс, худший курс
❌ Изменение цены час, неделя, месяц
❌ Парсинг bestchaing по парам
❌ Конвертор валюты с предложением лучшего курса
❌ Самостоятельная торговля маржи binance
'''
what_get = 'Отлично! Теперь выбери что хочешь получить: '
what_amount = 'А теперь напиши мне сумму которую хочешь поменять: '
data_entry_error = '''
‼️Данные введены некоректно:
Вместо запятой попробуй точку‼️
p.s. про то что текст ты писать не должен, я вообще молчу‼️
'''
for_binance_symbol = '''
Введи валютную пару примерно так: "btcusdt"
'''
for_coinbace_symbol = '''
Введи валютную пару примерно так: "btc-usd"
'''