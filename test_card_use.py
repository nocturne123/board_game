"""这个文件将前期工作组合起来，实现在地图上打出一张攻击牌的效果
具体需要实现的包括：从player_data到player_action到player到player_sprite的创建
地图的创建
完善卡牌的打出逻辑，把card的逻辑和card_sprite的逻辑分开
card负责生效，card_sprite负责处理在手中、打出、打出后的逻辑
现在还不用管game、轮次相关的逻辑，先把牌打出来一张再说"""

import arcade
from arcade import load_textures, load_texture
from enum import Enum
from pathlib import Path
from ENUMS.common_enums import BlockTypeEnum, SpeciesEnum
from pyglet.math import Vec2
import toml
from itertools import cycle
from hexlogic import HexCoords, hex_to_pixel
from charaters import Charater
from player_data import PlayerData
from player import Player
from player_action import PlayerAction
from PIL import Image

from map_block import (
    grass_block,
    mountain_block,
    shallow_water_block,
    dense_forest_block,
    snow_block,
    snow_castle_block,
    our_town_block,
    town_block_no_fence,
    town_block_high_fence,
    town_block_with_fence,
    tree_of_harmony_block,
)

SCREEN_TITLE = "Test Map"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

VECTOR_PONY_SCALING = 0.12

CHARACTER_SCALING = 0.5
MAP_BLOCK_PATH = "resources/map_config/base_map_hexlogic.toml"

# 字体
arcade.load_font("resources/fonts/fusion-pixel-10px-monospaced-zh_hans.ttf")

TILE_SCALING = 2
TILE_WIDTH = 32
TILE_HEIGHT = -28

# 地图的加载
# 相比于test_map_2.py，这里用一个函数将地图的加载逻辑打个包，方便查看


def load_map_block():
    """返回所有地图块"""

    block_list = arcade.SpriteList()

    town_block1 = town_block_no_fence(BlockTypeEnum.cloudsdale, -2, -2, 4)
    town_block2 = town_block_no_fence(BlockTypeEnum.sweet_apple_acres, -2, 0, 2)
    town_block3 = town_block_no_fence(BlockTypeEnum.sugar_cube_corner, -2, 2, 0)
    town_block4 = snow_castle_block(BlockTypeEnum.crystal_empire, 0, -5, 5)
    town_block5 = town_block_with_fence(BlockTypeEnum.castle_of_friendship, 0, -2, 2)
    town_block6 = town_block_no_fence(BlockTypeEnum.town_hall, 0, 0, 0)
    town_block7 = town_block_no_fence(BlockTypeEnum.carousel_boutique, 0, 2, -2)
    town_block8 = town_block_no_fence(BlockTypeEnum.zecora_house, 0, 4, -4)
    town_block9 = town_block_high_fence(BlockTypeEnum.canterlot, 2, -4, 2)
    town_block10 = town_block_no_fence(BlockTypeEnum.rainbow_dash_house, 2, -2, 0)
    town_block11 = town_block_no_fence(BlockTypeEnum.fluttershy_house, 2, 0, -2)
    town_block12 = snow_castle_block(BlockTypeEnum.old_castle, 2, 2, -4)
    town_block13 = tree_of_harmony_block(BlockTypeEnum.tree_of_harmony, 3, 1, -4)
    town_block14 = our_town_block(BlockTypeEnum.our_town, 4, -6, 2)
    town_block15 = town_block_no_fence(BlockTypeEnum.manehattan, 6, -5, -1)
    town_block16 = town_block_with_fence(BlockTypeEnum.baltimare, 6, -3, -3)

    town_block_list = [
        town_block1,
        town_block2,
        town_block3,
        town_block4,
        town_block5,
        town_block6,
        town_block7,
        town_block8,
        town_block9,
        town_block10,
        town_block11,
        town_block12,
        town_block13,
        town_block14,
        town_block15,
        town_block16,
    ]

    with open(MAP_BLOCK_PATH, "r") as map_toml:
        map_dic = toml.load(map_toml)

    grass_hex_list = map_dic["grass_hex_list"]
    mountain_hex_list = map_dic["mountain_hex_list"]
    dense_forest_hex_list = map_dic["dense_forest_hex_list"]
    snow_hex_list = map_dic["snow_hex_list"]
    water_hex_list = map_dic["water_hex_list"]

    grass_block_list = [grass_block(x[0], x[1], x[2]) for x in grass_hex_list]
    mountain_block_list = [mountain_block(x[0], x[1], x[2]) for x in mountain_hex_list]
    dense_forest_block_list = [
        dense_forest_block(x[0], x[1], x[2]) for x in dense_forest_hex_list
    ]
    snow_block_list = [snow_block(x[0], x[1], x[2]) for x in snow_hex_list]
    water_block_list = [shallow_water_block(x[0], x[1], x[2]) for x in water_hex_list]
    block_list.extend(grass_block_list)
    block_list.extend(mountain_block_list)
    block_list.extend(snow_block_list)
    block_list.extend(water_block_list)
    block_list.extend(dense_forest_block_list)
    block_list.extend(town_block_list)
    block_list.sort(key=lambda x: x.center_y, reverse=True)

    return block_list


# 基础玩家数据
sun_burst = Charater(
    health=13,
    magic_attack=2,
    physical_attack=2,
    mental_attack=1,
    speed=1,
    name="sun_burst",
    collect_items=(1, 2, 3),
    species=SpeciesEnum.pegasi,
)

derpy = Charater(
    health=13,
    magic_attack=0,
    physical_attack=3,
    mental_attack=3,
    speed=2,
    name="derpy",
    collect_items=(1, 2, 3),
    species=SpeciesEnum.pegasi,
)

