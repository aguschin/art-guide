import os
import time

from decouple import config
from telethon.sync import TelegramClient
from telethon.tl import types

API_ID = config("API_ID") or os.environ["API_ID"]
API_HASH = config("API_HASH") or os.environ["API_HASH"]
PHONE = config("PHONE") or os.environ["PHONE"]


timeout_seconds = 600

current_directory = os.path.dirname(os.path.realpath(__file__))
data_folder = "data"
image_filename = "leo.jpg"


def send_image_to_bot(client, chat_id, image_path):
    try:
        with open(image_path, "rb") as file:
            client.send_file(chat_id, file)
    except Exception as e:
        print(f"Error sending image to bot: {e}")


def generate_expected_filename(artist_name, artwork_title):
    expected_filename = f"{artist_name} - {artwork_title}"
    return expected_filename


def check_audio_generation(client, chat_id, timeout_seconds):
    start_time = time.time()
    expected_filename = generate_expected_filename("Leonardo da Vinci", "Mona Lisa")

    while time.time() - start_time < timeout_seconds:
        messages = client.iter_messages(chat_id)
        last_message = list(messages)[0]

        if (
            isinstance(last_message, types.Message)
            and last_message.media
            and isinstance(last_message.media, types.MessageMediaPhoto)
        ):
            # print("Bot isn't functional")
            return "Bot isn't functional"
        elif last_message.message == "Sorry, I couldn't find a match for that image.":
            # print("No audio file generated for that artist")
            return "No audio file generated for that artist"
        elif last_message.media and isinstance(
            last_message.media, types.MessageMediaDocument
        ):
            document = last_message.media.document
            if document.mime_type == "audio/mpeg" and document.attributes:
                for attribute in document.attributes:
                    if isinstance(attribute, types.DocumentAttributeFilename):
                        file_name = attribute.file_name
                        # print(f"Generated audio file name: {file_name}")

                        if expected_filename in file_name:
                            # print(f"Matching audio file found: {file_name}")
                            return f"Matching audio file found: {file_name}"
                        else:
                            # print(f"Unexpected audio file found: {file_name}")
                            return f"Unexpected audio file found: {file_name}"


def main():
    with TelegramClient("anon", API_ID, API_HASH) as client:
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(PHONE)
            client.sign_in(PHONE, input("Enter code: "))
        chat_id = "harbour_art_guide_bot"
        image_path = os.path.join(current_directory, data_folder, image_filename)

        send_image_to_bot(client, chat_id, image_path)
        time.sleep(10)
        result = check_audio_generation(client, chat_id, timeout_seconds)
        print(result)


if __name__ == "__main__":
    main()
