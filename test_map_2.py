import arcade
from ENUMS import BlockTypeEnum
from pyglet.math import Vec2
import toml

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

MAP_BLOCK_PATH = "resources/map_config/base_map.toml"

TILE_SCALING = 1

"""
# x轴向上，y轴向右的左手坐标系下的城镇坐标
# 草方块、水方块见resource文件夹下的y_axis_reverse_map.toml文件
# 此处为手动录入的城镇坐标

town_block1 = snow_castle_block(BlockTypeEnum.crystal_empire, 14, 4)
town_block2 = our_town_block(BlockTypeEnum.our_town, 12, 8)
town_block3 = town_block_no_fence(BlockTypeEnum.cloudsdale, 10, 2)
town_block4 = town_block_high_fence(BlockTypeEnum.canterlot, 10, 6)
town_block5 = town_block_with_fence(BlockTypeEnum.castle_of_friendship, 8, 4)
town_block6 = town_block_no_fence(BlockTypeEnum.manehattan, 8, 10)
town_block7 = town_block_no_fence(BlockTypeEnum.sweet_apple_acres, 6, 2)
town_block8 = town_block_no_fence(BlockTypeEnum.rainbow_dash_house, 6, 6)
town_block9 = town_block_no_fence(BlockTypeEnum.town_hall, 4, 4)
town_block10 = town_block_with_fence(BlockTypeEnum.baltimare, 4, 10)
town_block11 = town_block_no_fence(BlockTypeEnum.sugar_cube_corner, 2, 2)
town_block12 = town_block_no_fence(BlockTypeEnum.carousel_boutique, 0, 4)
town_block13 = town_block_no_fence(BlockTypeEnum.fluttershy_house, 2, 6)
town_block14 = town_block_no_fence(BlockTypeEnum.zecora_house, -4, 4)
town_block15 = snow_castle_block(BlockTypeEnum.old_castle, -2, 6)
town_block16 = tree_of_harmony_block(BlockTypeEnum.tree_of_harmony, -1, 7)
"""

# 手动录入的所有城镇方块
town_block1 = snow_castle_block(BlockTypeEnum.crystal_empire, 10, 0)
town_block2 = our_town_block(BlockTypeEnum.our_town, 8, -4)
town_block3 = town_block_no_fence(BlockTypeEnum.cloudsdale, 6, 2)
town_block4 = town_block_high_fence(BlockTypeEnum.canterlot, 6, -2)
town_block5 = town_block_with_fence(BlockTypeEnum.castle_of_friendship, 4, 0)
town_block6 = town_block_no_fence(BlockTypeEnum.manehattan, 4, -6)
town_block7 = town_block_no_fence(BlockTypeEnum.sweet_apple_acres, 2, 2)
town_block8 = town_block_no_fence(BlockTypeEnum.rainbow_dash_house, 2, -2)
town_block9 = town_block_no_fence(BlockTypeEnum.town_hall, 0, 0)
town_block10 = town_block_with_fence(BlockTypeEnum.baltimare, 0, -6)
town_block11 = town_block_no_fence(BlockTypeEnum.sugar_cube_corner, -2, 2)
town_block12 = town_block_no_fence(BlockTypeEnum.carousel_boutique, -4, 0)
town_block13 = town_block_no_fence(BlockTypeEnum.fluttershy_house, -2, -2)
town_block14 = town_block_no_fence(BlockTypeEnum.zecora_house, -8, 0)
town_block15 = snow_castle_block(BlockTypeEnum.old_castle, -6, -2)
town_block16 = tree_of_harmony_block(BlockTypeEnum.tree_of_harmony, -5, -3)

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

grass_block_list = [grass_block(x[0], x[1]) for x in grass_hex_list]
mountain_block_list = [mountain_block(x[0], x[1]) for x in mountain_hex_list]
dense_forest_block_list = [
    dense_forest_block(x[0], x[1]) for x in dense_forest_hex_list
]
snow_block_list = [snow_block(x[0], x[1]) for x in snow_hex_list]
water_block_list = [shallow_water_block(x[0], x[1]) for x in water_hex_list]


class MyGame(arcade.Window):
    """Our custom Window Class"""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_sprite = None
        self.block_list = None
        self.camera_map = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

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

        self.block_list.sort(key=lambda x: x.center_y, reverse=True)

    def on_draw(self):
        """Draw everything"""
        self.clear()
        self.camera_map.use()
        self.block_list.draw(pixelated=True)

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
    def scroll_to_player(self):
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
        self.camera_sprites.move_to(position, 1.0)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        # self.camera_sprites.resize(int(width), int(height))
        # self.camera_gui.resize(int(width), int(height))
        pass


window = MyGame()
window.setup()
arcade.run()
