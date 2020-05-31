from typing import *
from argparse import ArgumentParser, Namespace
import os
from image_io import read_image, save_image
from dither_image import dither_image


def main() -> None:
    parser = ArgumentParser(
        "Batch dither images using Floyd-Steinberg algorithm."
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="whether to dither images as grayscale or colored",
        default="grayscale",
        choices=["grayscale", "colored"],
    )
    parser.add_argument(
        "-s",
        "--shade-count",
        help="number of unique pixel colors in dithered images",
        default=4,
        type=int,
    )
    parser.add_argument("images", help="paths of images to dither", nargs="+")
    parser.add_argument(
        "out_dir", help="directory where dithered images will be stored"
    )

    args = parser.parse_args()

    for image_path in args.images:
        image = read_image(image_path)
        print(f"Loaded {image_path}.")

        dithered = dither_image(
            image,
            grayscale=args.mode == "grayscale",
            shade_count=args.shade_count,
        )
        print(f"Dithered {image_path}.")

        image_name = os.path.basename(image_path)
        destination = os.path.join(args.out_dir, image_name)
        save_image(destination, dithered)
        print(f"Saved to {destination}.")


main()

