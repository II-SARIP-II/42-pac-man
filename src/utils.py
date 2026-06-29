from ursina import Vec3


def convertPosToVec(coo: tuple[int, int], size: tuple[int, int]) -> Vec3:
    width, height = size
    x, y = coo

    x -= width / 2
    y =(height / 2) - y

    return Vec3(x, 0, y)
