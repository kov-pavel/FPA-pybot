import telebot
from imwatermark import WatermarkEncoder
from imwatermark import WatermarkDecoder
import cv2

bot = telebot.TeleBot("5129621356:AAFPoKs4SPEcU299zaJscEEXJwEgS8efxm4")
WM = "Vasya 777"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg):
    bot.reply_to(msg, "Putin is God")


@bot.message_handler(content_types=['document'])
def edit_doc(doc):
    try:
        file_info = bot.get_file(doc.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_document(doc.chat.id, downloaded_file)
    except Exception as ex:
        bot.send_message(doc.chat.id, "Error: " + ex)


def has_wm(photo):
    try:
        #photo = 'test.png'
        #photo_info = bot.get_file(photo.document.file_id)
        #photo_in = bot.download_file(photo_info.file_path)
        #photo_out = bot.download_file(photo_info.file_path)

        bgr = cv2.imread('test.jpg')
        wm = 'test'
        encoder = WatermarkEncoder()
        encoder.set_watermark('bytes', wm.encode('utf-8'))
        bgr_encoded = encoder.encode(bgr, 'dwtDctSvd')
        dwnld_photo = bot.download_file('test.jpg')
        cv2.imwrite(dwnld_photo, bgr_encoded)
        bot.send_photo(photo.chat.id, dwnld_photo)

        # decoder = WatermarkDecoder('bytes', 32)
        # watermark = decoder.decode(bgr, 'dwtDctSvd')
        # print(watermark.decode('utf-8'))
    except Exception as ex:
        bot.send_message(photo.chat.id, "Error: " + ex)


@bot.message_handler(content_types=['photo'])
def edit_photo(photo):
    has_wm(photo)
    #if has_wm(photo):
        #print("Photo has a WM!")
    #else:
        #print("Photo hasn't a WM!")


bot.infinity_polling()
