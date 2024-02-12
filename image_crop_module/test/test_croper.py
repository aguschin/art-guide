import logging
import os
from time import time

from PIL import Image

from ..distortion_sam_croper import distortion_crop_image

DATA_MOST_CROP_PATH = "./data/most_crop/"
DATA_MOST_NOT_CROP_PATH = "./data/most_no_crop/"


logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()


def test_distortion_croper():
    image_list = os.listdir(DATA_MOST_NOT_CROP_PATH)[0]
    image_path = os.path.join(DATA_MOST_NOT_CROP_PATH, image_list)

    image = Image.open(image_path)
    _, proportion = distortion_crop_image(image)

    mylogger.info(f"test_distortion_croper: proportion={proportion}")

    assert proportion > 0.0 and proportion <= 1.0


def calculate_croped_number(path, threshold=0.9, fail=True, log=True):
    image_list = os.listdir(path)

    total, croped = len(image_list), 0

    for image_name in image_list:
        image_path = os.path.join(path, image_name)

        image = Image.open(image_path)

        try:
            _, proportion = distortion_crop_image(image)
        except Exception as ex:
            print(image_name)
            raise ex

        if proportion < threshold or proportion > 1.0:
            croped += 1

            if not fail and log:
                mylogger.info(
                    f"Area Proportion image not fail at {threshold}-({proportion}) : {image_name}"
                )

        elif fail and log:
            mylogger.info(
                f"Area Proportion image fail at {threshold}-({proportion}) : {image_name}"
            )

    return croped / total


def test_ratio_non_cropable_images():
    proportion = calculate_croped_number(
        DATA_MOST_NOT_CROP_PATH, threshold=0.9, fail=False
    )
    mylogger.info(f"test_ratio_non_cropable_images: proportion={proportion}")

    assert proportion < 0.1


def test_ratio_cropable_images():
    proportion = calculate_croped_number(DATA_MOST_CROP_PATH, threshold=0.9, fail=True)

    mylogger.info(f"test_ratio_cropable_images: proportion={proportion}")

    assert proportion > 0.9


def test_croper_time_rate():
    TIME_RATE = 1.5 * 60  # mean minutes per operation

    total = len(os.listdir(DATA_MOST_NOT_CROP_PATH)) + len(
        os.listdir(DATA_MOST_CROP_PATH)
    )

    initial_time = time()

    _ = calculate_croped_number(DATA_MOST_NOT_CROP_PATH, threshold=1.0, log=False)
    _ = calculate_croped_number(DATA_MOST_CROP_PATH, threshold=1.0, log=False)

    dt = time() - initial_time
    rate = dt / total

    mylogger.info(f"test_croper_time_rate: rate={rate}")

    assert rate < TIME_RATE
