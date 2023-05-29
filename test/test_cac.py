import numpy as np

from src.cac import compress


def test_compression():
    img = np.array([[1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0]])
    res = compress(img, (2, 2))
    answer = np.array(
        [np.array([1]), np.array([1, 0, 1, 0]), np.array([1]), np.array([1, 0, 1, 0])]
    )
    for i, j in zip(res, answer):
        assert np.array_equal(i, j)


def test_window_size_validation():
    img = np.array([[1, 1, 1, 0], [1, 1, 1, 0]])
    try:
        compress(img, (2, 3))
    except AssertionError:
        assert True
    else:
        assert False
