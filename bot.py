import json
import os
from time import sleep

import numpy as np
import requests
from decouple import config
from telebot import TeleBot

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
bot = TeleBot(token=TELEGRAM_TOKEN)

DEBUG = config("DEBUG") == "True"
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

    # bot.send_message(message.chat.id, "Image received. Processing...")
    # bot.send_message(
    #     message.chat.id,
    #     "Debug mode enabled: I'm going to send you cosine similarity values for the closest matches, "
    #     "and then send information about the closest artworks and the cropping result. "
    #     "If I'll be confident about results, I'll send the audio with the description."
    # )
    bot.send_message(
        message.chat.id,
        f"Image received. This will take up to 30s since we're running this on CPU.",
    )
    sleep(0.1)
    bot.send_message(message.chat.id, f"Let's crop the image first:")

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
        kn_distance = json.loads(kn_distance)
        kn_distance = [np.round(i, 4) for i in kn_distance]
        metadata = response.json().get("metadata")
        metadata = [
            {"cosine_distance": d}
            | {
                k: v
                for k, v in i.items()
                if k in ["author_name", "title", "url", "image_url"]
            }
            for i, d in zip(json.loads(metadata), kn_distance)
        ]
        #     "author_name": "Gerard van Honthorst",
        #     "style": "Baroque",
        #     "date": NaN,
        #     "id": 13193,
        #     "url": "https://www.wikiart.org/en/gerard-van-honthorst/the-nativity",
        #     "title": "The Nativity",
        #     "original_title": NaN,
        #     "series": NaN,
        #     "genre": "religious painting",
        #     "media": NaN,
        #     "location": NaN,
        #     "dimension": NaN,
        #     "description": NaN,
        #     "tags": "Pictureframe,Stockphotography",
        #     "image_url": "https://uploads1.wikiart.org/00310/images/gerard-van-honthorst/the-nativity-by-gherard-delle-notti-in-exeter-cathedral-3.JPG!Large.JPG",
        #     "file_name": "9f394314215af506c4ab7097ba4f7abb69cbb1e8.jpg"

        # bot.send_message(message.chat.id, f"Let's crop the image first:")
        with open(img_crp, "rb") as photo_crp:
            bot.send_photo(message.chat.id, photo=photo_crp, caption="")
        sleep(1)
        # bot.send_message(message.chat.id, f"Now let's run the similarity search. The closest artworks found have cosine distance of {kn_distance}")
        bot.send_message(
            message.chat.id,
            f"Let's see the top search results, starting from the most probable:",
        )
        for j, i in enumerate(metadata):
            m = json.dumps(i)
            for x in range(0, len(m), 4095):
                bot.send_message(message.chat.id, f"{j+1} result: " + m[x : x + 4095])
            sleep(1)
    bot.send_message(
        message.chat.id,
        f"Ok, now let's check if we are confident with search results... If we are, I'll send you an audio below.",
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
        # os.system(f"rm {filename}")
    else:
        print(response.content)
        print("Error calling API.")


bot.infinity_polling()
