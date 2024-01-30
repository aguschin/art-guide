import logging
import os
import random

import numpy as np
from PIL import Image
from sklearn.metrics import precision_recall_curve

from ..utils.utils import make_syntetic_first_second_distances

DATA_IMAGES_PATH = "data/img/full/"
IMAGE_MAX_NUMBER = 5000


logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()

load_vector_db(False, reload=True)


def get_image_idx_name_matching(images_names):
    positive = 0

    for _im in images_names:
        try:
            image = Image.open(os.path.join(DATA_IMAGES_PATH, _im))
            # to check the size and truncation
            _ = image.resize((255, 255))
        except Exception as ex:
            mylogger.info(f"image {_im} load error")
            mylogger.info(str(ex))
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


def test_precision_recall():
    y_test, y_score = make_syntetic_first_second_distances(DATA_IMAGES_PATH, n=5000)
    precision, recall, thresholds = precision_recall_curve(y_test, y_score)

    # find recall value with 0.9 of presition value
    index = np.searchsorted(precision, 0.9, side="left")
    if index > precision.shape[0]:
        index = precision.shape[0] - 1

    recall_idx = recall[index]

    mylogger.info(f"test presition/recall presition value {precision[index]}")
    mylogger.info(f"test presition/recall recall value {recall_idx}")
    mylogger.info(f"test presition/recall threshold value {thresholds[index]}")

    assert recall_idx > 0.6
