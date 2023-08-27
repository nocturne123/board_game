from hexutil import Hex, HexPathFinder
import arcade
from pathlib import Path
from pprint import pprint
from ENUMS import BlockTypeEnum

SCREEN_TITLE = "Test Map"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

TILE_SCALING = 1


def hex_to_pixel(hex: Hex) -> tuple:
    """Converts a hex coordinate to a pixel coordinate
    将六边形坐标转换为像素坐标
    """
    hex_x = hex[0]
    hex_y = hex[1]
    return (hex_y * 24, hex_x * 13)


class map_block(arcade.Sprite):
    def __init__(
        self,
        block_type: BlockTypeEnum = BlockTypeEnum.grass,
        image_x=0,
        image_y=0,
        hex_x=0,
        hex_y=0,
    ):
        super().__init__(
            filename="resources/images/fantasyhextiles_v3.png",
            image_width=32,
            image_height=48,
            scale=TILE_SCALING,
            image_x=image_x,
            image_y=image_y,
            center_x=300 + hex_to_pixel(Hex(hex_x, hex_y))[0],
            center_y=300 + hex_to_pixel(Hex(hex_x, hex_y))[1],
        )
        self.hex_position = Hex(hex_x, hex_y)
        self.type: BlockTypeEnum = block_type


# 下面是具体的地图图块定义，除了具体城镇，其他图块不用传入block_type参数
class grass_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.grass,
            image_x=0,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class little_forest_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            image_x=32,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class dense_forest_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.dense_forest,
            image_x=64,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class rock_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            image_x=96,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class spruce_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            image_x=128,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class mountain_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.mountain,
            image_x=160,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class shallow_water_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.water,
            image_x=192,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class deep_water_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.water,
            image_x=224,
            image_y=0,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class town_block_no_fence(map_block):
    def __init__(self, block_type, hex_x, hex_y):
        super().__init__(
            block_type=block_type,
            image_x=0,
            image_y=48,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class town_block_with_fence(map_block):
    def __init__(self, block_type, hex_x, hex_y):
        super().__init__(
            block_type=block_type,
            image_x=32,
            image_y=48,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class town_block_high_fence(map_block):
    def __init__(self, block_type, hex_x, hex_y):
        super().__init__(
            block_type=block_type,
            image_x=64,
            image_y=48,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class snow_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.snow,
            image_x=0,
            image_y=96,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class snow_little_forest_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.snow,
            image_x=32,
            image_y=96,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class snow_dense_forest_block(map_block):
    def __init__(self, hex_x, hex_y):
        super().__init__(
            block_type=BlockTypeEnum.snow,
            image_x=64,
            image_y=96,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class snow_town_block(map_block):
    def __init__(self, block_type, hex_x, hex_y):
        super().__init__(
            block_type=block_type,
            image_x=192,
            image_y=96,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class snow_castle_block(map_block):
    def __init__(self, block_type, hex_x, hex_y):
        super().__init__(
            block_type=block_type,
            image_x=224,
            image_y=96,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class our_town_block(map_block):
    def __init__(self, block_type, hex_x, hex_y):
        super().__init__(
            block_type=block_type,
            image_x=0,
            image_y=240,
            hex_x=hex_x,
            hex_y=hex_y,
        )


class tree_of_harmony_block(map_block):
    def __init__(self, block_type, hex_x, hex_y):
        super().__init__(
            block_type=block_type,
            image_x=128,
            image_y=48,
            hex_x=hex_x,
            hex_y=hex_y,
        )


# 手动录入的所有草方块
grass_block1 = grass_block(0, 0)
grass_block2 = grass_block(-1, 1)
grass_block3 = grass_block(0, 2)
grass_block4 = grass_block(1, 3)
grass_block5 = grass_block(2, 4)
grass_block6 = grass_block(3, 5)
grass_block7 = grass_block(4, 6)
grass_block8 = grass_block(3, 3)
grass_block9 = grass_block(5, 3)
grass_block10 = grass_block(7, 3)
grass_block11 = grass_block(9, 3)
grass_block12 = grass_block(11, 3)
grass_block13 = grass_block(5, 1)
grass_block14 = grass_block(7, 1)
grass_block15 = grass_block(9, 1)
grass_block16 = grass_block(11, 1)
grass_block17 = grass_block(4, 2)
grass_block18 = grass_block(8, 2)
grass_block19 = grass_block(6, 4)
grass_block20 = grass_block(1, 5)
grass_block21 = grass_block(5, 5)
grass_block22 = grass_block(7, 5)
grass_block23 = grass_block(11, 5)
grass_block24 = grass_block(7, 7)
grass_block25 = grass_block(1, 9)
grass_block26 = grass_block(3, 9)
grass_block27 = grass_block(5, 9)
grass_block28 = grass_block(7, 9)
grass_block29 = grass_block(9, 9)
grass_block30 = grass_block(11, 9)
grass_block31 = grass_block(2, 10)
grass_block32 = grass_block(6, 10)
grass_block33 = grass_block(10, 10)

# 手动录入的所有高山方块
mountain_block1 = mountain_block(2, 0)
mountain_block2 = mountain_block(8, 0)
mountain_block3 = mountain_block(12, 0)
mountain_block4 = mountain_block(13, 1)
mountain_block5 = mountain_block(14, 2)
mountain_block6 = mountain_block(16, 4)
mountain_block7 = mountain_block(15, 5)
mountain_block8 = mountain_block(13, 3)
mountain_block9 = mountain_block(-1, 3)
mountain_block10 = mountain_block(-3, 3)
mountain_block11 = mountain_block(8, 6)
mountain_block12 = mountain_block(9, 7)
mountain_block13 = mountain_block(10, 8)
mountain_block14 = mountain_block(11, 7)

# 手动录入的所有森林方块
dense_forest_block1 = dense_forest_block(1, 1)
dense_forest_block2 = dense_forest_block(-2, 2)
dense_forest_block3 = dense_forest_block(-2, 4)
dense_forest_block4 = dense_forest_block(-1, 5)
dense_forest_block5 = dense_forest_block(0, 6)
dense_forest_block6 = dense_forest_block(1, 7)
dense_forest_block7 = dense_forest_block(2, 8)
dense_forest_block8 = dense_forest_block(3, 7)
dense_forest_block9 = dense_forest_block(0, 8)
dense_forest_block10 = dense_forest_block(-3, 5)
dense_forest_block11 = dense_forest_block(6, 8)
dense_forest_block12 = dense_forest_block(8, 8)
dense_forest_block13 = dense_forest_block(6, 0)
dense_forest_block14 = dense_forest_block(10, 0)

# 手动录入的所有雪地方块
snow_block1 = snow_block(12, 2)
snow_block2 = snow_block(15, 3)
snow_block3 = snow_block(12, 4)
snow_block4 = snow_block(13, 5)
snow_block5 = snow_block(14, 6)
snow_block6 = snow_block(13, 7)

# 手动录入的所有水方块
water_block1 = shallow_water_block(3, 1)
water_block2 = shallow_water_block(4, 0)
water_block3 = shallow_water_block(5, 7)
water_block4 = shallow_water_block(4, 8)
water_block5 = shallow_water_block(10, 4)
water_block6 = shallow_water_block(9, 5)
water_block7 = shallow_water_block(12, 6)

# 手动录入的所有城镇方块
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

# 将所有地图块放入列表
grass_block_list = [
    grass_block1,
    grass_block2,
    grass_block3,
    grass_block4,
    grass_block5,
    grass_block6,
    grass_block7,
    grass_block8,
    grass_block9,
    grass_block10,
    grass_block11,
    grass_block12,
    grass_block13,
    grass_block14,
    grass_block15,
    grass_block16,
    grass_block17,
    grass_block18,
    grass_block19,
    grass_block20,
    grass_block21,
    grass_block22,
    grass_block23,
    grass_block24,
    grass_block25,
    grass_block26,
    grass_block27,
    grass_block28,
    grass_block29,
    grass_block30,
    grass_block31,
    grass_block32,
    grass_block33,
]

mountain_block_list = [
    mountain_block1,
    mountain_block2,
    mountain_block3,
    mountain_block4,
    mountain_block5,
    mountain_block6,
    mountain_block7,
    mountain_block8,
    mountain_block9,
    mountain_block10,
    mountain_block11,
    mountain_block12,
    mountain_block13,
    mountain_block14,
]

dense_forest_block_list = [
    dense_forest_block1,
    dense_forest_block2,
    dense_forest_block3,
    dense_forest_block4,
    dense_forest_block5,
    dense_forest_block6,
    dense_forest_block7,
    dense_forest_block8,
    dense_forest_block9,
    dense_forest_block10,
    dense_forest_block11,
    dense_forest_block12,
    dense_forest_block13,
    dense_forest_block14,
]

snow_block_list = [
    snow_block1,
    snow_block2,
    snow_block3,
    snow_block4,
    snow_block5,
    snow_block6,
]

water_block_list = [
    water_block1,
    water_block2,
    water_block3,
    water_block4,
    water_block5,
    water_block6,
    water_block7,
]

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


class MyGame(arcade.Window):
    """Our custom Window Class"""

    def __init__(self):
        """Initializer"""
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player_sprite = None
        self.player_list = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_list.extend(grass_block_list)
        self.player_list.extend(mountain_block_list)
        self.player_list.extend(dense_forest_block_list)
        self.player_list.extend(snow_block_list)
        self.player_list.extend(water_block_list)
        self.player_list.extend(town_block_list)

        self.player_list.sort(key=lambda x: x.center_y, reverse=True)

    def on_draw(self):
        """Draw everything"""
        self.clear()
        self.player_list.draw(pixelated=True)


window = MyGame()
window.setup()
arcade.run()
