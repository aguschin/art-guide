import warnings
warnings.filterwarnings("ignore")
from image_crop_module.croper import crop_image
from reverse_image_search_module.search_image import find_image,find_file_name

import os
from PIL import Image
def process_image(image_path):
    img = Image.open(image_path)
    cropped_image = crop_image(img)
    idx, _, _ = find_image(cropped_image)
    return find_file_name(idx)[0]

folder_path = 'test_crop'
matched_count = 0
supported_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

for file in os.listdir(folder_path):
    if file.lower().endswith(tuple(supported_extensions)):
        full_path = os.path.join(folder_path, file)
        processed_file_name = process_image(full_path)
        base_file_name = file.split('-')[0]
        if processed_file_name == base_file_name:
            matched_count += 1
print(f"Number of matched images: {matched_count}")
