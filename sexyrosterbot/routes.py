import telebot
from flask import request
from requests import get

from . import server, bot, BOT_URL
from .models import User, Roster


@server.route('/')
@server.route('/index')
def index():
    return 'sexy roster mainpage'


@server.route('/users')
def users():
    users = User.query.all()
    users_string = '<p>'
    for user in users:
        users_string += str(user.username) + '<br>'
    users_string += '</p>'
    return users_string


@server.route('/roster/<username>')
def roster(username):
    u = User.query.filter_by(username=username).first_or_404()
    r = u.rosters.first()
    return r.roster


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@server.route("/set_webhook")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BOT_URL)
    return "set webhook", 200
