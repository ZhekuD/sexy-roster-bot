import telebot
from flask import request, render_template, url_for
from requests import get

from . import server, bot, BOT_URL
from .models import User, Roster


@server.route('/')
@server.route('/index')
def index():
    return render_template('index.html', title='Home')


@server.route('/users')
def users():
    users = User.query.all()
    users_string = '<p>'
    for user in users:
        users_string += str(user.username) + '-' + str(user.user_telegram_id) + '<br>'
    users_string += '</p>'
    return users_string


@server.route('/roster/<user_id>')
def roster(user_id):
    user = User.query.filter_by(user_telegram_id=user_id).first_or_404()
    roster = user.rosters.first()
    return render_template(
        'roster.html',
        title='Your roster',
        input_roster=roster
    )


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
