from typing import *
import numpy as np


def dither_image(image: np.ndarray, *, shade_count=4) -> np.ndarray:
    """ Dither all channels using dither_func. """

    if shade_count < 1:
        raise ValueError(f"shade_count must be >= 2, got {shade_count}.")

    if _is_2d(image):
        return _dither_channel(image, shade_count=shade_count)
    elif _has_channel_count(image, 3):
        return _dither_rgb(image, shade_count=shade_count)
    elif _has_channel_count(image, 4):
        return _dither_rgba(image, shade_count=shade_count)
    else:
        raise ValueError(f"Unhandled image shape {image.shape}.")


def _dither_rgba(image: np.ndarray, shade_count: int) -> np.ndarray:
    if not _has_channel_count(image, 4):
        raise ValueError("image must have exactly 4 channels.")

    dithered_rgb = _dither_rgb(image[:, :, :3])
    return np.vstack((dithered_rgb, image[:, :, 3]))


def _dither_rgb(image: np.ndarray, shade_count: int) -> np.ndarray:
    """ Dither an image with RGB channels. """

    if not _has_channel_count(image, 3):
        raise ValueError("image must have exactly 3 color channels.")

    dithered_channels: List[np.ndarray] = []
    for channel_ix in range(3):
        channel = image[:, :, channel_ix]
        dithered = _dither_channel(channel, shade_count)

        dithered_channels.append(dithered)

    return np.array(dithered_channels)


def _dither_channel(channel: np.ndarray, shade_count: int) -> np.ndarray:
    """ Dither a single channel of image using Floyd-Steinberg algorithm. """

    if not _is_2d(channel):
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


def _is_2d(ndarray: np.ndarray) -> bool:
    return len(ndarray.shape) == 2


def _is_3d(ndarray: np.ndarray) -> bool:
    return len(ndarray.shape) == 3


def _has_channel_count(image: np.ndarray, expected_count: int) -> bool:
    if not _is_3d(image):
        raise ValueError("image must have exactly 3 dimensions.")
    else:
        return image.shape[2] == expected_count


def _are_values_in_range(
    ndarray: np.ndarray, minimum: float, maximum: float
) -> bool:
    """ Check if values in ndarray are in inclusive [minimum, maximum] range. """

    smallest = ndarray.min()
    biggest = ndarray.max()

    return minimum <= smallest <= maximum and minimum <= biggest <= maximum
