import os
from io import StringIO
from datetime import datetime

from requests import get

from . import bot, db, TOKEN, BOT_URL
from .roster_parser import roster_body_parser, roster_style_parser
from .models import User, Roster


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Hello there! Send me your BattleScibe roster in HTML format " +
        "and I will make it pretty-looking and easy readable on your devices!"
    )

    if User.query.filter_by(user_telegram_id=message.chat.id).first() is None:
        user = User(
            user_telegram_id=message.chat.id,
            first_name=message.chat.first_name,
            second_name=message.chat.last_name,
            username=message.chat.username
        )
        db.session.add(user)
        db.session.commit()


@bot.message_handler(commands=['/profile'])
def send_profile_url(message):
    bot.send_message(message.chat.id, BOT_URL + str(message.chat.id))


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
        new_html = roster_body_parser(resp.text)

        roster = Roster(
            body=roster_style_parser(new_html, add_style=False),
            title=message.document.file_name[:-5],
            create_time=datetime.utcnow(),
            author=User.query.filter_by(user_telegram_id=message.chat.id).first()
        )
        db.session.add(roster)
        db.session.commit()

        file = StringIO(roster_style_parser(new_html))
        file.name = 'edited_' + message.document.file_name
        bot.send_message(chat_id, 'Here you go:')
        bot.send_message(
            message.chat.id,
            BOT_URL + f"rosters/{message.chat.id}/{roster.id}"
        )
        bot.send_document(chat_id, file)
        file.close()
    else:
        bot.send_message(chat_id, 'Something go wrong...')
