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


def run_all_models(filename, photo_url, verbose=False, k_neibours=1):
    k_neibours = 1 if not verbose else k_neibours

    image = Image.open(requests.get(photo_url, stream=True).raw)

    cropped_image = crop_image(image)

    # _, list of distances, list of metadata
    _, distance, metadata = find_image(cropped_image, n=k_neibours)

    # save some steps to debug
    if verbose:
        image_filename = 'cache/cropped_'+get_image_name_from_url(photo_url)

        pil_img = Image.fromarray((cropped_image * 255).astype(np.uint8))
        pil_img.save(image_filename)

    if distance[0] < 0.9:
        return_body = {'error': "Sorry, I couldn't find a match for that image."}

        if verbose:
            return_body.update({ 'distance': json.dumps(distance, indent=2),
                                 'cropped_img': image_filename,
                                 'metadata': json.dumps(metadata, indent=2)})
        
        return return_body
    
    description_text = describe(metadata[0])['description']

    filename = 'cache/'+metadata.get('author_name') + \
               ' - ' + \
               metadata.get('title')

    text_to_audio(description_text, filename=filename)

    return_body = {'audio_filename': filename, 'error': None}

    if verbose:
        return_body.update({ 'cropped_img': image_filename,
                             'distance': json.dumps(distance, indent=2),
                             'metadata': json.dumps(metadata, indent=2)})

    return return_body
