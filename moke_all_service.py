#%%
import requests
from PIL import Image

from descriptor_module.descriptor import describe
from text2speech_module.google_text_to_speech import text_to_audio
from reverse_image_search_module.search_image import find_image
from image_crop_module.croper import crop_image

import matplotlib.pyplot as plt
import numpy as np

#%%

image = Image.open('tests/imgs/test_mona.jpg')
photo_url = 'dasd.png'

#%%

# todo delete
plt.imsave('cache/im1.png', image)

cropped_image = crop_image(image)

#%%

print(type(cropped_image), cropped_image.shape)

plt.imsave('cache/im2.png', cropped_image)

#%%

# only to debug

_, distance, metadata = find_image(cropped_image)

#%%

# save some steps to debug
image_filename = f'cache/cropped_{photo_url}'

pil_img = Image.fromarray((cropped_image * 255).astype(np.uint8))
pil_img.save(image_filename)

#%%

if distance < 0.9:
    assert False

description_text = describe(metadata)['description']

filename = 'cache/'+metadata.get('author_name') + \
            ' - ' + \
            metadata.get('title')

text_to_audio(description_text, filename=filename)
# %%
