import telebot
import os
from flask import Flask, request
from configparser import ConfigParser


config = ConfigParser()
config.read('config.ini')

# TOKEN = config['bot']['Token']
TOKEN = "TOKEN"
BOT_URL = "https://boiling-spire-19861.herokuapp.com/bot"
PORT = os.environ.get('PORT', 80)

server = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BOT_URL)
    return "?", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello there!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if os.environ.get('HEROKU'):
    server.run(host="0.0.0.0", port=PORT)
else:
    bot.polling()
