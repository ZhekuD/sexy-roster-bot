from flask import Flask, request
from configparser import ConfigParser
from io import StringIO
from requests import get
import telebot
import os

from .roster_parser import roster_parser


config = ConfigParser()
config.read('config.ini')

TOKEN = os.environ.get('TOKEN') or config['bot']['Token']
PORT = os.environ.get('PORT', 80)
BOT_URL = "https://sexy-roster.herokuapp.com/"

server = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BOT_URL)
    return "?", 200

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Hello there! Send me your BattleScibe roster in HTML format \
        and I will make it pretty-looking and easy readable on your devices!"
    )

@bot.message_handler(content_types=['document'])
def send_document(message):
    chat_id = message.chat.id
    if not 'text/html' in message.document.mime_type:
        bot.send_message(chat_id, "Your file isn't HTML...")
        return

    file_info = bot.get_file(file_id=message.document.file_id)
    url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
    resp = get(url)
    if resp.ok:
        file = StringIO(roster_parser(resp.text))
        file.name = 'edited_' + message.document.file_name
        bot.send_message(chat_id, 'Here you go:')
        bot.send_document(chat_id, file)
        file.close()
    else:
        bot.send_message(chat_id, 'Something go wrong...')

if os.environ.get('HEROKU'):
    server.run(host="0.0.0.0", port=PORT)
else:
    bot.polling()
