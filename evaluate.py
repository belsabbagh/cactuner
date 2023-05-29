from os import listdir
from os.path import isfile, join
import time

import pandas as pd

from src.image_handler import image_compression, image_reading


def image_iter(dirpath="data"):
    """Iterates through all images in a directory"""
    for f in listdir(dirpath):
        if isfile(join(dirpath, f)):
            yield f, image_reading(join(dirpath, f), verbose=False)


def base_test(img, ga=False):
    """Runs a single test"""
    start = time.time()
    res = image_compression(img, use_genetic_algorithm=ga, debug=False)
    end = time.time()
    return res, end - start


if __name__ == "__main__":
    results = pd.DataFrame(columns=["Image", "BF_CR", "BF_time", "GA_CR", "GA_time"])
    results.index.name = "Image"
    for name, image in image_iter():
        ga_res, ga_time = base_test(image, ga=True)
        bf_res, bf_time = base_test(image, ga=False)
        res = {
            "Image": name,
            "BF_CR": bf_res["CR"],
            "BF_time": bf_time,
            "GA_CR": ga_res["CR"],
            "GA_time": ga_time,
        }
        results = pd.concat([results, pd.DataFrame(res, index=[name])])
        print("Finished " + name)
    results.to_csv("results.csv")
