import os
from PIL import Image
from ..search_image import find_index_from_image, find_file_name, load_vector_db
from ..resnet18 import gen_multi_cropping
import logging


logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()


DATA_IMAGES_PATH = 'data/img/full/'
K_CROPPING = 6
N_SEARCH = 10
IMAGE_MAX_NUMBER = 5000

load_vector_db(True, reload=True)

def is_in_reference_many(image_names):
    positive = []

    for _im in image_names:
        try:
            image = Image.open(os.path.join(DATA_IMAGES_PATH, _im))
            # to check the size and truncation
            _ = image.resize((255, 255))
        except Exception as ex:
            mylogger.info(f'image {_im} load error')
            mylogger.info(str(ex))
            continue
        
        
        idxs, dists = [], []

        for x_ini, y_ini, x_end, y_end in gen_multi_cropping(image.width, image.height, K_CROPPING):
            image_croped = image.crop((x_ini, y_ini, x_end, y_end))

            idx, dist = find_index_from_image(image_croped, n=N_SEARCH)
            idx, dist = idx[0], dist[0]
            
            idxs.append(idx)
            dists.append(dist)
        
        selected_idx, selected_dist = max(zip(idxs, dists), key=lambda x: x[1])

        file_name = find_file_name(selected_idx)

        if file_name == _im:
            positive.append(1)
        else:
            positive.append(0)
            mylogger.info(f"Not a match in {K_CROPPING} <original>{_im} <distance>{selected_dist}")

    return positive

def is_in_reference_single(image_names, th=0.0):
    positive = []

    for _im in image_names:
        try:
            image = Image.open(os.path.join(DATA_IMAGES_PATH, _im))
            # to check the size and truncation
            _ = image.resize((255, 255))
        
            idx, dist = find_index_from_image(image, n=N_SEARCH)
            idx = idx[0]
            dist = dist[0]

            file_name = find_file_name(idx)

            if file_name == _im and dist >= th:
                positive.append(1)
            else:
                positive.append(0)
                mylogger.info(f"Not a match in n={N_SEARCH} <original>{_im}")
            
        except Exception as ex:
            mylogger.info(f'image {_im} error')
            mylogger.info(str(ex))

    return positive


# ----------------------------------------------------------------------------------------------------

'''
Many to many:
    Many cropings including the original image 
        to 
    Multi embedding reference (embeding with the original image + cropings of it)

One to many:
    Original image 
        to
    Multi embedding reference (embeding with the original image + cropings of it)
'''

def test_random_cropp_one_to_many_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = is_in_reference_single(images_names)

    acc = sum(positive) / len(positive)

    mylogger.info(f"MultiCropping: one to many: ACCURACY = {acc} N = {N_SEARCH}")

    assert acc > 0.88

def test_random_cropp_many_to_many_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = is_in_reference_many(images_names)

    acc = sum(positive) / len(positive)

    mylogger.info(f"MultiCropping: many to many: ACCURACY = {acc} K = {K_CROPPING} N = {N_SEARCH}")

    assert acc > 0.99


def test_random_cropp_one_to_many_distance9_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = is_in_reference_single(images_names, 0.9)

    acc = sum(positive) / len(positive)

    mylogger.info(f"MultiCropping: one to many distance 0.9 : ACCURACY = {acc} N = {N_SEARCH}")

    assert acc > 0.88