import requests
from PIL import Image

from descriptor_module.descriptor import describe
from text2speech_module.google_text_to_speech import text_to_audio
from reverse_image_search_module.search_image import find_image

def run_all_models(filename, photo_url):
    image = Image.open(requests.get(photo_url, stream=True).raw)

    _, distance, metadata = find_image(image)

    print("Distance:", distance)

    if distance < 0.9:
        return {'error': "Sorry, I couldn't find a match for that image."}

    description_text = describe(metadata)['description']

    text_to_audio(description_text, filename=filename)

    return {'audio_filename': filename, 'error': None}
