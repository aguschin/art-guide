import os
import random
from PIL import Image
from ..search_image import find_index_from_image, find_file_name
from ..resnet18 import gen_multi_cropping
import logging


logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()


DATA_IMAGES_PATH = 'data/img/full/'
K_CROPPING = 10
N_SEARCH = 10
IMAGE_MAX_NUMBER = 5000

def get_image_matching_many(image_names):
    positive = 0

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
            positive += 1
        else:
            mylogger.info(f"Not a match in {K_CROPPING} <original>{_im} <distance>{selected_dist}")

    return positive

def get_image_matching_single(image_names, th=0.0):
    positive = 0

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
                positive += 1
            else:
                mylogger.info(f"Not a match in n={N_SEARCH} <original>{_im}")
            
        except Exception as ex:
            mylogger.info(f'image {_im} error')
            mylogger.info(str(ex))

    return positive


# todo: images names to random
def test_random_cropp_many_one_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = get_image_matching_many(images_names)

    acc = positive / 100

    mylogger.info(f"MultiCropping: many to one: ACCURACY = {acc} K = {K_CROPPING}")

    assert acc > 0.99

def test_random_cropp_one_to_many_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = get_image_matching_single(images_names)

    acc = positive / 100

    mylogger.info(f"MultiCropping: one to many: ACCURACY = {acc} N = {N_SEARCH}")

    assert acc > 0.88

def test_random_cropp_many_to_many_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = get_image_matching_many(images_names)

    acc = positive / 100

    mylogger.info(f"MultiCropping: many to many: ACCURACY = {acc} K = {K_CROPPING} N = {N_SEARCH}")

    assert acc > 0.99


def test_random_cropp_one_to_many_distance9_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = get_image_matching_single(images_names, 0.9)

    acc = positive / 100

    mylogger.info(f"MultiCropping: one to many distance 0.9 : ACCURACY = {acc} N = {N_SEARCH}")

    assert acc > 0.88