from copy import copy
from .on_fly_pyttsx3 import pyttsx3_text_to_audio
from .suno_bark_tts import suno_bark_tts
from gtts_tts import gtts_text_to_audio

# engine : pyttsx3, gtts, suno_bark


def text_to_speech(INPUT_TEXT: str, index: int, engine: str = 'pyttsx3'):
    output = ''

    if engine == 'pyttsx3':
        output = pyttsx3_text_to_audio(INPUT_TEXT, index)
    elif engine == 'suno_bark':
        output = suno_bark_tts(INPUT_TEXT, index)
    elif engine == 'gtts':
        output = gtts_text_to_audio(INPUT_TEXT, index)
    else:
        assert False, f'engine value {engine} not found'

    return {'audio_wave': output}