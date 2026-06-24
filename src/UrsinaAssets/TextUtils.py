from ursina import Text, Vec3, color


class TextUtils(Text):
    def __init__(
        self,
        text="",
        position=Vec3(0, 0, 0),
        color=color.white,
        parent=None,
        origin=(0, 0),
        **kwargs,
    ):

        super().__init__(
            text=text,
            position=position,
            color=color,
            parent=parent,
            origin=origin,
            **kwargs,
        )

        self.rotation_x = 90
        self.scale = 30
