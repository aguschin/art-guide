from PIL import Image

from descriptor_module.descriptor import describe
from image_crop_module.croper import crop_image
from reverse_image_search_module.search_image import find_image
from text2speech_module.google_text_to_speech import text_to_audio

image = Image.open("tests/imgs/test_mona.jpg")
k_neibours = 5

cropped_image = crop_image(image)

_, distance, metadata = find_image(cropped_image, n=k_neibours)

print(distance, len(metadata), metadata[0])
