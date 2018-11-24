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
#job = updater.job_queue

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome to Free Books from Packtpub Boot!")

def list_book(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="go list books Adriana")

def echo(bot, update):
    print(update.message)
    text = update.message.text
    result=None
    if text.isnumeric():
        result = int(text) ** 2
    else:
        result = 'Error !!!'
    bot.send_message(chat_id=update.message.chat_id, text=result)

def sayhi(bot, job):
    job.context.message.reply_text("hi")

def callback_increasing(bot, job):
    print(job.__dict__)
    #bot.send_message(chat_id='@examplechannel',
                      #text='Sending messages with increasing delay up to 10s, then stops.')
    job.interval += 1.0
    if job.interval > 10.0:
        job.schedule_removal()

def callback_alarm(bot, job):
    bot.send_message(chat_id=job.context, text='BEEP')

def callback_timer(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id, text='Setting a timer for 3 seconds!')
    job_queue.run_once(callback_alarm, 3, context=update.message.chat_id)

def main():
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('book', list_book))

    dispatcher.add_handler(CommandHandler('timer', callback_timer, pass_job_queue=True))

    #dispatcher.add_handler(MessageHandler(Filters.text , time, pass_job_queue=True))

    #job_minute = job.run_repeating(callback_increasing, 1)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()