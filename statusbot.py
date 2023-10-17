import os
import time
from telethon.sync import TelegramClient
from telethon.tl import functions, types
import pandas as pd
import csv


api_id = '28134127'
api_hash = '2b96ba5a07fc201eac8f236e5a879d25'

# TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
# TeleBot(token=TELEGRAM_TOKEN)

# bot_token = '6431040317:AAFDFv2R_qBsv9JuVUDzTIyXHOu5l1sUUwc'

# TODO: fix the data

timeout_seconds = 600
current_directory = os.path.dirname(os.path.realpath(__file__))
relative_path = "text2speech_module/data.csv"
csv_file_path = os.path.join(current_directory, relative_path)

def send_image_to_bot(client, chat_id, image_path):
    try:
        with open(image_path, 'rb') as file:
            client.send_file(chat_id, file)
    except Exception as e:
        print(f"Error sending image to bot: {e}")

def generate_expected_filename(artist_name, artwork_title):
    expected_filename = f"{artist_name} - {artwork_title}"
    return expected_filename

def check_audio_generation(client, chat_id, artist_name, artwork_title):
    start_time = time.time()
    expected_filename = generate_expected_filename(artist_name, artwork_title)

    while True:
        if time.time() - start_time > timeout_seconds:
            print("Timeout: Audio not generated within the specified time.")
            return "Timeout: Audio not generated within the specified time."

        messages = client.get_messages(chat_id)
        for message in messages:
            if isinstance(message, types.Message):
                if message.audio:
                    audio = message.audio
                    if audio.attributes and audio.attributes[0].title:
                        file_name = audio.attributes[0].title
                        if expected_filename in file_name:
                            print(f"Matching audio file found: {file_name}")
                            return f"Matching audio file found: {file_name}"
                        else:
                            print(f"Unexpected audio file found: {file_name}")
                            return f"Unexpected audio file found: {file_name}"
                    else:
                        print("Audio title is missing or None.")
                        return "Audio title is missing or None."

def main():
    with TelegramClient('anon', api_id, api_hash) as client:
        chat_id = 'harbour_art_guide_bot'
        df = pd.read_csv(csv_file_path)
        num_samples = min(5, len(df))

        for i in range(num_samples):
            row = df.iloc[i]
            image_path = row['Img']
            artist_name = row['Author']
            artwork_title = row['Title']

            relative_path2 = "data/"

            send_image_to_bot(client, chat_id, relative_path2 + image_path)
            result = check_audio_generation(client, chat_id, artist_name, artwork_title)
            print(result)

if __name__ == '__main__':
    main()
