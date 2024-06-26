import json

import numpy as np
import requests
from PIL import Image

from descriptor_module.descriptor import describe
from image_crop_module.croper import crop_image
from reverse_image_search_module.search_image import find_image
from text2speech_module.google_text_to_speech import text_to_audio


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
    image_filename = "cache/cropped_" + get_image_name_from_url(photo_url)
    pil_img = Image.fromarray((cropped_image).astype(np.uint8))
    pil_img.save(image_filename)

    if distance[0] < 0.8:
        return_body = {"error": "Sorry, I couldn't find a match for that image."}

        if verbose:
            return_body.update(
                {
                    "distance": json.dumps(distance, indent=2),
                    "cropped_img": image_filename,
                    "metadata": json.dumps(metadata, indent=2),
                }
            )

        return return_body

    description_text = describe(metadata[0])["description"]

    filename = (
        "cache/" + metadata[0].get("author_name") + " - " + metadata[0].get("title")
    )

    text_to_audio(description_text, filename=filename)

    return_body = {"audio_filename": filename, "error": None}

    return_body.update(
        {
            "cropped_img": image_filename,
            "distance": json.dumps(distance, indent=2),
            "metadata": json.dumps(metadata, indent=2),
        }
    )

    return return_body


def run_all_models_web(image):
    cropped_image = crop_image(image)

    _, distance, metadata = find_image(cropped_image, n=1)

    if distance[0] < 0.86:
        return cropped_image, "Sorry, I couldn't find a match for that image."

    description_text = describe(metadata[0])["description"]

    # text_to_audio(description_text, filename=filename)

    return cropped_image, description_text
