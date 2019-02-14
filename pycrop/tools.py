import os
import re
from math import floor

from PIL import Image


def default_save_path(path, size):
    savepath, ext = os.path.splitext(path)
    savepath = '%s__w%dh%d%s' % (savepath, *size, ext)
    return savepath


def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def normilize_size(size, img_size):

    if None not in size:
        return size

    W, H = img_size
    w, h = size

    if w is None:
        return h * W / H, h
    return w, w * H / W


def get_cover_size(from_size, to_size):
    p = max([ts / fs for ts, fs in zip(to_size, from_size)])
    return tuple(floor(p * fs) for fs in from_size)


def get_contain_size(from_size, to_size):
    p = min([ts / fs for ts, fs in zip(to_size, from_size)])
    return tuple(floor(p * fs) for fs in from_size)


def get_coords_from_center(from_size, to_size):
    return (
        floor((from_size[0] - to_size[0]) / 2),
        floor((from_size[1] - to_size[1]) / 2),
        floor((from_size[0] + to_size[0]) / 2),
        floor((from_size[1] + to_size[1]) / 2)
    )


def adjust_coords(coords, size, point):
    vec = [
        size[0] * (point[0] - 50) / 100,
        size[1] * (point[1] - 50) / 100
    ]

    if coords[0] + vec[0] < 0:
        vec[0] = - coords[0]
    if coords[1] + vec[1] < 0:
        vec[1] = - coords[1]
    if coords[3] + vec[1] > size[1]:
        vec[1] = size[1] - coords[3]
    if coords[2] + vec[0] > size[0]:
        vec[0] = size[0] - coords[2]

    return tuple(floor(sum(coord)) for coord in zip(coords, 2 * vec))


def cover(path, size, point, savepath=None, quality=90):
    with Image.open(path) as img:
        size = normilize_size(size, img.size)

        if savepath is None:
            savepath = default_save_path(path, size)
        assure_path_exists(os.path.dirname(savepath))

        cover_size = get_cover_size(img.size, size)

        coords = get_coords_from_center(cover_size, size)
        coords = adjust_coords(coords, cover_size, point)

        img = img.resize(cover_size, Image.ANTIALIAS)
        img = img.crop(coords)

        img.save(savepath, subsampling=0,
                 quality=quality, optimize=True)
        return (True, savepath)
    return (False, '')


def contain(path, size, savepath=None, quality=90):
    with Image.open(path) as img:
        size = normilize_size(size, img.size)

        if savepath is None:
            savepath = default_save_path(path, size)
        assure_path_exists(os.path.dirname(savepath))

        contain_size = get_contain_size(img.size, size)
        img = img.resize(contain_size, Image.ANTIALIAS)

        img.save(savepath, subsampling=0,
                 quality=quality, optimize=True)

        return (True, savepath)
    return (False, '')


if __name__ == "__main__":

    img_path = os.path.abspath('img.jpg')

    cover(img_path, (500, None), (50, 50))
