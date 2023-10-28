import json
import os

import imageio
import numpy


def rgb2gray(rgb):
    return numpy.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


def dothing(im):
    img = rgb2gray(imageio.imread("./assets/map/" + im + "/map.png"))
    sc = json.load(open("./assets/map/" + im + "/meta.json"))["shader_scale"]
    im2 = numpy.zeros((int(img.shape[0] / sc), int(img.shape[1] / sc)), dtype="uint8")
    for i in range(0, img.shape[0], sc):
        for j in range(0, img.shape[1], sc):
            im2[int(i / sc), int(j / sc)] = numpy.mean(img[i : i + sc, j : j + sc])

    imageio.imwrite("./assets/map/" + im + "/shade.png", im2)


for im in os.listdir("./assets/map/"):
    dothing(im)
