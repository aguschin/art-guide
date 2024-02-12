import os
import pickle
import random
import warnings

import numpy as np
import PIL
import torch
import torchvision
import torchvision.transforms.functional as F
from decouple import config
from PIL import Image
from torchvision import transforms
from tqdm import tqdm
from transformers import AutoImageProcessor, AutoModel

# Disable all warnings
warnings.filterwarnings("ignore")

MULTI_EMBEDDINGS = config("MULTI_EMBEDDINGS") == "True"

SINGLE_VALES_OUTPUT_FILE = config("SINGLE_VALES_OUTPUT_FILE")
SINGLE_KEYS_OUTPUT_FILE = config("SINGLE_KEYS_OUTPUT_FILE")

MULTI_VALES_OUTPUT_FILE = config("MULTI_VALES_OUTPUT_FILE")
MULTI_KEYS_OUTPUT_FILE = config("MULTI_KEYS_OUTPUT_FILE")


torch.manual_seed(17)


class Img2VecResnet18:
    def __init__(self, batch_size=64):
        self.device = torch.device("cpu")
        self.model_name = 'facebook/dinov2-base'
        self.feature_extractor = AutoImageProcessor.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name).to(self.device)
        self.model.eval()
        self.batch_size = batch_size

    # def getFeatureLayer(self):
    #     cnnModel = torchvision.models.resnet18(pretrained=True)
    #     layer = cnnModel._modules.get("avgpool")
    #     self.layer_output_size = 512

    #     return cnnModel, layer

    def preprocess_image(self, image):
        if not isinstance(image, torch.Tensor):
            image = self.feature_extractor(images=image, return_tensors="pt").to(
                self.device
            )
        return image

    def getVectors(self, images):
        with torch.no_grad():
            inputs = self.preprocess_image(images)
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :]
        return embeddings.cpu().numpy()


img2vec = Img2VecResnet18(batch_size=1)


def extract_and_save_embeddings(input_folder, output_file):
    image_files = tqdm(
        [
            f
            for f in os.listdir(input_folder)
            if f.endswith((".jpg", ".jpeg", ".png", ".bmp"))
        ]
    )

    counter = 0
    failed = 0
    embeddings_dict = {}

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)

        try:
            image = Image.open(image_path)

            vector = img2vec.getVectors(image)
            embeddings_dict[
                image_file
            ] = vector.tolist()  # Convert to list for serialization
            counter += 1
        except Exception as e:
            print(f"Skipping image: {image_file} - Error: {str(e)}")
            failed += 1

    with open(output_file, "wb") as output_f:
        pickle.dump(embeddings_dict, output_f)

    print(f"Successful images: {counter}")
    print(f"Failed images: {failed}")


def make_points(point1, point2, width, height):
    return point1[0] * width, point1[1] * height, point2[0] * width, point2[1] * height


def gen_multi_cropping(width, height, k=6, min_size_random=128):
    """
    6 default croppings are made by hand, the rest are random
    """

    DEFAULT_CROPP = [
        [(0, 0), (1, 1)],
        [(0.25, 0.25), (0.75, 0.75)],
        [(0, 0), (0.5, 0.5)],
        [(0.5, 0), (1, 0.5)],
        [(0, 0.5), (0.5, 1)],
        [(0.5, 0.5), (1, 1)],
    ]

    for i in range(k):
        if i < 6:
            default_points = DEFAULT_CROPP[i]
            x, y, xend, yend = make_points(
                default_points[0], default_points[1], width, height
            )
        else:
            x = random.randint(0, width - min_size_random)
            y = random.randint(0, height - min_size_random)

            xend = random.randint(x + min_size_random, width)
            yend = random.randint(y + min_size_random, height)

        yield x, y, xend, yend


def extract_and_save_embeddings_multiple(input_folder, output_file, k=6):
    image_files = tqdm(
        [
            f
            for f in os.listdir(input_folder)
            if f.endswith((".jpg", ".jpeg", ".png", ".bmp"))
        ]
    )

    counter = 0
    failed = 0
    embeddings_dict = {}

    for image_file in image_files:
        image_path = os.path.join(input_folder, image_file)

        try:
            image = Image.open(image_path)

            vectors = []

            for x, y, x_end, y_end in gen_multi_cropping(
                image.width, image.height, k=k, min_size_random=128
            ):
                croped = image.crop((x, y, x_end, y_end))
                feature_vector = img2vec.getVectors(croped)

                vectors.append(feature_vector)

            embeddings_dict[image_file] = vectors

            counter += 1
        except Exception as e:
            print(f"Skipping image: {image_file} - Error: {str(e)}")
            failed += 1

    with open(output_file, "wb") as output_f:
        pickle.dump(embeddings_dict, output_f)

    print(f"Successful images: {counter}")
    print(f"Failed images: {failed}")


if __name__ == "__main__":
    IMAGE_FOLDER = "data"

    if not os.path.isdir(IMAGE_FOLDER):
        os.mkdir(IMAGE_FOLDER)

    input_folder = "data/img/full"

    if MULTI_EMBEDDINGS:
        print("Making embeddings MULTI")

        output_file = f"{IMAGE_FOLDER}/embeddings_full_multi.pkl"
        extract_and_save_embeddings_multiple(input_folder, output_file)
    else:
        print("Making embeddings SINGLE")

        output_file = f"{IMAGE_FOLDER}/embeddings_full.pkl"
        extract_and_save_embeddings(input_folder, output_file)
