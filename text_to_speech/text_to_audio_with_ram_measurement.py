import os
import time
import psutil
from gtts import gTTS
from IPython.display import Audio

def text_to_audio(text, language='en', slow=False, filename="output.mp3"):
    """
    Convert a given text to audio and save it to a file.

    Args:
        text (str): The text to convert to audio.
        language (str): Language in which to convert the text (default is 'en' for English).
        slow (bool): Whether the audio should be slow (default is False).
        filename (str): Name of the output audio file (default is "output.mp3").
    """
    # Get the current time before creating the audio
    start_time = time.time()

    # Get the current RAM usage before creating the audio
    initial_ram_usage = psutil.virtual_memory().used

    audio_converter = gTTS(text=text, lang=language, slow=slow)
    audio_converter.save(filename)
    os.system(f"mpg321 {filename}")

    # Calculate runtime
    end_time = time.time()
    runtime = end_time - start_time

    # Get the RAM usage after creating the audio
    final_ram_usage = psutil.virtual_memory().used
    ram_usage_increase = final_ram_usage - initial_ram_usage

    print("Runtime and RAM Usage:")
    print(f"Runtime: {runtime:.4f} seconds")
    print(f"Initial RAM Usage: {initial_ram_usage} bytes")
    print(f"Final RAM Usage: {final_ram_usage} bytes")
    print(f"RAM Usage Increase: {ram_usage_increase} bytes")

    return Audio(filename)

# Example usage
mytext = 'Welcome to Habour.Space Project!'
audio_output = text_to_audio(mytext, slow=False, filename="welcome.mp3")
audio_output
