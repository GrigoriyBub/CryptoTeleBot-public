import telebot
from enum import Enum

ROOT_USER = '' #указать id администратора в str
user_list = [] #user_id, у которых есть доступ в int
db_file = "database.db"
API_KEY = '' #указать токен от botfather
bot = telebot.TeleBot(API_KEY)

symbol_list_coinbase = ['btc-usd', 'ltc-usd', 'eth-usd', 'etc-usd', 'usd-rub']
symbol_list_binance = ['btcusdt', 'ltcusdt', 'ETHUSDT', 'ETCUSDT', 'USDTRUB']


# Функция проверки авторизации
def autor(chatid):
    for el in user_list:
        if el == chatid or chatid == int(ROOT_USER):
            return True
    return False


def not_autor(message):
    bot.send_message(message.chat.id, 'Тебе сюда нельзя!')
    bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')
    bot.send_message(ROOT_USER, 'Кто-то ломится, его ID: \n' + str(message.chat.id))


# Клавиатура
kb_help = telebot.types.ReplyKeyboardMarkup()
kb_help.add('/help')
kb_exit = telebot.types.ReplyKeyboardMarkup()
kb_exit.add('/exit')
kb_conversion = telebot.types.ReplyKeyboardMarkup()
kb_conversion.add('BTC', 'ETH', 'USDT', 'RUB', '/exit', '/help')
kb_conversion_btc = telebot.types.ReplyKeyboardMarkup()
kb_conversion_btc.add('ETH', 'USDT', 'RUB', '/conversion', '/exit', '/help')
kb_conversion_eth = telebot.types.ReplyKeyboardMarkup()
kb_conversion_eth.add('BTC', 'USDT', 'RUB', '/conversion', '/exit', '/help')
kb_conversion_usdt = telebot.types.ReplyKeyboardMarkup()
kb_conversion_usdt.add('BTC', 'ETH', 'RUB', '/conversion', '/exit', '/help')
kb_conversion_rub = telebot.types.ReplyKeyboardMarkup()
kb_conversion_rub.add('BTC', 'ETH', 'USDT', '/conversion', '/exit', '/help')
kb_conversion_exit = telebot.types.ReplyKeyboardMarkup()
kb_conversion_exit.add('/conversion', '/exit')


class States(Enum):
    S_NOSTAT = 0
    S_HELP = 1
    S_CONVERSION = 2
    S_CONVERSION_BTC = 21
    S_CONVERSION_BTCETH = 212
    S_CONVERSION_BTCUSDT = 213
    S_CONVERSION_BTCRUB = 214
    S_CONVERSION_ETH = 22
    S_CONVERSION_ETHBTC = 221
    S_CONVERSION_ETHUSDT = 223
    S_CONVERSION_ETHRUB = 224
    S_CONVERSION_USDT = 23
    S_CONVERSION_USDTBTC = 231
    S_CONVERSION_USDTETH = 232
    S_CONVERSION_USDTRUB = 234
    S_CONVERSION_RUB = 24
    S_CONVERSION_RUBBTC = 241
    S_CONVERSION_RUBETH = 242
    S_CONVERSION_RUBUSDT = 243
    S_PRICE_BINANCE = 3
    S_PRICE_COINBASE = 4
