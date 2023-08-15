import os
from gtts import gTTS
from IPython.display import Audio

async def text_to_audio(text, language='en', slow=False, filename="output.mp3"):
    """
    Convert a given text to audio and save it to a file.

    Args:
        text (str): The text to convert to audio.
        language (str): Language in which to convert the text (default is 'en' for English).
        slow (bool): Whether the audio should be slow (default is False).
        filename (str): Name of the output audio file (default is "output.mp3").
    """
    audio_converter = gTTS(text=text, lang=language, slow=slow)
    await audio_converter.save(filename)
    return Audio(filename)

# Example usage
mytext = 'Welcome to Habour.Space Project!'
audio_output = text_to_audio(mytext, slow=False, filename="welcome.mp3")
