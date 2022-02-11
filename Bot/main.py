import telebot
from watermark import apply_watermark

bot = telebot.TeleBot("5129621356:AAFPoKs4SPEcU299zaJscEEXJwEgS8efxm4")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.reply_to(msg, "Putin is God")


@bot.message_handler(content_types=['document'])
def edit_doc(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        result = process_photo(file_info)
        bot.send_photo(message.chat.id, result)
    except Exception as ex:
        print("Error: ", ex)

@bot.message_handler(content_types=['photo'])
def edit_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        result = process_photo(file_info)
        bot.send_photo(message.chat.id, result)
    except Exception as ex:
        print("Error: ", ex)

def process_photo(file_info) -> bytes:
    downloaded_file = bot.download_file(file_info.file_path)
    return apply_watermark(downloaded_file)

bot.infinity_polling()
