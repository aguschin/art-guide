import os
from PIL import Image
from ..croper import crop_image


DATA_MOST_CROP_PATH = '../../data/most_crop/'
DATA_MOST_NOT_CROP_PATH = '../../data/most_no_crop/'


def test_ratio_non_cropable_images():
    image_list = os.listdir(DATA_MOST_NOT_CROP_PATH)

    total, croped = len(image_list), 0

    for image_name in image_list:
        image_path = os.path.join(DATA_MOST_NOT_CROP_PATH, image_name)

        image = Image.open(image_path)


def test_ratio_cropable_images():
    assert True
