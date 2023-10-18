import os
import random
from PIL import Image
from ..search_image import find_index_from_image, find_file_name
import logging


DATA_IMAGES_PATH = 'data/img/full/'
IMAGE_MAX_NUMBER = 5000


logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()


def get_image_idx_name_matching(images_names):
    positive = 0

    for _im in images_names:
        try:
            image = Image.open(os.path.join(DATA_IMAGES_PATH, _im))
        except Exception as ex:
            mylogger.error(f'image {_im} load error')
            mylogger.error(str(ex))
            continue

        idx, dist = find_index_from_image(image, n=1)
        idx = idx[0]

        file_name = find_file_name(idx)

        if file_name == _im:
            positive += 1
        else:
            mylogger.info(f"UNMATCHED <original>{_im} <matched>{file_name}")

    return positive


def test_static_accuracy():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive = get_image_idx_name_matching(images_names)

    acc = positive / 100

    mylogger.info(f"test_static_acc: ACCURACY = {acc}")

    assert acc > 0.98


def test_static_accuracy_random():
    images_names = os.listdir(DATA_IMAGES_PATH)

    random.shuffle(images_names)

    images_names = images_names[:IMAGE_MAX_NUMBER]

    positive = get_image_idx_name_matching(images_names)

    acc = positive / IMAGE_MAX_NUMBER

    mylogger.info(f"test_static_acc (random): ACCURACY = {acc}")

    assert acc > 0.98
