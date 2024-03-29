import math

import cv2
import numpy as np
import torch
from segment_anything import SamPredictor, sam_model_registry
from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor

SAM_MODELS = {
    "vit_h": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth",
    "vit_l": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth",
    "vit_b": "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth",
}

from .cropper_utils import (
    find_aspect_ratio,
    find_width_height_aspect_ratio,
    side_distance,
)

MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"


processor = SegformerImageProcessor.from_pretrained(MODEL_NAME)
model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)

painting_id = 22


def load_sam():
    global sam

    sam_type = "vit_h"
    checkpoint_url = SAM_MODELS[sam_type]

    sam_ck = sam_model_registry[sam_type]()
    state_dict = torch.hub.load_state_dict_from_url(checkpoint_url)
    sam_ck.load_state_dict(state_dict, strict=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # we need a big GPU here
    # sam_ck.to(device=device)
    sam = SamPredictor(sam_ck)


sam = None
load_sam()


def point_interseption(l1, l2):
    x1, y1 = l1[0][0], l1[0][1]
    x2, y2 = l1[1][0], l1[1][1]
    x3, y3 = l2[0][0], l2[0][1]
    x4, y4 = l2[1][0], l2[1][1]

    # Calculate the coefficients of the line equations (Ax + By = C)
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1

    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3

    # Calculate the determinant
    det = A1 * B2 - A2 * B1

    # Check if the lines are parallel (det == 0)
    if det == 0:
        return (-1, -1)
    else:
        # Calculate the intersection point
        x_intersection = (B2 * C1 - B1 * C2) / det
        y_intersection = (A1 * C2 - A2 * C1) / det
        intersection_point = (x_intersection, y_intersection)

        return intersection_point


def select_corner(point_list, ref_point):
    point = max(point_list, key=lambda x: x[0] * ref_point[0] + x[1] * ref_point[1])
    return point


def make_corners(point_list):
    x1, y1 = point_list[0]
    x2, y2 = point_list[1]
    x3, y3 = point_list[2]

    cross_product = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)

    if cross_product < 0:
        point_list = point_list[::-1]

    # firs corner point
    first_corner = max(enumerate(point_list), key=lambda x: -x[1][0] - x[1][1])[0]

    # shift the points
    point_list = point_list[first_corner:] + point_list[:first_corner]

    return point_list


# poligon area
def poligon_area_from_points(vertices):
    vertices = np.vstack((vertices, vertices[0]))
    # Calculate the area using the Shoelace formula
    o = vertices[:-1, 0] * vertices[1:, 1] - vertices[1:, 0] * vertices[:-1, 1]
    area = 0.5 * np.abs(np.sum(o))

    return area


def calc_bbox_from_points(points):
    mi_x, mi_y = points[:, 0].min(), points[:, 1].min()
    ma_x, ma_y = points[:, 0].max(), points[:, 1].max()

    return [(mi_x, mi_y), (ma_x, mi_y), (ma_x, ma_y), (mi_x, ma_y)]


def make_four_points(poligon):
    points = poligon.reshape(-1, 2)

    assert poligon.shape[0] > 2

    if poligon.shape[0] == 3:
        # calc a bounding box
        bbox = calc_bbox_from_points(points)
        corner_oriented_bbox = make_corners(bbox)

        return corner_oriented_bbox

    points_distance = []
    for i in range(points.shape[0]):
        iplus = (i + 1) % points.shape[0]

        p1, p2 = points[i], points[iplus]
        distance = side_distance(p1, p2)

        points_distance.append((i, p1, p2, distance))

    points_distance = sorted(points_distance, key=lambda x: x[3])

    points_distance = points_distance[-4:]

    points_distance = sorted(points_distance, key=lambda x: x[0])

    interseption_of_four_sides = []

    for i in range(4):
        pos_1 = i
        pos_2 = (i + 1) % 4

        l1 = (points_distance[pos_1][1], points_distance[pos_1][2])
        l2 = (points_distance[pos_2][1], points_distance[pos_2][2])

        interseption = point_interseption(l1, l2)

        interseption_of_four_sides.append(interseption)

    corner_oriented_interseption = make_corners(interseption_of_four_sides)

    return corner_oriented_interseption


def adjust_points_and_padd(point_list, IW, IH):
    # calculate padding for negative points value
    top_pad = 0
    bottom_pad = 0
    left_pad = 0
    right_pad = 0

    for point in point_list:
        bottom_pad = max(bottom_pad, max(0, point[1] - IH))
        top_pad = max(top_pad, max(0, -1 * point[1]))

        right_pad = max(right_pad, max(0, point[0] - IW))
        left_pad = max(left_pad, max(0, -1 * point[0]))

    top_pad = math.ceil(top_pad)
    bottom_pad = math.ceil(bottom_pad)
    left_pad = math.ceil(left_pad)
    right_pad = math.ceil(right_pad)

    points = [(x + left_pad, y + top_pad) for x, y in point_list]
    points = np.array(points)

    return points, top_pad, bottom_pad, left_pad, right_pad


#  ------------------------------------------------------------------


