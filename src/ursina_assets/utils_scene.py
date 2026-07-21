from ursina import Entity


def gridLayout(container: Entity, spacing: float) -> None:
    """Arrange an entity's children in a single evenly-spaced column.

    Centers the children around the container's local origin along the
    z-axis, resetting their x position and lifting them to y=1.

    Args:
        container (Entity): The entity whose children should be laid
            out.
        spacing (float): Distance between consecutive children along
            the z-axis.

    Returns:
        None.
    """
    total_childen = len(container.children)

    center_offset = (total_childen - 1) / 2

    for i, child in enumerate(container.children):
        child.x = 0
        child.z = -(i - center_offset) * spacing
        child.y = 1
