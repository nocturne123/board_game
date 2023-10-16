from ENUMS.common_enums import BlockTypeEnum
from hexutil import Hex
import arcade

TILE_SCALING = 1


def hex_to_pixel(hex: Hex) -> tuple:
    """Converts a hex coordinate to a pixel coordinate
    将六边形坐标转换为像素坐标
    """
    hex_x = hex[0]
    hex_y = hex[1]
    return (hex_y * -24, hex_x * 13)


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
