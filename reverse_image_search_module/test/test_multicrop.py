import os
import numpy as np
import random
from PIL import Image
from ..search_image import find_index_from_image, find_file_name
import logging
import matplotlib.pyplot as plt
from datetime import datetime


logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()


DATA_IMAGES_PATH = 'data/img/full/'
K_CROPPING = 10
IMAGE_MAX_NUMBER = 5000


def random_cropping(image_width, image_height, min_size, K):
    for _ in range(K):
        x_ini = random.randint(0, image_width - min_size)
        y_ini = random.randint(0, image_height - min_size)

        x_end = random.randint(x_ini + min_size, image_width)
        y_end = random.randint(y_ini + min_size, image_height)

        yield x_ini, y_ini, x_end, y_end


def get_image_matching(image_names):
    positive = 0
    not_a_match = 0

    probs = []

    for _im in image_names:
        try:
            image = Image.open(os.path.join(DATA_IMAGES_PATH, _im))
            # to check the size and truncation
            _ = image.resize((255, 255))
        except Exception as ex:
            mylogger.info(f'image {_im} load error')
            mylogger.info(str(ex))
            continue
        
        matching_rate = 0

        for x_ini, y_ini, x_end, y_end in random_cropping(255,255, 200, K_CROPPING):
            image_croped = image.crop((x_ini, y_ini, x_end, y_end))

            idx, _ = find_index_from_image(image_croped, n=1)
            idx = idx[0]

            file_name = find_file_name(idx)

            if file_name == _im:
                positive += 1
                matching_rate += 1
        
        if matching_rate == 0:
            not_a_match += 1
            # Uncomment this if need it
            # mylogger.info(f"Not a match in {K_CROPPING} <original>{_im}")
        
        matching_rate /= K_CROPPING
        probs.append(matching_rate)

    return positive, not_a_match, probs


def test_random_cropp_many_one_images():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:100]

    positive, not_a_match, probs = get_image_matching(images_names)

    acc = positive / (100 * K_CROPPING)
    not_a_match /= 100

    mylogger.info(f"MultiCropping: many to one: ACCURACY = {acc} K = {K_CROPPING} Not a Match = {not_a_match}")

    current_time = datetime.now()
    time_string = current_time.strftime("%Y%m%d_%H%M%S")
    filename = f"test_multi_to_one_histogram_{time_string}.png"
    
    plt.hist(probs, bins=20, color='blue', edgecolor='black')
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram of Acc per picture')
    plt.savefig(filename)

    mylogger.info(filename)

    # todo Add correct assert,
    assert True