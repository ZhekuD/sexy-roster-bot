import os
from io import StringIO

from requests import get

from . import bot, TOKEN
from .roster_parser import roster_parser


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Hello there! Send me your BattleScibe roster in HTML format " +
        "and I will make it pretty-looking and easy readable on your devices!"
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
