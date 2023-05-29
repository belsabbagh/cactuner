import numpy as np

DELIMITER = -1


class CompressedImage:
    def __init__(self, code, shape, window_shape, block_shape):
        self.code = code
        self.shape = shape
        self.window_shape = window_shape
        self.block_shape = block_shape


def img_slicer(img, w_shape):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array should look like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = img.shape
    nrows, ncols = w_shape
    assert h % nrows == 0, f"{h} rows is not evenly divisible by {nrows}"
    assert w % ncols == 0, f"{w} cols is not evenly divisible by {ncols}"
    return (
        img.reshape(h // nrows, nrows, -1, ncols)
        .swapaxes(1, 2)
        .reshape(-1, nrows, ncols)
    )


def compress(img: np.ndarray, window_shape=None):
    window_shape = window_shape if window_shape is not None else (2, 3)
    """
    Compresses the image using Constant Area Coding.
    """

    def encode(w):
        return np.array([w[0][0]]) if len(set(w.flatten())) == 1 else w.flatten()

    h, w = img.shape
    nrows, ncols = window_shape
    assert h % nrows == 0, f"{h} rows is not evenly divisible by {nrows}"
    assert w % ncols == 0, f"{w} cols is not evenly divisible by {ncols}"
    assert nrows > 0 and ncols > 0, "Window shape must be greater than 0"
    assert nrows <= h and ncols <= w, "Window shape must be smaller than image shape"
    buffer = []
    for window in img_slicer(img, window_shape):
        buffer.append(encode(window))
    return np.array(buffer)


def decompress(
    code: np.ndarray, target_size: tuple[int, int], window_size: tuple[int, int]
) -> np.ndarray:
    pass


def compression_ratio(img, compression):
    return np.prod(img.shape) / sum([len(i) for i in compression])


def rel_data_redundancy(img, compression):
    return 1 - 1 / compression_ratio(img, compression)


def get_block_type(image_array, block_width, block_height, w_start, h_start):
    has_white = False
    has_black = False
    for w in range(w_start, w_start + block_width):
        for h in range(h_start, h_start + block_height):
            if image_array[h][w]:
                has_white = True
            else:
                has_black = True
            if has_white and has_black:
                return 'M'
    if has_white:
        return 'W'
    elif has_black:
        return 'B'


def blocks_counter_encoder(blocks_array):
    unique, counts = np.unique(blocks_array, return_counts=True)
    counter = dict(zip(unique, counts))
    codes = counter.copy()
    max_count = max(counter, key=counter.get)
    codes[max_count] = '0'
    i = 0
    for key, value in counter.items():
        if key is not max_count:
            if len(counter) == 2:
                codes[key] = '1'
            elif len(counter) == 3:
                if i == 0:
                    codes[key] = '01'
                    i = i + 1
                elif i == 1:
                    codes[key] = '11'
    return counter, codes


def CAC(image_array, block_width, block_height, debug=False, get_result=False):
    image_width = len(image_array[0])
    image_height = len(image_array)
    blocks_array = np.asarray(
        [[get_block_type(image_array, block_width, block_height, x * block_width, y * block_height)
          for x in range(int(image_width / block_width))] for y in range(int(image_height / block_height))])
    counter, codes = blocks_counter_encoder(blocks_array)
    N1 = image_width * image_height
    N2 = 0
    for key, value in counter.items():
        if key == 'M':
            N2 = N2 + value * (len(codes[key]) + block_width * block_height)
        else:
            N2 = N2 + (value * len(codes[key]))
    CR = N1 / N2
    if get_result:
        with open("Result.txt", "w") as result:
            for h in range(len(blocks_array)):
                for w in range(len(blocks_array[0])):
                    if blocks_array[h][w] == 'M':
                        result.write(codes['M'])
                        for hx in range(h * block_height, (h + 1) * block_height):
                            for wx in range(w * block_width, (w + 1) * block_width):
                                result.write(str(int(image_array[hx][wx])))
                    else:
                        result.write(codes[blocks_array[h][w]])
            result.close()
    else:
        open("Result.txt", "w").close()
    if debug:
        print("For Block Size (Width*Height): (" + str(block_width) + "*" + str(block_height) + ")")
        print("Blocks Counter: " + str(counter))
        print("Blocks Codes:   " + str(codes))
        print("Blocks Array Size (Width*Height): (" + str(len(blocks_array[0])) + "*" + str(len(blocks_array)) + ")")
        print("Blocks Array:")
        print(blocks_array)
        print("Compression Ratio (N1/N2): (" + str(N1) + "/" + str(N2) + ") = " + str(CR))
        print("Result: Result.txt")
    return CR
