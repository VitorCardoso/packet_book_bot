import telegram
import time
from configuration import configuration as config
from configuration import logging
from parser_html import BookParser
from telegram.ext import TypeHandler, Updater, CommandHandler, MessageHandler, Filters

telegram_config = config['telegram']

TOKEN = telegram_config['token']

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

book_parser = BookParser()


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Welcome to Free Books from Packtpub Bot!")


def list_book(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=telegram.ChatAction.TYPING)
    book_parser.parse()
    template = f"""
<b>{book_parser.title}</b>

{book_parser.desc}

Time left: {book_parser.left_time} hours

<a href="{book_parser.image}">____________</a>
<a href="{book_parser.offer_url}">Claim Here !!!</a>
    """
    bot.send_message(chat_id=update.message.chat_id,
                     text=template,
                     parse_mode=telegram.ParseMode.HTML)


def main():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('book', list_book))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
