from ursina import Vec3


def convertPosToVec(coo: tuple[int, int], size: tuple[int, int]) -> Vec3:
    width, height = size
    x, y = coo

    x -= width / 2
    y = (height / 2) - y

    return Vec3(x, 0, y)


def convertVecToPos(pos: Vec3, size: tuple[int, int]) -> tuple[int, int]:
    width, height = size
    x_vec, _, y_vec = pos
    x = x_vec + (width / 2)
    y = (height / 2) - y_vec
    return (int(x), int(y))
