from typing import *
from skimage import io
import numpy as np


def read_image(path: str) -> np.ndarray:
    """ Read image at path. """
    image = io.imread(path)
    if not _values_in_range(image, 0, 1):
        return image / 255


def save_image(path: str, image: np.ndarray) -> None:
    """ Save image to path. """
    if not _values_in_range(image, 0, 255):
        image = (image * 255).astype(int)

    io.imsave(path, image)


def _values_in_range(
    ndarray: np.ndarray, minimum: int, maximum: int
) -> bool:
    return ndarray.min() <= minimum and ndarray.max() <= maximum