@torch.no_grad()
def generate_mask(image, minimun_area=100, dp_box=3):
    """
    image: pilow image
    return: croped image, proportion of croping
    """

    # original size
    OW = image.width
    OH = image.height
    image_area = OW * OH

    # generate the mask-segmentation
    inputs = processor(images=image, return_tensors="pt")
    logits = model(**inputs).logits

    # select only paintings
    mask = logits.squeeze().argmax(0)
    mask = (mask == painting_id).numpy().astype(np.uint8)

    # middle size
    IW = mask.shape[0]
    IH = mask.shape[1]

    # find bboxes
    mask = cv2.dilate(mask.astype(np.uint8), None, iterations=1)
    num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(
        mask, connectivity=8
    )

    boxes = []
    area_threshold = 0

    image_array = np.asarray(image)

    for i in range(1, num_labels):  # Start from 1 to ignore background component
        x, y, w, h, area = stats[i]

        # distance to the center
        D = (IW / 2 - centroids[i][0]) ** 2 + (IH / 2 - centroids[i][1]) ** 2

        if area > minimun_area:
            boxes.append((x, y, x + w, y + h, D, area))
            area_threshold = max(area_threshold, area)

    if len(boxes) == 0:
        return image_array, np.zeros(image_array.shape, dtype=np.uint8), False

    area_threshold *= 0.8

    selected = min(boxes, key=lambda x: x[4] if x[5] >= area_threshold else 1e9)

    x, y, w, h, _, _ = selected
    # convert boxes cordinates to the original image shape
    x, y, w, h = (x / IW) * OW, (y / IH) * OH, (w / IW) * OW, (h / IH) * OH
    # expand the boxes
    x, y, w, h = (
        max(0, x - dp_box),
        max(0, y - dp_box),
        min(OW - 1, w + dp_box),
        min(OH - 1, h + dp_box),
    )

    boxes = [(x, y, w, h)]

    sam.set_image(image_array)

    # using sam up to 2sc
    boxes_np = torch.Tensor(boxes)
    transformed_boxes = sam.transform.apply_boxes_torch(boxes_np, image_array.shape[:2])
    mask, _, _ = sam.predict_torch(
        point_coords=None,
        point_labels=None,
        boxes=transformed_boxes.to(sam.device),
        multimask_output=False,
    )

    mask = mask.squeeze().cpu().numpy().astype(np.uint8)

    return image_array, mask, True


def find_best_contour(contours, W, H):
    distances_and_areas = []
    area_threshold = 0

    for i, contour in enumerate(contours):
        M = cv2.moments(contour)

        area = M["m00"] if len(contour) > 3 else 0

        if area != 0:
            Cx = int(M["m10"] / area)
            Cy = int(M["m01"] / area)
        else:
            Cx, Cy = 0, 0

        D = (W / 2 - Cx) ** 2 + (H / 2 - Cy) ** 2

        distances_and_areas.append((i, area, D))
        area_threshold = max(area_threshold, area)

    area_threshold = area_threshold * 0.8

    selected = min(
        distances_and_areas, key=lambda x: x[2] if x[1] >= area_threshold else 1e9
    )

    return contours[selected[0]], selected[1]


def distortion_crop_image(image):
    """
    image: pilow image
    return: croped image, proportion of croping
    """

    # import ipdb

    # ipdb.set_trace()

    image, mask, flag = generate_mask(image, 800, 3)

    if not flag:
        return image, 1

    # find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # no painting found
    if len(contours) < 1:
        return image, 1

    contour, raw_contour_area = find_best_contour(
        contours, mask.shape[0], mask.shape[1]
    )

    # the area of the segemented area is too small
    if raw_contour_area < 800:
        return image, 1

    del contours

    contour = cv2.convexHull(contour)

    # approximate a poligon
    epsilon = 0.02 * cv2.arcLength(contour, True)
    poligon = cv2.approxPolyDP(contour, epsilon, True)

    # fit a 4-side poligon, and return 4 corners points
    points = make_four_points(poligon)

    # todo: add support for padding with negative interseption
    points, top_pad, bottom_pad, left_pad, right_pad = adjust_points_and_padd(
        points, image.shape[0], image.shape[1]
    )

    # image_np = np.array(image, dtype=np.float32) / 255.0
    image_np = cv2.copyMakeBorder(
        image,
        top_pad,
        bottom_pad,
        left_pad,
        right_pad,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )

    src_points = points.astype(np.float32)

    # final shape
    corner1 = (0, 0)
    corner2 = (image_np.shape[0], 0)
    corner3 = (image_np.shape[0], image_np.shape[1])
    corner4 = (0, image_np.shape[1])

    dst_points = np.array([corner1, corner2, corner3, corner4], dtype=np.float32)

    image_area = image.shape[0] * image.shape[1]
    area_proportion = poligon_area_from_points(src_points)
    area_proportion /= image_area

    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective warp to the image
    warped_image = cv2.warpPerspective(
        image_np, matrix, (image_np.shape[0], image_np.shape[1])
    )

    # Adjust aspect ratio of wraping
    aspect_ratio = find_aspect_ratio(src_points)
    wh_aa = find_width_height_aspect_ratio(src_points, aspect_ratio)

    aa_width = min(image_np.shape[0], image_np.shape[1])
    aa_height = aa_width * wh_aa

    resized_aa_image = cv2.resize(warped_image, (int(aa_width), int(aa_height)))

    return resized_aa_image, area_proportion
