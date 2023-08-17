import pyttsx3
from IPython.display import Audio


def text_to_audio(text, rate=150, volume=0.9, filename="output.mp3"):
    """
    Convert a given text to audio and save it to a file.
    Args:
        text (str): The text to convert to audio.
        language (str): Language in which to convert the text (default is 'en' for English).
        slow (bool): Whether the audio should be slow (default is False).
        filename (str): Name of the output audio file (default is "output.mp3").
    # Example usage
    # mytext = 'Welcome to Habour.Space Project!'
    # text_to_audio(mytext, slow=False, filename="welcome.mp3")
    """

    # Initialize the text-to-speech engine
    audio_converter = pyttsx3.init()

    # Set properties (optional)
    audio_converter.setProperty("rate", rate) # Speed of speech (words per minute)
    audio_converter.setProperty("volume", volume) # Volume level (0.0 to 1.0)

    # Convert the text to speech
    audio_converter.save_to_file(text, filename)

    # Wait until above command is finished.
    audio_converter.runAndWait()