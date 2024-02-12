import sys
import time
from os.path import abspath, dirname

import numpy as np

sys.path.append(dirname(dirname(abspath(__file__))))
import warnings

warnings.filterwarnings("ignore")
import os
import statistics

from PIL import Image

from image_crop_module.croper import crop_image
from reverse_image_search_module.search_image import find_image, load_vector_db


def process_image(image_path, n=1, crop=True):
    print("Start process image")
    img = Image.open(image_path)
    if crop:
        img = crop_image(img)
        print(f"Cropped image {image_path}")
    idx, _, _ = find_image(img, n)
    return idx


def run_the_test(multi):
    try:
        load_vector_db(multi=multi, reload=True)
        folder_path = "tests/test_crop"
        supported_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]

        reference_images_idx = {}
        counter = 0

        # Process reference images
        for file in os.listdir(folder_path):
            if file.lower().endswith(tuple(supported_extensions)) and "-" not in file:
                full_path = os.path.join(folder_path, file)
                base_file_name = file.split(".")[0]
                reference_images_idx[base_file_name] = process_image(
                    full_path, n=1, crop=False
                )

        positions = []

        # Process and compare images with reference
        for file in os.listdir(folder_path):
            print(f"Checking file for comparison: {file}")

            if file.lower().endswith(tuple(supported_extensions)) and "-" in file:
                # if counter>=10:
                #     print("Limit")
                #     break
                base_file_name, _ = file.split("-")[0], file.split("-")[1]
                if base_file_name in reference_images_idx:
                    full_path = os.path.join(folder_path, file)
                    processed_idx_list = process_image(full_path, n=-1)
                    print("found idx")
                    for i, idx in enumerate(processed_idx_list):
                        if idx in reference_images_idx[base_file_name]:
                            positions.append(i)
                            break
                counter += 1
                print(f"Processed comparison image: {file} (Counter: {counter})")

        # Calculate and print statistics
        print("Finish run test")
        positions = np.array(positions)
        print("Median Position:", statistics.median(positions))
        print("Mean Position:", positions.mean())
        accuracy = (positions < 1).mean()
        print("Top-1 accuracy: {}".format(accuracy))
        print("Top-10 accuracy: {}".format((positions < 10).mean()))
        print("Top-100 accuracy: {}".format((positions < 100).mean()))
        print("Top-1000 accuracy: {}".format((positions < 1000).mean()))
        print("Top-10000 accuracy: {}".format((positions < 10000).mean()))
        print(f"{len(positions)} positions: {positions}")
        return accuracy
    except Exception as e:
        print(f"Error :{e}")


def test_images_after_crop_single_embedding():
    start_time = time.time()
    accuracy = run_the_test(multi=False)
    print("Time for single embedding:", (time.time() - start_time) / 60, "minutes")
    # assert accuracy > 0.17, "Ratio of correct findings should be higher"


# def test_images_after_crop_multi_embedding():
#     start_time = time.time()
#     accuracy = run_the_test(multi=True)
#     print("Time for multi embeddings: ", (time.time() - start_time) / 60, " minutes")
#     assert accuracy > 0.14, "Ratio of correct findings should be higher"
