from transformers import SegformerImageProcessor
from transformers import SegformerForSemanticSegmentation
import torch
import cv2
import numpy as np


MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"


processor = SegformerImageProcessor.from_pretrained(MODEL_NAME)
model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)

painting_id = 22


def side_distance(p1, p2):
    # euclidian
    dd = (p1 - p2) ** 2
    dd = dd.sum()
    return dd


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
    point = max(point_list,
                key=lambda x: x[0]*ref_point[0] + x[1]*ref_point[1])
    return point


def make_four_points(poligon):
    points = poligon.reshape(-1, 2)

    points_distance = []
    for i in range(points.shape[0]):
        iplus = (i+1) % points.shape[0]

        p1, p2 = points[i], points[iplus]
        distance = side_distance(p1, p2)

        points_distance.append((i, p1, p2, distance))

    points_distance = sorted(points_distance, key=lambda x: x[3])

    points_distance = points_distance[-4:]

    points_distance = sorted(points_distance, key=lambda x: x[0])

    interseption_of_four_sides = []

    for i in range(4):
        pos_1 = i
        pos_2 = (i+1) % 4

        l1 = (points_distance[pos_1][1], points_distance[pos_1][2])
        l2 = (points_distance[pos_2][1], points_distance[pos_2][2])

        interseption = point_interseption(l1, l2)

        interseption_of_four_sides.append(interseption)

    corner_oriented_interseption = [
        select_corner(interseption_of_four_sides, (-1, -1)),  # 0, 0
        select_corner(interseption_of_four_sides, (1, -1)),  # W, 0
        select_corner(interseption_of_four_sides, (1, 1)),  # W, H
        select_corner(interseption_of_four_sides, (-1, 1)),  # 0, H
    ]

    return corner_oriented_interseption


def filter_four_points(point_list, W, H):
    new_l = [(min(max(x, 0), W), min(max(y, 0), H))
             for x, y in point_list]
    new_l = [(int(x), int(y)) for x, y in new_l]

    return new_l


#  ------------------------------------------------------------------


def find_best_contour(contours, W, H):

    distances_and_areas = []
    area_threshold = 0

    for i, contour in enumerate(contours):
        M = cv2.moments(contour)

        area = M["m00"]

        if area != 0:
            Cx = int(M["m10"] / area)
            Cy = int(M["m01"] / area)
        else:
            Cx, Cy = 0, 0

        D = (W/2 - Cx) ** 2 + (H/2 - Cy) ** 2

        distances_and_areas.append((i, area, D))
        area_threshold = max(area_threshold, area)

    area_threshold = area_threshold * 0.75

    selected = min(distances_and_areas,
                   key=lambda x: x[2] if area >= area_threshold else 1e9)

    return contours[selected[0]]


# poligon area
def poligon_area_from_points(vertices):
    vertices = np.vstack((vertices, vertices[0]))
    # Calculate the area using the Shoelace formula
    o = vertices[:-1, 0] * vertices[1:, 1] - vertices[1:, 0] * vertices[:-1, 1]
    area = 0.5 * np.abs(np.sum(o))

    return area


@torch.no_grad()
def distortion_crop_image(image):
    '''
        image: pilow image
        return: croped image, proportion of croping
    '''

    # original size
    OW = image.width
    OH = image.height

    # generate the mask-segmentation
    inputs = processor(images=image, return_tensors="pt")
    logits = model(**inputs).logits

    # select only paintings
    mask = logits.squeeze().argmax(0)
    mask = (mask == painting_id).numpy().astype(np.uint8)

    # middle size
    IW = mask.shape[0]
    IH = mask.shape[1]

    # find contours
    contours, _ = cv2.findContours(mask,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) < 1:
        return np.array(image, dtype=np.float32) / 255.0, 1

    contour = find_best_contour(contours, IW, IH)

    del contours

    # approximate a poligon
    epsilon = 0.02 * cv2.arcLength(contour, True)
    poligon = cv2.approxPolyDP(contour, epsilon, True)

    # fit a 4-side poligon, and return 4 corners points
    points = make_four_points(poligon)

    # try to remove this in the final
    # todo: add support for padding with negative interseption
    # todo: add support for non-conves poligons (use convex hull)
    points = filter_four_points(points, IW, IH)
    points = np.array(points)

    # make wraping matrix
    src_points = points * np.array([[OW/IW, OH/IH]])
    src_points = src_points.astype(np.float32)

    # final shape
    corner1 = (0, 0)
    corner2 = (OW, 0)
    corner3 = (OW, OH)
    corner4 = (0, OH)

    dst_points = np.array([corner1, corner2, corner3, corner4],
                          dtype=np.float32)

    area_proportion = poligon_area_from_points(dst_points)
    area_proportion = poligon_area_from_points(src_points)

    # Compute the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    image_np = np.array(image, dtype=np.float32) / 255.0
    # Apply the perspective warp to the image
    warped_image = cv2.warpPerspective(image_np, matrix, (OW, OH))

    return warped_image, area_proportion
