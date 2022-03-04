import telebot
import sqlite3
from zipfile import ZipFile
from io import BytesIO
import os

from telebot import types

from watermark import apply_watermark
from config import ARCHIVE_NAME

bot = telebot.TeleBot("5129621356:AAFPoKs4SPEcU299zaJscEEXJwEgS8efxm4")
try:
    connect = sqlite3.connect("d:\\labs\\bot\\FPA-pybot\\Bot\\users.db")
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users 
        (id BIGINT,
        word BOOLEAN,
        UNIQUE(id)
        );
        """)

    connect.commit()
finally:
    cursor.close()
    connect.close()


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.reply_to(msg, "Бета версия бота для наложения защиты на картинку. \n"
                      "Введите /help для ознакомления с функционалом")


@bot.message_handler(commands=['help'])
def send_help(msg):
    bot.reply_to(msg, "Для использования бота просто отправьте ему сообщение, содержащее: \n"
                      "1) Любую фотографию \n"
                      "2) Фотографию, прикрепленную как файл \n"
                      "3) Архив формата .zip, содержащий в себе только(!) фотографии любого формата размером до 50 мб\n"
                      "Ответным сообщением вы получите фотографию/архив с вашими фотографиями с наложенной защитой\n\n"
                      "Чтобы сменить кодируемое слово, напишите /change")


@bot.message_handler(commands=['change'])
def send_help(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    but1 = types.KeyboardButton("Тренд")
    but2 = types.KeyboardButton("Финтрендинг")
    markup.add(but1, but2)
    bot.reply_to(msg, "Выберите новое слово\n", reply_markup=markup)
    bot.register_next_step_handler(msg, change_word)


def change_word(msg):
    try:
        connect = sqlite3.connect("d:\\labs\\bot\\FPA-pybot\\Bot\\users.db")
        cursor = connect.cursor()
        if msg.text == "Тренд":
            cursor.execute("""INSERT OR REPLACE INTO users (id, word)
                                     VALUES ({id}, {value});
                         """.format(id=msg.chat.id, value=0))
            bot.reply_to(msg, "Кодовое слово изменено на Тренд", reply_markup=None)
        elif msg.text == "Финтрендинг":
            cursor.execute("""INSERT OR REPLACE INTO users (id, word)
                               VALUES ({id}, {value});
                   """.format(id=msg.chat.id, value=1))
            bot.reply_to(msg, "Кодовое слово изменено на Финтрендинг", reply_markup=None)
        else:
            bot.reply_to(msg, "Неправильное слово\n", reply_markup=None)
    finally:
        connect.commit()
        cursor.close()
        connect.close()


@bot.message_handler(content_types=['document'])
def edit_archive(message):
    type_of_watermark = get_watermark_type(message.chat.id)
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
def edit_photo(message):
    type_of_watermark = get_watermark_type(message.chat.id)
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        result = apply_watermark(downloaded_file, type_of_watermark)
        bot.send_photo(message.chat.id, result)
    except Exception as ex:
        print("Error: ", ex)


def get_watermark_type(user_id):
    try:
        connect = sqlite3.connect("d:\\labs\\bot\\FPA-pybot\\Bot\\users.db")
        cursor = connect.cursor()
        cursor.execute(f"""SELECT word FROM users WHERE id={user_id}""");
        type = cursor.fetchone()
        if type is None:
            return 0
        else:
            return type[0]
    finally:
        connect.commit()
        cursor.close()
        connect.close()


bot.infinity_polling()
