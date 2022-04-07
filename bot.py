import logging
import telebot
import os
import telegram_send
from  telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from algorand import *
# from apscheduler.schedulers.background import BackgroundScheduler

ASSET_NAMES = ['AKITA', 'TINYUSDC', 'USDC', 'PLANETS', 'OPUL', 'AWT']

TOKEN = '5147511379:AAGU-RIX5yl1lLNR_YG-ekYlpHwNNovLj2Y'
bot = telebot.TeleBot(TOKEN)

# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

# We define command handlers. Error handlers also receive the raised TelegramError object in error.
# @bot.message_handler(content_types=["text"])
# def start(update, context, job):
#     """Sends a message when the command /start is issued."""
#     chat_info_id = job.context
#     context.bot.send_message(chat_id=chat_info_id, text= f'This is a telegram bot that sends you liquidity updates on pools in the algorand blockchain.\n We currently have {ASSET_NAMES} that this bot functions for checking the asset prices and liquidity updates for the {ASSET_NAMES}/ALGO liquidity pool')



def help(bot, context):
    """Sends a message when the command /help is issued."""
    bot.message.reply_text('Help!')


def echo(bot, context):
    """Echos the user message."""
    bot.message.reply_text(bot.message.text)

# @bot.message_handler(content_types=["text"])
# @bot.message_handler(commands=['start'])
def bot_whale(update, bot, job_queue):
    chat_id = update.message.chat.id
    whale_activities()
    bot.send_message(chat_id=chat_id, text=f"{response_whale}")
    job_queue.run_repeating(start, 5, context=chat_id)

    # length_rem = len(response_whale_removed)
    # for items in response_whale
    print(response_whale)

""" To stop receiving updates from the bot"""
def stop_updates(bot, job_queue):
    bot.send_message(chat_id=bot.chat.id,
                      text='Stopped!')
    job_queue.stop()
# message[-1].message_id

def bot_get_asset(update, context):
    asset_prices_get()
    length = len(response_asset)
    for i in range(length):
        update.message.reply_text(response_asset[i])

def error(update, context):
    """Logs Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Starts the bot."""
    # Creates the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = '5147511379:AAGU-RIX5yl1lLNR_YG-ekYlpHwNNovLj2Y'#enter your token here
    APP_NAME='https://arcane-coast-66180.herokuapp.com/' #Edit the heroku app-name


    
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    #
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", bot_whale, pass_args=True, pass_job_queue=True))


    # dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("asset", bot_get_asset, pass_job_queue=True)) # fetches the prices of assets in the list
    dp.add_handler(CommandHandler('stop', stop_updates, pass_args=True, pass_job_queue=True)) # Stop the bot from sending messages




    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))


    # log all errors
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    # updater.start_polling(clean=True)

    updater.idle()



if __name__ == '__main__':
    main()