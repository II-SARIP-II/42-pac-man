from typing import TYPE_CHECKING

from ursina import Entity, Vec3

from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class InstructionScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)
