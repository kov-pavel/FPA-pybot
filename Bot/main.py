import io
import telebot
from zipfile import ZipFile
from io import BytesIO
import os
from watermark import apply_watermark
from config import ARCHIVE_NAME


bot = telebot.TeleBot("5129621356:AAFPoKs4SPEcU299zaJscEEXJwEgS8efxm4")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.reply_to(msg, "Putin is God")

@bot.message_handler(content_types=['document'])
def edit_archive(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        arc = bot.download_file(file_info.file_path)
        with ZipFile(ARCHIVE_NAME, 'w') as result:

            with ZipFile(BytesIO(arc), 'r') as zip:
                namelist = zip.namelist()

                for filename in namelist:
                    processed_file = apply_watermark(zip.read(filename))
                    result.writestr(filename, processed_file)
        
        with open(ARCHIVE_NAME, 'rb') as result:
            bot.send_document(message.chat.id, result)
    except Exception as ex:
        print("Error: ", ex)
    finally:
        os.remove(ARCHIVE_NAME)

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
