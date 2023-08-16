from transformers import SegformerImageProcessor
from transformers import SegformerForSemanticSegmentation
import torch
import cv2
import numpy as np


# Find the painitng id
# ls = model.config.id2label.values()
# print(ls)

# search = ['painting']

# for i, v in enumerate(ls):
#  if v in search:
#    print (i, v)


MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"


processor = SegformerImageProcessor.from_pretrained(MODEL_NAME)
model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)

painting_id = 22


def min_max(image):
    minv = image.min()
    maxv = image.max()

    return (image - minv) / (maxv - minv)


def distance(a, b):
    return ((a - np.array(b)) ** 2).sum()


@torch.no_grad()
def crop_image(image):
    '''image: pilow image '''

    W = image.width
    H = image.height

    inputs = processor(images=image, return_tensors="pt")
    logits = model(**inputs).logits

#    mask = logits.detach().squeeze().argmax(0)
    mask = logits.squeeze().argmax(0)
    mask = (mask == painting_id).numpy()

    mask = cv2.resize(mask.astype(float), (W, H))

    image_np = min_max(np.array(image))
    image_np = image_np * mask.reshape(mask.shape[0], mask.shape[1], 1)

    mask = mask.astype(np.uint8)
    _, _, stats, centroids = cv2.connectedComponentsWithStats(mask)

    stats[0, 4] = 0.0

    # remove the smallest clusters
    h = stats[:, 4] > stats[:, 4].max() * 0.75

    stats = stats[h, :]
    centroids = centroids[h, :]

    image_center = np.array([image.width / 2, image.height / 2])

    best_c = min(enumerate(centroids),
                 key=lambda x: distance(image_center, x[1]))[0]

    x, y, width, height, _ = stats[best_c]
    croped = image_np[y:y+height, x:x+width]

    return croped
