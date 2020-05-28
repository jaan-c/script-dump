from typing import *
import numpy as np
from skimage import data, io, color, img_as_float64


def dither_layer(layer: np.ndarray, level_count: int = 4) -> np.ndarray:
    assert len(layer.shape) == 2

    copy = img_as_float64(layer)
    height, width = copy.shape
    distribution_weights = [7, 3, 5, 1] / np.int64(16)
    neighbor_offsets = [(1, 0), (-1, 1), (0, 1), (1, 1)]

    for y in range(height):
        for x in range(width):
            old_pixel = copy[y, x]
            new_pixel = round_to_nearest_level(old_pixel, level_count)
            copy[y, x] = new_pixel

            quantization_error = old_pixel - new_pixel

            for offset, weight in zip(neighbor_offsets, distribution_weights):
                ox, oy = x + offset[0], y + offset[1]
                try:
                    copy[oy, ox] = np.clip(
                        copy[oy, ox] + (quantization_error * weight),
                        a_min=0,
                        a_max=1,
                    )
                except IndexError:
                    pass

    return copy


def round_to_nearest_level(pixel: np.float64, level_count: int) -> np.float64:
    assert 0 <= pixel <= 1
    assert level_count >= 2

    gap_count = level_count - 1
    return np.round(pixel * gap_count) / gap_count


image = color.rgb2gray(data.logo())
dithered = dither_layer(image, 4)
# io.imshow(dithered)
# io.show()
