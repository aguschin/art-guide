import os
from time import time
import logging
from PIL import Image
from ..distortion_croper import distortion_crop_image


DATA_MOST_CROP_PATH = 'data/most_crop/'
DATA_MOST_NOT_CROP_PATH = 'data/most_no_crop/'


def get_logs_handle():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - \
                                %(levelname)s - %(message)s')

    logger = logging.getLogger('test_cropper')

    file_handler = logging.FileHandler('testcropper.log')
    logger.addHandler(file_handler)

    return logger, file_handler


LOGGER, _ = get_logs_handle()


def test_distortion_croper():
    global LOGGER

    image_list = os.listdir(DATA_MOST_NOT_CROP_PATH)[0]
    image_path = os.path.join(DATA_MOST_NOT_CROP_PATH,
                              image_list)

    image = Image.open(image_path)
    _, proportion = distortion_crop_image(image)

    LOGGER.info(f'test_distortion_croper: proportion={proportion}')

    assert proportion > 0.0 and proportion <= 1.0


def calculate_croped_number(path, threshold=0.9):
    image_list = os.listdir(path)

    total, croped = len(image_list), 0

    for image_name in image_list:
        image_path = os.path.join(path, image_name)

        image = Image.open(image_path)

        try:
            _, proportion = distortion_crop_image(image)
        except Exception as ex:
            print(image_name)
            assert False, str(ex)

        croped += 1 if proportion < threshold else 0

    return croped / total


def test_ratio_non_cropable_images():
    proportion = calculate_croped_number(DATA_MOST_NOT_CROP_PATH,
                                         threshold=0.9)

    LOGGER.info(f'test_ratio_non_cropable_images: proportion={proportion}')

    assert proportion < 0.1


def test_ratio_cropable_images():
    proportion = calculate_croped_number(DATA_MOST_CROP_PATH,
                                         threshold=0.9)

    LOGGER.info(f'test_ratio_cropable_images: proportion={proportion}')

    assert proportion > 0.9


def test_croper_time_rate():
    TIME_RATE = 1.5 * 60  # mean minutes per operation

    initial_time = time()

    _ = calculate_croped_number(DATA_MOST_NOT_CROP_PATH, threshold=1.0)
    _ = calculate_croped_number(DATA_MOST_CROP_PATH, threshold=1.0)

    dt = time() - initial_time
    rate = dt / TIME_RATE

    LOGGER.info(f'test_croper_time_rate: rate={rate}')

    assert rate < TIME_RATE
