from skimage import color, data, io
import numpy as np


def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    return color.rgb2gray(image)
