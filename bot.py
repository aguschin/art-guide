import asyncio
import os

from telebot.async_telebot import AsyncTeleBot
from decouple import config

from descriptor_module.descriptor import describe
from text_to_speech.google_text_to_speech import text_to_audio

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
bot = AsyncTeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
async def send_welcome(message):
    text = \
"""
    Hi. This bot will accept an image of a painting and it will send you back an audio and text with a description of it, talking about its name, author, date, etc.\n\
    
    To use it, just upload an image and you will receive the audio and text.\n\
"""

    await bot.reply_to(message, text)


@bot.message_handler(content_types=['photo'])
async def handle_image(message):
    image = message.photo[-1]

    filename = str(message.chat.username) + "_" + str(message.chat.id) + "_" + str(message.id) + ".mp3"

    await bot.send_message(message.chat.id, "Image received. Processing...")

    description_text = describe(
        {
            'author_name': 'Leonardo Da Vinci',
            'art_name': 'La Gioconda',
            'type': 'portrait',
            'style': 'Renaissance',
            'objects': [],
            'period': '',
            'date': ''
        }
    )['description']

    text_to_audio(description_text, filename=filename)
    audio = open(filename, 'rb')
    await bot.send_audio(message.chat.id, audio)
    audio.close()
    os.system(f"rm {filename}")


asyncio.run(bot.infinity_polling())
