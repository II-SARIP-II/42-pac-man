from ursina import Entity


def gridLayout(container: Entity, spacing: float) -> None:
    total_childen = len(container.children)

    center_offset = (total_childen - 1) / 2

    for i, child in enumerate(container.children):
        child.x = 0
        child.z = -(i - center_offset) * spacing
        child.y = 1
