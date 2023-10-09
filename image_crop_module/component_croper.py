from transformers import SegformerImageProcessor
from transformers import SegformerForSemanticSegmentation
import torch
import cv2
import numpy as np


MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"


processor = SegformerImageProcessor.from_pretrained(MODEL_NAME)
model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)

painting_id = 22
pot_id = 125
sculpture_id = 132


def min_max(image):
    minv = image.min()
    maxv = image.max()

    return (image - minv) / (maxv - minv)


def distance(a, b):
    return ((a - np.array(b)) ** 2).sum()


@torch.no_grad()
def component_crop_image(image):
    '''image: pilow image '''

    W = image.width
    H = image.height

    inputs = processor(images=image, return_tensors="pt")
    logits = model(**inputs).logits

    mask = logits.squeeze().argmax(0)
    mask = (mask == painting_id) + (mask == pot_id) + (mask == sculpture_id)
    mask = (mask == 1).numpy()

    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask.astype(float), kernel, cv2.BORDER_REFLECT)

    mask = cv2.resize(mask, (W, H))

    image_np = min_max(np.array(image))

    mask = mask.astype(np.uint8)
    _, _, stats, centroids = cv2.connectedComponentsWithStats(mask)

    stats[0, 4] = 0.0

    # remove the smallest clusters
    h = stats[:, 4] >= stats[:, 4].max() * 0.75

    stats = stats[h, :]
    centroids = centroids[h, :]

    # if len(centroids) == 0:
    #    return image

    image_center = np.array([image.width / 2, image.height / 2])

    best_c = min(enumerate(centroids),
                 key=lambda x: distance(image_center, x[1]))[0]

    x, y, width, height, _ = stats[best_c]
    croped = image_np[y:y+height, x:x+width]

    return croped.astype(np.float32)
