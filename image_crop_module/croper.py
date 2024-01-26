from .distortion_croper import distortion_crop_image


def crop_image(image):
    """
    image: pilow image
    """
    croped, _ = distortion_crop_image(image)

    return croped
