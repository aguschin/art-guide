import os

import torchvision.transforms as transforms
from PIL import Image

from .search_image import find_image


def make_syntetic_first_second_distances(folder_path, n=1000):
    augmentation_transforms = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.RandomRotation(5),
            # transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(
                brightness=0.2, contrast=0.2, saturation=0.2, hue=0.05
            ),
            transforms.RandomResizedCrop(224, scale=(0.9, 1.0)),
            transforms.ToTensor(),
        ]
    )

    image_files = os.listdir(folder_path)[:n]
    file_distances_aug = {}
    file_distances_aug_second = {}

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)

        image = Image.open(image_path)

        augmented_image = augmentation_transforms(image)

        # feature_vector = img2vec.getVectors(augmented_image)
        idx, dist, data = find_image(augmented_image, n=2)

        file_distances_aug[image_file] = dist[0]
        file_distances_aug_second[image_file] = dist[1]

    y_test, y_score = [], []
    for k, v in file_distances_aug.items():
        y_test.append(1)
        y_score.append(v)

    for k, v in file_distances_aug_second.items():
        y_test.append(0)
        y_score.append(v)

    return y_test, y_score
