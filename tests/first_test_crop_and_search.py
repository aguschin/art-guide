import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(abspath(__file__))))
import warnings

warnings.filterwarnings("ignore")
from image_crop_module.croper import crop_image
from reverse_image_search_module.search_image import find_image, load_vector_db
import os
import statistics

from PIL import Image


def process_image(image_path, n=1):
    img = Image.open(image_path)
    cropped_image = crop_image(img)
    idx, _, _ = find_image(cropped_image, n)
    return idx

 
import os
import statistics

def run_the_test(multi):
    load_vector_db(multi=multi, reload=True)
    folder_path= 'tests/test_crop'
    supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    reference_images_idx = {}

    # Process reference images
    for file in os.listdir(folder_path):
        if file.lower().endswith(tuple(supported_extensions)) and "-" not in file:
            full_path = os.path.join(folder_path, file)
            base_file_name = file.split(".")[0]
            reference_images_idx[base_file_name] = process_image(full_path, n=1)

    positions = []

    # Process and compare images with reference
    for file in os.listdir(folder_path):
        if file.lower().endswith(tuple(supported_extensions)) and "-" in file:
            base_file_name, _ = file.split("-")[0], file.split("-")[1]
            if base_file_name in reference_images_idx:
                full_path = os.path.join(folder_path, file)
                processed_idx_list = process_image(full_path, n=10000)
                for i, idx in enumerate(processed_idx_list):
                    if idx in reference_images_idx[base_file_name]:
                        positions.append(i)
                        break

    # Calculate and print statistics
    median_position = statistics.median(positions)
    mean_position = statistics.mean(positions)
    zero_position_percentage = sum([el == 0 for el in positions]) / len(positions)
    return median_position, mean_position, zero_position_percentage

def test_images_after_crop_single_embedding():
    median_position, mean_position, zero_position_percentage = run_the_test(multi=False)
    print("Median Position:", median_position)
    print("Mean Position:", mean_position)
    print("Percentage of Positions at 0:", zero_position_percentage)
    assert zero_position_percentage > 0.17, "Ratio of correct findings should be higher"


def test_images_after_crop_multi_embedding():
    median_position, mean_position, zero_position_percentage = run_the_test(multi=True)
    print("Median Position:", median_position)
    print("Mean Position:", mean_position)
    print("Percentage of Positions at 0:", zero_position_percentage)
    assert zero_position_percentage > 0.21, "Ratio of correct findings should be higher"
