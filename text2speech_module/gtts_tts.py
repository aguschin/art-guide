from gtts import gTTS
import os


def gtts_text_to_audio(text: str, index: int):
    """
    Convert a given text to audio and save it to a file using gTTS (Google Text-to-Speech).
    Args:
        text (str): The text to convert to audio.
        index (int): Index for the output audio file naming.
        lang (str): Language in which to convert the text (default is 'en' for English).
        slow (bool): Whether the audio should be slow (default is False).
    """
    lang = 'en'
    slow = False

    # Generate the audio using gTTS
    tts = gTTS(text=text, lang=lang, slow=slow)

    filename = f"{index}.mp3"
    filepath = os.path.join("output_folder", filename)  # Change "output_folder" to your desired output folder

    # Save the generated audio to the file
    tts.save(filepath)

    return f"Audio file '{filename}' generated successfully."


# Example usage
my_text = "Welcome to Harbour.Space Project!"
result = gtts_text_to_audio(my_text, index=0)
print(result)  # Output: "Audio file '0.mp3' generated successfully."
