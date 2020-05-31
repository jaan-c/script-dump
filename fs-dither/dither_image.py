from typing import *
from skimage.color import rgb2gray
import numpy as np


def dither_image(
    image: np.ndarray, *, grayscale=True, shade_count=4
) -> np.ndarray:
    """ Dither image with Floyd-Steinberg algorithm. """

    image = rgb2gray(image) if grayscale else image

    if len(image.shape) == 2:
        return _dither_channel(image, shade_count)

    elif len(image.shape) == 3 and image.shape[2] in (3, 4):
        dithered_color_channels: List[np.ndarray] = []
        for color_channel_ix in range(3):
            color_channel = image[:, :, color_channel_ix]
            dithered = _dither_channel(color_channel, shade_count)

            dithered_color_channels.append(dithered)

        channels = [*dithered_color_channels]
        if image.shape[2] == 4:  # If has alpha channel.
            channels.append(image[:, :, 3])

        return np.dstack(channels)

    else:
        raise ValueError(f"Invalid image shape {image.shape}.")


def _dither_channel(channel: np.ndarray, shade_count: int) -> np.ndarray:
    """ Dither a single channel (2 dimensional array) of image using 
        Floyd-Steinberg algorithm. """

    if len(channel.shape) != 2:
        raise ValueError(f"channel must exactly have 2 dimensions.")
    elif shade_count < 2:
        raise ValueError("shade_count must be minimum of 2.")

    copy = channel.copy()
    height, width = copy.shape
    gap_count = shade_count - 1
    offsets_and_weights = [  # (x_offset, y_offset, distribution_weight)
        (1, 0, 7 / 16),
        (-1, 1, 3 / 16),
        (0, 1, 5 / 16),
        (1, 1, 1 / 16),
    ]

    for y in range(height):
        for x in range(width):
            old_pixel = copy[y, x]
            new_pixel = round(old_pixel * gap_count) / gap_count
            copy[y, x] = new_pixel

            quantization_error = old_pixel - new_pixel

            for ox, oy, w in offsets_and_weights:
                nx, ny = x + ox, y + oy
                try:
                    copy[ny, nx] += quantization_error * w
                except IndexError:
                    pass

    return copy
