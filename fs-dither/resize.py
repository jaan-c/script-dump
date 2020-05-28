from skimage import transform
import numpy as np


def shrink(image: np.ndarray, max_axis: int) -> np.ndarray:
    """ Shrink image so that its width and height is under max_axis. If it 
        already is, no processing is performed.
    """
    height, width = image.shape

    if height <= max_axis and width <= max_axis:
        return image.copy()

    if width >= height:
        downscale_factor = max_axis / width
    else:
        downscale_factor = max_axis / height

    return transform.rescale(image, downscale_factor, anti_aliasing=True)
