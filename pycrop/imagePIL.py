import os
import re

from PIL import Image


def assure_path_exists(path, f=True):
    if f:
        path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)


def normilize_size(size, img):

    if None not in size:
        return size

    W, H = img.size
    w, h = size

    if w is None:
        return h * W / H, h
    return w, w * H / W


class ImagePIL:

    def __init__(self, path, point=(50, 50), quality=90):
        self.path = os.path.abspath(path)
        self.point = point
        self.quality = quality

    def get_cover_size(self, from_size, to_size):
        p = max(
            to_size[0] / from_size[0],
            to_size[1] / from_size[1]
        )
        return (int(p * from_size[0]), int(p * from_size[1]))

    def get_contain_size(self, from_size, to_size):
        p = min(
            to_size[0] / from_size[0],
            to_size[1] / from_size[1]
        )
        return (int(p * from_size[0]), int(p * from_size[1]))

    def get_coords_from_center(self, from_size, to_size):
        coords = (
            int((from_size[0] - to_size[0]) / 2),
            int((from_size[1] - to_size[1]) / 2),
            int((from_size[0] + to_size[0]) / 2),
            int((from_size[1] + to_size[1]) / 2)
        )
        return coords

    def adjust_coords(self, coords, size, point):
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
        return tuple([int(sum(coord)) for coord in zip(coords, 2 * vec)])

    def default_save_path(self, *args, **kwargs):
        savepath, ext = os.path.splitext(self.path)

        savepath = '%s__w%dh%d%s' % (savepath, *size, ext)

    def cover(self, size, point=None, savepath=None, overwrite=True):
        with Image.open(self.path) as img:
            if point is None:
                point = self.point

            if savepath is None:
                savepath = self.default_save_path(size=size, method='cover')

            size = normilize_size(size, img)

            if not overwrite:
                if os.path.isfile(savepath):
                    return (True, savepath)

            cover_size = self.get_cover_size(img.size, size)

            coords = self.get_coords_from_center(cover_size, size)
            coords = self.adjust_coords(coords, cover_size, point)

            img = img.resize(cover_size, Image.ANTIALIAS)
            img = img.crop(coords)

            assure_path_exists(savepath)

            img.save(savepath, subsampling=0,
                     quality=self.quality, optimize=True)
            return (True, savepath)
        return (False,)

    def contain(self, size, savepath=None, overwrite=True):
        with Image.open(self.path) as img:

            if savepath is None:
                savepath = self.default_save_path(size=size, method='contain')

            size = normilize_size(size, img)

            if not overwrite:
                if os.path.isfile(savepath):
                    return (True, savepath)

            contain_size = self.get_contain_size(img.size, size)
            img = img.resize(contain_size, Image.ANTIALIAS)

            assure_path_exists(savepath)

            img.save(savepath, subsampling=0,
                     quality=self.quality, optimize=True)

            return (True, savepath)
        return (False,)


if __name__ == '__main__':

    img = ImagePIL(os.path.abspath('img.jpg'))
    img.contain((300, 230))
    img.cover((300, 230), point=(50, 10))
