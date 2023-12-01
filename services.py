import requests
from PIL import Image

from descriptor_module.descriptor import describe
from text2speech_module.google_text_to_speech import text_to_audio
from reverse_image_search_module.search_image import find_image
from image_crop_module.croper import crop_image

# plt
import numpy as np
import json

def get_image_name_from_url(image_url):
    image_name = image_url.split("/")[-1]
    return image_name


def run_all_models(filename, photo_url):
    image = Image.open(requests.get(photo_url, stream=True).raw)

    cropped_image = crop_image(image)

    _, distance, metadata = find_image(cropped_image)

    # save some steps to debug
    image_filename = 'cache/cropped_'+get_image_name_from_url(photo_url)

    pil_img = Image.fromarray((cropped_image * 255).astype(np.uint8))
    pil_img.save(image_filename)

    if distance < 0.9:
        return {'error': "Sorry, I couldn't find a match for that image.",
                'distance': distance,
                'cropped_img': image_filename,
                'metadata': json.dumps(metadata, indent=2)}

    description_text = describe(metadata)['description']

    filename = 'cache/'+metadata.get('author_name') + \
               ' - ' + \
               metadata.get('title')

    text_to_audio(description_text, filename=filename)

    return {'audio_filename': filename,
            'error': None,
            'cropped_img': image_filename,
            'distance': distance,
            'metadata': json.dumps(metadata, indent=2)}
