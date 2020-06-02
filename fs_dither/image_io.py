from typing import *
from skimage import io, img_as_ubyte, img_as_float64
import numpy as np


def read_image(path: str) -> np.ndarray:
    """ Read image at path and returns a 2D array for grayscale and 3D array for
        RGB and RGBA images.
    """
    image = io.imread(path)
    if image.dtype == np.uint8:
        image = img_as_float64(image)

    return image


def save_image(path: str, image: np.ndarray) -> None:
    """ Save image to path. 

        The file extension of path will determine the encoding to be used, ie.
        .jpg, .png etc.
    """
    if image.dtype == np.float64:
        image = img_as_ubyte(image)

    io.imsave(path, image)

