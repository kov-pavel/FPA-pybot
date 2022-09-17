import logging
import os
from io import BytesIO
from zipfile import ZipFile

import telebot

from auth import user, admin
from config import ARCHIVE_NAME, SECRET_KEY, WATERMARKS, STATUSES, BACKDOOR
from db import Database
from watermark import apply_watermark

bot = telebot.TeleBot(SECRET_KEY)
logger = telebot.logger
telebot.logger.setLevel(logging.ERROR)


@bot.message_handler(commands=['start'])
@user(bot)
def send_welcome(msg):
    bot.reply_to(msg, "Бета версия бота для наложения защиты на картинку. \n"
                      "Введите /help для ознакомления с функционалом")


@bot.message_handler(commands=['help'])
@user(bot)
def send_help(msg):
    bot.reply_to(msg, "Для использования бота просто отправьте ему сообщение, содержащее: \n"
                      "1) Любую фотографию \n"
                      "2) Фотографию, прикрепленную как файл \n"
                      "3) Архив формата .zip, содержащий в себе только(!) фотографии любого формата размером до 50 мб\n"
                      "Ответным сообщением вы получите фотографию/архив с вашими фотографиями с наложенной защитой\n\n"
                      "Чтобы сменить кодируемое слово, напишите /change\n"
                      "Чтобы добавить нового пользователя, напишите /add\n"
                      "Чтобы удалить пользователя, напишите /remove\n"
                      "Чтобы вывести список пользователей, напишите /list\n")


@bot.message_handler(commands=['change'])
@user(bot)
def send_change(msg):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    but1 = telebot.types.KeyboardButton("Тренд")
    but2 = telebot.types.KeyboardButton("Финтрендинг")
    markup.add(but1, but2)
    bot.reply_to(msg, "Выберите новое слово\n", reply_markup=markup)
    bot.register_next_step_handler(msg, change_word)


def change_word(msg):
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    if msg.text in WATERMARKS:
        with Database() as db:
            db.set_new_word(msg.from_user.id, msg.text)
            bot.reply_to(msg, f"Кодовое слово изменено на {msg.text}", reply_markup=markup)
    else:
        bot.reply_to(msg, "Неправильное слово\n", reply_markup=markup)


@bot.message_handler(content_types=['document'])
@user(bot)
def edit_archive(message):
    with Database() as db:
        type_of_watermark = db.get_watermark_type(message.from_user.id)
    try:
        file_info = bot.get_file(message.document.file_id)
        arc = bot.download_file(file_info.file_path)
        with ZipFile(ARCHIVE_NAME, 'w') as result:

            with ZipFile(BytesIO(arc), 'r') as zip:
                namelist = zip.namelist()

                for filename in namelist:
                    processed_file = apply_watermark(zip.read(filename), type_of_watermark)
                    result.writestr(filename, processed_file)

        with open(ARCHIVE_NAME, 'rb') as result:
            bot.send_document(message.chat.id, result)
    except Exception as ex:
        print("Error: ", ex)
    finally:
        os.remove(ARCHIVE_NAME)


@bot.message_handler(content_types=['photo'])
@user(bot)
def edit_photo(message):
    with Database() as db:
        type_of_watermark = db.get_watermark_type(message.from_user.id)
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        result = apply_watermark(downloaded_file, type_of_watermark)
        bot.send_photo(message.chat.id, result)
    except Exception as ex:
        print("Error: ", ex)


@bot.message_handler(commands=['add'])
@admin(bot)
def add_user(msg):
    bot.reply_to(msg, "Вы собираетесь добавить в бота нового пользователя\n"
                      "Введите его ID:\n")
    bot.register_next_step_handler(msg, choose_status)


@bot.message_handler(commands=['list'])
@admin(bot)
def users_list(msg):
    response = "Список пользователей:\n"
    with Database() as db:
        users = db.get_all_users()
        for user in users:
            if user[0] != BACKDOOR:
                response += f'Id: {user[0]}, статус: {STATUSES[user[1]]}, имя: {user[2]}\n'
        bot.reply_to(msg, response)


@bot.message_handler(commands=['remove'])
@admin(bot)
def remove_user(msg):
    bot.reply_to(msg, "Вы собираетесь удалить пользователя\n"
                      "Введите его ID:\n")
    bot.register_next_step_handler(msg, check_user)


def check_user(msg):
    try:
        user_id = int(msg.text)
        with Database() as db:
            db.delete_user(user_id)
            bot.reply_to(msg, f"Пользователь {user_id} удален\n")
    except ValueError:
        bot.reply_to(msg, f"Неверный id\n")


def choose_status(msg) -> None:
    try:
        user_id = int(msg.text)
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        but1 = telebot.types.KeyboardButton("Пользователь")
        but2 = telebot.types.KeyboardButton("Администратор")
        markup.add(but1, but2)
        bot.reply_to(msg, "Какой статус будет у нового пользователя\n", reply_markup=markup)
        bot.register_next_step_handler(msg, add_username, user_id=user_id)
    except ValueError:
        bot.reply_to(msg, f"Не могу добавить пользователя {msg.text}\n", reply_markup=None)


def add_username(msg, user_id: int) -> None:
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    with Database() as db:
        bot.reply_to(msg, f"Как вы хотите назвать этого пользователя\n", reply_markup=markup)
        bot.register_next_step_handler(msg, add_new_user, user_id=user_id, status=msg.text == 'Администратор')


def add_new_user(msg, user_id: int, status: bool) -> None:
    with Database() as db:
        db.add_new_user(user_id, status, msg.text)
        bot.reply_to(msg, f"Пользователь {user_id} добавлен\n", reply_markup=None)


if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(e)
