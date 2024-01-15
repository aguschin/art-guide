import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
import warnings
warnings.filterwarnings("ignore")
from image_crop_module.croper import crop_image
from reverse_image_search_module.search_image import find_image, find_file_name
import os
from PIL import Image
import statistics

def process_image(image_path, n=1):
    img = Image.open(image_path)
    cropped_image = crop_image(img)
    idx, _, _ = find_image(cropped_image, n)
    return idx

folder_path = 'tests/test_crop'
matched_count = 0
supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

reference_images_idx = {}

for file in os.listdir(folder_path):
    if file.lower().endswith(tuple(supported_extensions)) and '-' not in file:
        full_path = os.path.join(folder_path, file)
        base_file_name = file.split('.')[0]
        reference_images_idx[base_file_name] = process_image(full_path, n=1)
positions = []
for file in os.listdir(folder_path):
    if file.lower().endswith(tuple(supported_extensions)) and '-' in file:
        base_file_name, _ = file.split('-')[0], file.split('-')[1]
        if base_file_name in reference_images_idx:
            full_path = os.path.join(folder_path, file)
            processed_idx_list = process_image(full_path, n=10000)
            for i, idx in enumerate(processed_idx_list):
                if idx in reference_images_idx[base_file_name]:
                    # matched_count += 1
                    # print(f"Match found for {file}: Reference index position {i}")
                    positions.append(i)
                    break
print(statistics.median(positions))
print(statistics.mean(positions))
print(positions)
print(sum([el == 0 for el in positions])/len(positions))
