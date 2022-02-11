import io
import telebot
from watermark import apply_watermark
from zipfile import ZipFile
from io import BytesIO
import os
import shutil

bot = telebot.TeleBot("5129621356:AAFPoKs4SPEcU299zaJscEEXJwEgS8efxm4")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.reply_to(msg, "Putin is God")


@bot.message_handler(content_types=['document'])
def edit_archive(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        arc = bot.download_file(file_info.file_path)
        result = ZipFile('Result.zip', 'w')

        with ZipFile(BytesIO(arc), 'a') as zip:
            namelist = zip.namelist()

            for filename in namelist:
                processed_file = apply_watermark(zip.read(filename))
                result.writestr(filename, processed_file)

        # This!!!
        bot.send_document(message.chat.id, open(result.filename, 'rb').read())
    except Exception as ex:
        print("Error: ", ex)


@bot.message_handler(content_types=['photo'])
def edit_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        result = apply_watermark(downloaded_file)
        bot.send_photo(message.chat.id, result)
    except Exception as ex:
        print("Error: ", ex)


bot.infinity_polling()
