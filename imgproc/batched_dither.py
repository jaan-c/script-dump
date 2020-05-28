import numpy as np
from skimage import img_as_int, data, io, color
from timeit import default_timer as timer

# Integer based image dithering.
def dither_grayscale(image: np.ndarray, *, level_count: int = 4) -> np.ndarray:
    if len(image.shape) != 2:
        raise ValueError(
            f"image is not grayscale, contains {image.shape[2]} color channels."
        )
    elif image.dtype.type is np.float64:
        raise ValueError("image must contain numpy.float64.")

    copy = image.copy()
    height, width = copy.shape
    gap_count = level_count - 1
    offsets_and_weights = [
        # (x_offset, y_offset, distribution_weight)
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


image = data.camera()
image = color.rgb2gray(image)
image = img_as_int(image)

start = timer()
dithered = dither_grayscale(image, level_count=4)
end = timer()

io.imshow(dithered)
io.show()

print(f"{end - start} sec")
