"""这个文件用于测试shadertoy在鼠标拖拽下进行描边的效果
2024.4.9 shader的编写和理解过于困难，完全不知道发生了什么事
先搁置，先把卡牌和选择写出来，后续技术成熟再回来写shader、特效"""

import arcade
import pyglet
from enum import Enum
from arcade import load_textures
from itertools import cycle
from hexlogic import HexCoords, hex_to_pixel
from pyglet.math import Vec2
from arcade.experimental import Shadertoy
from pathlib import Path

from charaters import Charater
from ENUMS.common_enums import SpeciesEnum
from player_data import PlayerData

"""
这个文件用于测试角色动画，实现灰琪在地图上上下左右移动的效果
"""


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


# pixel_font =
arcade.load_font("resources/fonts/fusion-pixel-10px-monospaced-zh_hans.ttf")

maud_pie_character = Charater(
    health=14,
    magic_attack=1,
    physical_attack=2,
    mental_attack=1,
    speed=1,
    name="maud_pie",
    collect_items=(1, 2, 3),
    species=SpeciesEnum.earth_pony,
)

maud_pie_player = PlayerData(maud_pie_character)

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

        self.player = maud_pie_player
        self.information = arcade.Text(
            text="",
            font_name="Fusion Pixel 10px Monospaced zh_hans",
            start_x=self.center_x + 50,
            start_y=self.center_y,
            color=arcade.color.BLUE,
            multiline=True,
            width=200,
        )
        self.show_text = False

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

        self.cur_texture = next(self.animation_sequance)
        if self.idle:
            self.cur_texture = 1

        def __repr__(self):
            return f"Maud Pie at {self.position}"

    def show_information(self):
        self.information.text = f"name:{self.player.name}\
            \nspecies:{self.player.species}\
            \nhealth:{self.player.health}\
            \nmagic_attack:{self.player.magic_attack}\
            \nphysical_attack:{self.player.physical_attack}\
            \nmental_attack:{self.player.mental_attack}\
            \nspeed:{self.player.speed}\
            \n来段中文，看看像素字体有没有生效"
        self.information.x = self.center_x + 50
        self.information.y = self.center_y


class MyGame(arcade.Window):
    """Our custom Window Class"""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.block_list = None
        self.camera_map = arcade.Camera()
        self.camera_map.move((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))
        # self.camera_map.position.x = -SCREEN_WIDTH / 2
        # self.camera_map.position.y = -SCREEN_HEIGHT / 2

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.held_player = None

        # self.shadertoy = None
        # self.channel0 = None
        # self.channel1 = None
        # self.load_shader()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_list.append(MaudPie())
        self.player_sprite = self.player_list[0]

    # def load_shader(self):
    #     window_size = self.get_size()

    #     self.shadertoy = Shadertoy.create_from_file(
    #         window_size, "shadertoy_test/step_1.glsl"
    #     )

    #     self.channel0 = self.shadertoy.ctx.framebuffer(
    #         color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
    #     )
    #     self.channel1 = self.shadertoy.ctx.framebuffer(
    #         color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
    #     )

    #     self.shadertoy.channel_0 = self.channel0.color_attachments[0]
    #     self.shadertoy.channel_1 = self.channel1.color_attachments[0]

    def on_draw(self):
        """Draw everything"""
        # self.channel0.use()
        # self.channel0.clear()

        self.use()

        self.clear()
        self.camera_map.use()
        self.player_list.draw(pixelated=True)
        if self.player_sprite.show_text:
            self.player_sprite.information.draw()
            self.player_list.draw_hit_boxes(color=arcade.color.GREEN)
            self.player_sprite.information.draw_hit_boxes(color=arcade.color.YELLOW)
        else:
            self.player_list.draw_hit_boxes(color=arcade.color.RED)
            self.player_sprite.information.draw_hit_boxes(color=arcade.color.BLUE)

            # self.shadertoy.render()

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
        self.player_sprite.show_information()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(self.camera_map.position)
        map_cords = self.camera_map.get_map_coordinates((x, y))
        players = arcade.get_sprites_at_point((map_cords), self.player_list)

        # 有玩家在点击的位置的情况，记录下玩家和玩家的位置
        if players:
            self.held_player = players[0]
            self.player_position_record = self.held_player.position

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        map_cords = self.camera_map.get_map_coordinates((x, y))
        players = arcade.get_sprites_at_point((map_cords), self.player_list)
        if players:
            self.player_sprite.show_text = True
        else:
            self.player_sprite.show_text = False
        if self.held_player:
            self.held_player.center_x += dx
            self.held_player.center_y += dy
            self.player_sprite.information.draw()

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.held_player:
            map_cords = self.camera_map.get_map_coordinates((x, y))

            self.held_player.position = map_cords

        self.held_player = None


window = MyGame()
window.setup()
arcade.run()
