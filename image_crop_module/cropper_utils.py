import numpy as np


def side_distance(p1, p2):
    # euclidian
    dd = (p1 - p2) ** 2
    dd = dd.sum()
    return dd


def find_aspect_ratio(corners):
    centroid = np.mean(corners, axis=0)

    # Apply the transformation to move to the center of coordinates
    corners = corners - centroid

    cov_matrix = np.cov(corners, rowvar=False)

    # Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    # Sort eigenvalues and eigenvectors in descending order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # Calculate aspect ratio from eigenvalues
    aspect_ratio = np.sqrt(eigenvalues[1] / eigenvalues[0])

    return aspect_ratio


def find_width_height_aspect_ratio(points_n, aspect_ratio):
    # determine with rec it is
    #   1     2
    # *--* *------*
    # |  | |      |
    # |  | *------*
    # *--*

    distance_w = side_distance(points_n[0], points_n[1])
    distance_h = side_distance(points_n[1], points_n[2])

    print(distance_w, distance_h)

    # wight height aspect ratio

    wh_aa = 1.0 / aspect_ratio if distance_w < distance_h else aspect_ratio

    return wh_aa
