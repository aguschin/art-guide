import os

import requests
from PIL import Image

from telebot import TeleBot
from decouple import config

from descriptor_module.descriptor import describe
from text2speech_module.google_text_to_speech import text_to_audio

from reverse_image_search_module.search_image import find_image

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
bot = TeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = \
"""
    Hi. This bot will accept an image of a painting and it will send you back an audio and text with a description of it, talking about its name, author, date, etc.\n\
    
    To use it, just upload an image and you will receive the audio and text.\n\
"""

    bot.reply_to(message, text)


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)

    bot.send_message(message.chat.id, "Image received. Processing...")

    # Construct the URL for downloading the photo
    photo_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"
    print("URL:", photo_url)

    image = Image.open(requests.get(photo_url, stream=True).raw)

    _, distance, metadata = find_image(image)

    print("Distance:", distance)

    if distance < 0.9:
        bot.send_message(message.chat.id, "Sorry, I couldn't find a match for that image.")
        return

    description_text = describe(metadata)['description']

    filename = str(message.chat.username) + "_" + str(message.chat.id) + "_" + str(message.id) + ".mp3"
    text_to_audio(description_text, filename=filename)
    audio = open(filename, 'rb')
    bot.send_audio(message.chat.id, audio)
    audio.close()
    os.system(f"rm {filename}")

bot.infinity_polling()
