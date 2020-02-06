import telebot
from flask import request, render_template, url_for, redirect
from requests import get

from . import server, bot, db, BOT_URL
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


@server.route('/rosters/<user_id>')
def user(user_id):
    user = User.query.filter_by(user_telegram_id=user_id).first_or_404()
    rosters = user.rosters.all()
    return render_template(
        'user.html', title='Your list', rosters=rosters
    )


@server.route('/rosters/<user_id>/<roster_id>')
def roster(user_id, roster_id):
    user = User.query.filter_by(user_telegram_id=user_id).first_or_404()
    roster = user.rosters.filter_by(id=roster_id).first_or_404()
    return render_template(
        'roster.html', title='Your roster', input_roster=roster
    )


@server.route('/rosters/<user_id>/<roster_id>/delete-roster')
def delete_roster(user_id, roster_id):
    user = User.query.filter_by(user_telegram_id=user_id).first_or_404()
    roster = user.rosters.filter_by(id=roster_id).first_or_404()
    if roster is not None:
        db.session.delete(roster)
        db.session.commit()
    return redirect(url_for('user', user_id=user.user_telegram_id))


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "!", 200


@server.route("/set_webhook")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=BOT_URL + 'bot')
    return "set webhook", 200
