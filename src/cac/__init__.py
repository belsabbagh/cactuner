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
