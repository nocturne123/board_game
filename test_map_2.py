import arcade
from arcade import load_textures
from enum import Enum
from ENUMS.common_enums import BlockTypeEnum
from pyglet.math import Vec2
import toml
from itertools import cycle
from hexlogic import HexCoords, hex_to_pixel

"""
这个文件是最主要的地图测试文件，现阶段所有的地图都在这里测试
已实现：基础地图的绘制
待实现：相机-包括相机的移动和缩放
"""

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

CHARACTER_SCALING = 0.5
MAP_BLOCK_PATH = "resources/map_config/base_map_hexlogic.toml"

TILE_SCALING = 1


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

Maud_Pie_file = (
    "resources/raw_character/mlp_pie_family_for_rpg_maker_by_zeka10000_dbo84ae.png"
)


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class MaudPie(arcade.Sprite):
    def __init__(self):
        super().__init__(hit_box_algorithm="None")

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

        self.hex_position = HexCoords(0, 0, 0)
        self.position = hex_to_pixel(self.hex_position, tile_width=26, tile_height=-24)

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


class MyGame(arcade.Window):
    """Our custom Window Class"""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_list = None
        self.block_list = None
        self.camera_map = arcade.SimpleCamera()
        self.camera_map.position.x = -SCREEN_WIDTH / 2
        self.camera_map.position.y = -SCREEN_HEIGHT / 2
        # move((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2))
        print(self.camera_map.position)

        # 角色操作相关设置
        self.held_player = None
        self.held_player_original_hex_position = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        self.block_list = arcade.SpriteList()
        self.block_list.extend(grass_block_list)
        self.block_list.extend(mountain_block_list)
        self.block_list.extend(dense_forest_block_list)
        self.block_list.extend(snow_block_list)
        self.block_list.extend(water_block_list)
        self.block_list.extend(town_block_list)

        self.player_list = arcade.SpriteList()

        self.player_list.append(MaudPie())

        self.block_list.sort(key=lambda x: x.center_y, reverse=True)
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """Draw everything"""
        self.clear()
        self.camera_map.use()
        self.block_list.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

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

    # TODO，需要更改移动到相机中心
    def camera_scroll(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = Vec2(
            self.player_sprite.center_x - self.width / 2,
            self.player_sprite.center_y - self.height / 2,
        )
        self.camera_map.move_to(position, 1.0)

    def on_update(self, delta_time: float):

        if self.up_pressed and not self.down_pressed:
            self.view_bottom = -1
        elif self.down_pressed and not self.up_pressed:
            self.view_bottom = +1
        if self.left_pressed and not self.right_pressed:
            self.view_left = -1
        elif self.right_pressed and not self.left_pressed:
            self.view_left = +1

        position = Vec2(self.view_left, self.view_bottom)
        position += self.camera_map.position
        self.camera_map.move_to(position, 1)
        # self.camera_map.move_to((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 2), 1)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_map.resize(int(width), int(height))
        self.camera_map.resize(int(width), int(height))

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        map_cords = self.camera_map.get_map_coordinates((x, y))
        players = arcade.get_sprites_at_point((map_cords), self.player_list)

        if players:
            self.held_player = players[0]
            self.held_player_original_hex_position = self.held_player.hex_position
        print(map_cords)
        print(self.held_player)
        print(players)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.held_player:
            self.held_player.center_x += dx
            self.held_player.center_y += dy

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if self.held_player:
            map_cords = self.camera_map.get_map_coordinates((x, y))
            blocks = arcade.get_sprites_at_point((map_cords), self.block_list)
            if blocks:
                block = blocks[0]
                self.held_player.hex_position = block.hex_position
                self.held_player.position = hex_to_pixel(
                    block.hex_position, tile_width=26, tile_height=-24
                )

            else:
                self.held_player.hex_position = self.held_player_original_hex_position
                self.held_player.position = hex_to_pixel(
                    self.held_player_original_hex_position,
                    tile_width=26,
                    tile_height=-24,
                )

        self.held_player = None
        self.held_player_original_hex_position = None


window = MyGame()
window.setup()
arcade.run()
