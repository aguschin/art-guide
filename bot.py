import os

import requests
from decouple import config
from telebot import TeleBot

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
bot = TeleBot(token=TELEGRAM_TOKEN)

DEBUG = bool(config("DEBUG"))
API_PORT = int(config("API_PORT"))


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    text = """
    Hi. This bot will accept an image of a painting and it will send you back an audio and text with a description of it, talking about its name, author, date, etc.\n\

    To use it, just upload an image and you will receive the audio and text.\n\
"""

    bot.reply_to(message, text)


@bot.message_handler(content_types=["photo"])
def handle_image(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)

    bot.send_message(message.chat.id, "Image received. Processing...")

    # Construct the URL for downloading the photo
    photo_url = (
        f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"
    )

    filename = (
        str(message.chat.username)
        + "_"
        + str(message.chat.id)
        + "_"
        + str(message.id)
        + ".mp3"
    )

    response = requests.get(
        f"http://localhost:{API_PORT}/process_image/",
        json={"filename": filename, "photo_url": photo_url},
    )

    # some information for debug
    if DEBUG:
        img_crp = response.json().get("cropped_img")
        kn_distance = response.json().get("distance")
        metadata = response.json().get("metadata")

        bot.send_message(message.chat.id, f"DB: Distance {kn_distance}")
        bot.send_message(message.chat.id, f"DB: Metadata")
        bot.send_message(message.chat.id, metadata)

        with open(img_crp, "rb") as photo_crp:
            bot.send_photo(
                message.chat.id, photo=photo_crp, caption="DB: Cropped image"
            )

    if response.json().get("error"):
        print("Error:", response.json().get("error"))
        bot.send_message(message.chat.id, response.json().get("error"))
        return

    if response.status_code == 200:
        filename = response.json().get("audio_filename")
        audio = open(filename, "rb")
        bot.send_audio(message.chat.id, audio)
        audio.close()
        os.system(f"rm {filename}")
    else:
        print(response.content)
        print("Error calling API.")


bot.infinity_polling()
