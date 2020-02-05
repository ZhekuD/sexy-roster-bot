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
BASEDIR = os.path.abspath(os.path.dirname(__file__))
BOT_URL = "https://sexy-roster.herokuapp.com/bot"


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'test.db')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(server)
migrate = Migrate(server, db)
bot = TeleBot(TOKEN)


from sexyrosterbot import routes, handlers, models
