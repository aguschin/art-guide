from io import BytesIO

import requests
import telebot
from decouple import config
from matplotlib import pyplot as plt

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = """Hi. This bot will accept an image of a painting and it will send you back an audio and text with a
        description of it, talking about its name, author, date, etc.\n\

        To use it, just upload an image and you will receive the audio and text.\n\
        """

    bot.reply_to(message, text)


@bot.message_handler(content_types=['photo'])
def handle_image(message):
    image = message.photo[-1]

    try:
        file_id = image.file_id
        file_info = bot.get_file(file_id)
        file_link = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        response = requests.get(file_link)
    except:
        print("Error fetching the image.")

    try:
        image = BytesIO(response.content)
        img = plt.imread(image, format="auto")
        plt.imshow(img)
        plt.axis('off')
        plt.show()
    except:
        print("Error plotting the image.")

    bot.send_message(message.chat.id, "Image received. Processing...")


bot.infinity_polling()
