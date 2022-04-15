from secret import token
from random import choice
from parsing import *
from utils import *

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

from telegram.ext import (
    Updater,
    MessageHandler, 
    Filters
)


keyboard = [
    ['Расписание игр', 'Рейтинг'],
    ['Фотографии'],
]

markup = ReplyKeyboardMarkup(
    keyboard,
    one_time_keyboard=False,
    resize_keyboard=True
)



def send_sched(update, context):
    sched_info = get_sched()
    # parse_mode="MarkdownV2" - в этом режиме можем использовать разметку Telegram в тексте сообщения
    # если не использовать этот аргумент, к примеру, двойные звездочки будут передаваться "как есть"
    # (вместо преобразования текста в жирный), а код [Google](https://google.com) не будет корректной ссылкой
    # disable_web_page_preview=True - не прикреплять предпросмотр ссылки к сообщению
    update.message.reply_text(form_sched_str(sched_info), reply_markup=markup, disable_web_page_preview=True, parse_mode="MarkdownV2")


def send_rating(update, context):
    update.message.reply_text(form_rating(get_rating()), reply_markup=markup)   


def other_text(update, context):
    update.message.reply_text("Нажмите на одну из кнопок Главного меню", reply_markup=markup)


updater = Updater(token)

dispatcher = updater.dispatcher


dispatcher.add_handler(MessageHandler(Filters.text("Расписание игр"), send_sched))
dispatcher.add_handler(MessageHandler(Filters.text("Рейтинг"), send_rating))
dispatcher.add_handler(MessageHandler(Filters.text, other_text))


updater.start_polling()
updater.idle()
