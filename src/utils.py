from ursina import Vec3


def convertPosToVec(coo: tuple[int, int], size: tuple[int, int]) -> Vec3:
    """Convert a grid coordinate to a world-space position.

    Args:
        coo (tuple[int, int]): Grid coordinate to convert.
        size (tuple[int, int]): Level grid (width, height).

    Returns:
        Vec3: The corresponding world-space position.
    """
    width, height = size
    x = float(coo[0])
    y = float(coo[1])

    x -= width / 2
    y = (height / 2) - y

    return Vec3(x, 0.1, y)


def convertVecToPos(pos: Vec3, size: tuple[int, int]) -> tuple[int, int]:
    """Convert a world-space position back to a grid coordinate.

    Inverse of `convertPosToVec`.

    Args:
        pos (Vec3): World-space position to convert.
        size (tuple[int, int]): Level grid (width, height).

    Returns:
        tuple[int, int]: The corresponding grid coordinate.
    """
    width, height = size
    x_vec, _, y_vec = pos
    x = x_vec + (width / 2)
    y = (height / 2) - y_vec
    return (int(x), int(y))
