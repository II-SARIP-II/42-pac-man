from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class InstructionScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0)
        )

        self.createScene()
        # gridLayout(self.container, 1.8)

    def createScene(self) -> None:
        self.createBackground()
        self.createText()
        self.createButtons()

    def createText(self) -> None:
        # Titre fixe, en haut de l'écran => z positif (avant du plan vu du dessus)
        self.title = TextUtils(
            parent=self.container,
            text="INSTRUCTIONS",
            color=color.yellow,
            scale=35.0,
            position=Vec3(0, 1, 4),
        )

        self.sections = Entity(parent=self.container, position=Vec3(0, 0, 0.5))

        self.createSection(title="MOVEMENT", lines=["WASD or Arrows"])
        self.createSection(title="PAUSE", lines=["Echap"])
        self.createSection(
            title="CHEAT MODE",
            lines=[
                "Toggle All  -  C",
                "Invincibility  -  B",
                "Increase Speed  -  V",
                "Freeze Ghosts  -  Z",
                "Infinite Lives - X"
            ],
        )

        # gridLayout espace les sections sur z -> cohérent avec la vue du dessus
        gridLayout(self.sections, 1.8)

    def createSection(self, title: str, lines: list[str]) -> Entity:
        section = Entity(parent=self.sections)

        TextUtils(
            parent=section,
            text=title,
            color=color.azure,
            scale=25.0,
            line_height=2,
            position=Vec3(0, 0, 0),
        )

        for i, line in enumerate(lines):
            TextUtils(
                parent=section,
                text=line,
                scale=20.0,
                line_height=2,
                position=Vec3(0, 0, -(i + 1) * 0.60),
            )

        return section

    def createButtons(self) -> None:
        self.button_return = ButtonUtils(
            text="RETURN",
            position=Vec3(0, 1, -6),
            action=lambda: self.onClickReturn(),
            button_color=color.dark_gray,
            parent=self.container,
        )

    def onClickReturn(self) -> None:
        self.game_engine.changeScene(self.game_engine.prev_scene)