maud_pie = Charater(
    health=14,
    magic_attack=1,
    physical_attack=2,
    mental_attack=1,
    speed=1,
    name="maud_pie",
    collect_items=(1, 2, 3),
    species=SpeciesEnum.earth_pony,
)

# 玩家
sun_burst_player = Player(sun_burst)
derpy_player = Player(derpy)
maud_pie_player = Player(maud_pie)

# 位置初始化
derpy_player.data.hex_position = HexCoords(1, -2, 1)
maud_pie_player.data.hex_position = HexCoords(3, -3, 0)


class PlayerSprite(arcade.Sprite):
    def __init__(
        self,
        path_or_texture: str | Path | arcade.Texture | None = None,
        player: Player = None,
        scale: float = VECTOR_PONY_SCALING,
        center_x: float = 0,
        center_y: float = 0,
        angle: float = 0,
        **kwargs,
    ):
        super().__init__(path_or_texture, scale, center_x, center_y, angle, **kwargs)
        self.player = player
        self.hex_position = player.data.hex_position
        self.position = hex_to_pixel(
            self.hex_position,
            tile_width=TILE_SCALING * TILE_WIDTH,
            tile_height=TILE_SCALING * TILE_HEIGHT,
        )


# 玩家精灵
sun_burst_sprite = PlayerSprite(
    Path(r"resources\raw_character\mlp_vector_club\sun_burst.png"),
    player=sun_burst_player,
    scale=VECTOR_PONY_SCALING,
)
maud_pie_sprite = PlayerSprite(
    Path(r"resources\raw_character\mlp_vector_club\maud.png"),
    player=maud_pie_player,
    scale=VECTOR_PONY_SCALING,
)
derpy_sprite = PlayerSprite(
    Path(r"resources\raw_character\mlp_vector_club\derpy.png"),
    player=derpy_player,
    scale=VECTOR_PONY_SCALING,
)


class MyGame(arcade.Window):
    """Our custom Window Class"""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.block_list = None
        self.camera_map = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.held_player = None
        self.held_player_original_hex_position = None

        self.held_block = None

    def setup(self):
        self.camera_map = arcade.SimpleCamera()
        self.camera_map.position.x = -SCREEN_WIDTH / 2
        self.camera_map.position.y = -SCREEN_HEIGHT / 2

        # 玩家列表
        self.player_list = arcade.SpriteList()
        self.player_list.append(maud_pie_sprite)
        self.player_list.append(sun_burst_sprite)
        self.player_list.append(derpy_sprite)

        # 地图块列表
        self.block_list = load_map_block()

        # 手牌列表
        self.hand_list = arcade.SpriteList()

        # 信息展示
        self.information = arcade.Text(
            text="",
            font_name="Fusion Pixel 10px Monospaced zh_hans",
            start_x=0,
            start_y=0,
            color=arcade.color.BLUE,
            multiline=True,
            width=200,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            map_cords = self.camera_map.get_map_coordinates((x, y))
            players = arcade.get_sprites_at_point((map_cords), self.player_list)

            if players:
                self.held_player = players[0]
                self.held_player_original_hex_position = self.held_player.hex_position

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        map_cords = self.camera_map.get_map_coordinates((x, y))
        blocks = arcade.get_sprites_at_point((map_cords), self.block_list)

        # 文字显示的逻辑
        players = arcade.get_sprites_at_point((map_cords), self.player_list)
        if players:
            player_sprite = players[0]
            data = player_sprite.player.data
            self.information.text = f"name:{data.name}\
            \nspecies:{data.species}\
            \nhealth:{data.health}\
            \nmagic_attack:{data.magic_attack}\
            \nphysical_attack:{data.physical_attack}\
            \nmental_attack:{data.mental_attack}\
            \nspeed:{data.speed}\
            \n来段中文，看看像素字体有没有生效"

            self.information.x = player_sprite.center_x + 50
            self.information.y = player_sprite.center_y
        else:
            self.information.text = ""

        if blocks:
            self.held_block = blocks[0]
        if self.held_player:
            self.held_player.center_x += dx
            self.held_player.center_y += dy

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.held_player:
                map_cords = self.camera_map.get_map_coordinates((x, y))
                blocks = arcade.get_sprites_at_point((map_cords), self.block_list)
                if blocks:
                    block = blocks[0]
                    self.held_player.hex_position = block.hex_position
                    self.held_player.position = hex_to_pixel(
                        block.hex_position,
                        tile_width=TILE_SCALING * TILE_WIDTH,
                        tile_height=TILE_SCALING * TILE_HEIGHT,
                    )

                else:
                    self.held_player.hex_position = (
                        self.held_player_original_hex_position
                    )
                    self.held_player.position = hex_to_pixel(
                        self.held_player_original_hex_position,
                        tile_width=TILE_SCALING * TILE_WIDTH,
                        tile_height=TILE_SCALING * TILE_HEIGHT,
                    )

            self.held_player = None
            self.held_player_original_hex_position = None

    def on_update(self, delta_time: float):

        if self.up_pressed and not self.down_pressed:
            self.view_bottom = -5
        elif self.down_pressed and not self.up_pressed:
            self.view_bottom = +5
        else:
            self.view_bottom = 0

        if self.left_pressed and not self.right_pressed:
            self.view_left = +5
        elif self.right_pressed and not self.left_pressed:
            self.view_left = -5
        else:
            self.view_left = 0

        position = Vec2(self.view_left, self.view_bottom)
        position += self.camera_map.position
        self.camera_map.move_to(position, 1)

    def on_draw(self):
        """Render the screen."""
        self.clear()
        self.camera_map.use()
        self.block_list.draw()
        if self.held_block:
            self.held_block.draw_hit_box(color=arcade.color.GREEN)
        self.player_list.draw()
        if self.information.text:
            self.information.draw()


window = MyGame()
window.setup()
arcade.run()
