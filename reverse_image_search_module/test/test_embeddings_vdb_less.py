import os
from PIL import Image
from ..search_image import find_index_from_image, find_file_name, load_vector_db
import logging


DATA_IMAGES_PATH = 'data/img/full/'
IMAGE_MAX_NUMBER = 5000


logging.basicConfig(level=logging.INFO)
mylogger = logging.getLogger()

load_vector_db(False, reload=True, vdb=False)

def get_image_idx_name_matching(images_names):
    positive = 0

    for _im in images_names:
        try:
            image = Image.open(os.path.join(DATA_IMAGES_PATH, _im))
            # to check the size and truncation
            _ = image.resize((255, 255))
        except Exception as ex:
            mylogger.info(f'image {_im} load error')
            mylogger.info(str(ex))
            continue

        idx, _ = find_index_from_image(image, n=1)
        idx = idx[0]

        print(_im, idx)

        # import ipdb
        # ipdb.set_trace()
        file_name = find_file_name(idx)

        # print(file_name)

        if file_name == _im:
            positive += 1
        else:
            mylogger.info(f"UNMATCHED <original>{_im} <matched>{file_name}")

    return positive

def test_static_accuracy():
    images_names = os.listdir(DATA_IMAGES_PATH)
    images_names = images_names[:3]

    positive = get_image_idx_name_matching(images_names)

    acc = positive / 3

    mylogger.info(f"test_static_acc: ACCURACY = {acc}")

    assert acc == 1.0