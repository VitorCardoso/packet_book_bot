import telegram
import time
from configuration import configuration as config
from configuration import logging
from telegram.ext import TypeHandler, Updater, CommandHandler, MessageHandler, Filters

telegram_config = config['telegram']

TOKEN=telegram_config['token']

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome to Free Books from Packtpub Boot!")

def list_book(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="go list books")

def echo(bot, update):
    text = update.message.text
    result=None
    if text.isnumeric():
        result = int(text) ** 2
    else:
        result = 'NOP'
    bot.send_message(chat_id=update.message.chat_id, text=result)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

list_book_handler = CommandHandler('book', list_book)
dispatcher.add_handler(list_book_handler)

timeToKill = int(telegram_config['timeToKill'])
updater.start_polling()
logging.info('Stop in %d seconds' % timeToKill)
time.sleep(timeToKill)
updater.stop()