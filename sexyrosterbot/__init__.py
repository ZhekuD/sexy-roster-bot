import os
from configparser import ConfigParser

from telebot import TeleBot
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


config = ConfigParser()
config.read('config.ini')

TOKEN = os.environ.get('TOKEN') or config['bot']['Token']
PORT = os.environ.get('PORT', 80)
BOT_URL = "https://sexy-roster.herokuapp.com/bot"
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

server = Flask(__name__)
db = SQLAlchemy(server)
migrate = Migrate(server, db)
bot = TeleBot(TOKEN)


from sexyrosterbot import routes, bot
