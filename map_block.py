"""使用hexlogic库的Hex类，定义地图图块"""

from ENUMS.common_enums import BlockTypeEnum

# from hexutil import Hex
from hexlogic import HexCoords, hex_to_pixel
import arcade

TILE_SCALING = 1

"""
def hex_to_pixel(hex: HexCoords) -> tuple:
    Converts a hex coordinate to a pixel coordinate
    #将六边形坐标转换为像素坐标
    
    hex_x = hex[0]
    hex_y = hex[1]
    return (hex_y * -24, hex_x * 13)
"""


class map_block(arcade.Sprite):
    def __init__(
        self,
        block_type: BlockTypeEnum = BlockTypeEnum.grass,
        image_x=0,
        image_y=0,
        hex_q=0,
        hex_r=0,
        hex_s=0,
    ):
        super().__init__(
            filename="resources/images/fantasyhextiles_v3.png",
            image_width=32,
            image_height=48,
            scale=TILE_SCALING,
            image_x=image_x,
            image_y=image_y,
            center_x=300
            + hex_to_pixel(
                HexCoords(hex_q, hex_r, hex_s), tile_width=26, tile_height=24
            )[0],
            center_y=300
            + hex_to_pixel(
                HexCoords(hex_q, hex_r, hex_s), tile_width=26, tile_height=24
            )[1],
        )
        self.hex_position = HexCoords(hex_q, hex_r, hex_s)
        self.type: BlockTypeEnum = block_type


# 下面是具体的地图图块定义，除了具体城镇，其他图块不用传入block_type参数
class grass_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.grass,
            image_x=0,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class little_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            image_x=32,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class dense_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.dense_forest,
            image_x=64,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class rock_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            image_x=96,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class spruce_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            image_x=128,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class mountain_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.mountain,
            image_x=160,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class shallow_water_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.water,
            image_x=192,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class deep_water_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.water,
            image_x=224,
            image_y=0,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class town_block_no_fence(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=block_type,
            image_x=0,
            image_y=48,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class town_block_with_fence(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=block_type,
            image_x=32,
            image_y=48,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class town_block_high_fence(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=block_type,
            image_x=64,
            image_y=48,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.snow,
            image_x=0,
            image_y=96,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_little_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.snow,
            image_x=32,
            image_y=96,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_dense_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=BlockTypeEnum.snow,
            image_x=64,
            image_y=96,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_town_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=block_type,
            image_x=192,
            image_y=96,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_castle_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=block_type,
            image_x=224,
            image_y=96,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class our_town_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=block_type,
            image_x=0,
            image_y=240,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class tree_of_harmony_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            block_type=block_type,
            image_x=128,
            image_y=48,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )
