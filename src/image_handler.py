import math
import time
import numpy as np
from PIL import Image
from src.cac import CAC
from src.cac.optimizers.bf import brute_force

from src.cac.optimizers.ga import genetic_algorithm


def image_reading(filepath, verbose=True):
    """Reads an image and outputs"""
    if verbose:
        print(f"{' Image Reading ':=^150}")
        print("Image File: " + filepath)
    image = Image.open(filepath).convert("1")
    if verbose:
        print(f"Image Metadata: {dict(mode=image.mode, size=image.size)}")
    return np.asarray(image)


def divisor_generator(n):
    """Generator of divisors of n excluding 1 and n to be used as block size dimensions"""
    divisors = []
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            divisors.append(i)
            if i * i != n:
                large_divisors.append(int(n / i))
    return sorted(divisors + large_divisors)


def image_compression(image_array, use_genetic_algorithm=False, debug=False):
    """Compresses an image using CAC and either brute force or genetic algorithm"""
    start_time = time.time()
    # print(f"{' Image Compression ':=^150}")
    block_sizes = generate_block_sizes(image_array.shape)
    max_CR = (
        genetic_algorithm(image_array, block_sizes, debug=debug)
        if use_genetic_algorithm
        else brute_force(image_array, block_sizes, debug=debug)
    )
    # print(" " * 25 + "=" * 100)
    temp_string = str("# Maximum Compression Ratio: " + str(max_CR["CR"]))
    # print(temp_string)
    # print("=" * len(temp_string))
    CAC(
        image_array,
        max_CR["block_width"],
        max_CR["block_height"],
        get_result=True,
        debug=debug,
    )
    # print("=" * 150)
    execution_time = time.time() - start_time
    # print("# Program Execution Time: " + str(execution_time) + " Seconds")
    # print("=" * 150)
    return max_CR

def generate_block_sizes(img_shape):
    """Generates a list of possible block sizes given the image shape"""
    block_heights, block_widths = [divisor_generator(i) for i in img_shape]
    # print("# Possible Block Widths:  " + str(block_widths))
    # print("# Possible Block Heights: " + str(block_heights))
    res = [(w, h) for w in block_widths for h in block_heights]
    # print("# Number of Possible Block Sizes (Width*Height): " + str(len(res)))
    return res