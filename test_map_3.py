import arcade
from enum import Enum
from arcade import load_textures
from itertools import cycle

"""
这个文件用于测试角色动画，实现灰琪在地图上上下左右移动的效果
"""


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


Maud_Pie_file = (
    "resources/raw_character/mlp_pie_family_for_rpg_maker_by_zeka10000_dbo84ae.png"
)


SCREEN_TITLE = "Maud Pie Moves Around"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

CHARACTER_SCALING = 1

TILE_SCALING = 1

down_texture_range_x = range(144, 289, 48)


class MaudPie(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = Direction.RIGHT
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        self.idle = True

        self.timer = 0
        self.frame_time = 0.1

        self.facing_right_textures = []
        textures = load_textures(
            Maud_Pie_file, [(x, 48 * 2, 48, 48) for x in range(48 * 3, 48 * 6 + 1, 48)]
        )
        self.facing_right_textures.extend(textures)

        self.facing_down_textures = []
        textures = load_textures(
            Maud_Pie_file, [(x, 48 * 0, 48, 48) for x in range(48 * 3, 48 * 6 + 1, 48)]
        )
        self.facing_down_textures.extend(textures)

        self.facing_left_textures = []
        textures = load_textures(
            Maud_Pie_file, [(x, 48 * 1, 48, 48) for x in range(48 * 3, 48 * 6 + 1, 48)]
        )
        self.facing_left_textures.extend(textures)

        self.facing_up_textures = []
        textures = load_textures(
            Maud_Pie_file, [(x, 48 * 3, 48, 48) for x in range(48 * 3, 48 * 6 + 1, 48)]
        )
        self.facing_up_textures.extend(textures)

        self.texture = self.facing_right_textures[self.cur_texture]

        self.animation_sequance = cycle([1, 0, 1, 2])

    def update_animation(self, delta_time: float = 1 / 60):

        self.timer += delta_time
        if self.timer < self.frame_time:
            return
        self.timer = 0
        if self.character_face_direction == Direction.RIGHT:
            self.texture = self.facing_right_textures[self.cur_texture]
        elif self.character_face_direction == Direction.LEFT:
            self.texture = self.facing_left_textures[self.cur_texture]
        elif self.character_face_direction == Direction.UP:
            self.texture = self.facing_up_textures[self.cur_texture]
        elif self.character_face_direction == Direction.DOWN:
            self.texture = self.facing_down_textures[self.cur_texture]

        animation_sequance = [1, 0, 1, 2]
        self.cur_texture = next(self.animation_sequance)
        if self.idle:
            self.cur_texture = 1


class MyGame(arcade.Window):
    """Our custom Window Class"""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_sprite = None
        self.block_list = None
        self.camera_map = arcade.Camera()

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        self.player_sprite = MaudPie()
        self.player_sprite.center_x = 300
        self.player_sprite.center_y = 300

    def on_draw(self):
        """Draw everything"""
        self.clear()
        self.camera_map.use()
        self.player_sprite.draw(pixelated=True)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        self.player_sprite.idle = False

        if key == arcade.key.UP:
            self.player_sprite.character_face_direction = Direction.UP
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.player_sprite.character_face_direction = Direction.DOWN
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.player_sprite.character_face_direction = Direction.LEFT
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.player_sprite.character_face_direction = Direction.RIGHT
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        self.player_sprite.idle = True
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time: float):
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.center_y += 1
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.center_y -= 1
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.center_x -= 1
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.center_x += 1
        self.player_sprite.update_animation()


window = MyGame()
window.setup()
arcade.run()
