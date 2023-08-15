import asyncio

from telebot.async_telebot import AsyncTeleBot
from decouple import config

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
    await bot.send_message(message.chat.id, "Image received. Processing...")


asyncio.run(bot.infinity_polling())
