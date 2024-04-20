"""使用hexlogic库的Hex类，定义地图图块
2024.3.29更新，为了适配arcade3.0.0dev25的写法，先把图片读到texture里面
再从texture里面生成sprite，实现地图"""

from ENUMS.common_enums import BlockTypeEnum

# from hexutil import Hex
from hexlogic import HexCoords, hex_to_pixel
import arcade


TILE_SCALING = 2
TILE_WIDTH = 28
TILE_HEIGHT = -24

image_x_list = range(0, 225, 32)
image_y_list = range(0, 241, 48)

Map_Textures = arcade.load_textures(
    file_name="resources/images/fantasyhextiles_v3.png",
    image_location_list=[(x, y, 32, 48) for y in image_y_list for x in image_x_list],
)

texture_0 = Map_Textures[0]
texture_1 = Map_Textures[7]


class map_block(arcade.Sprite):
    def __init__(
        self,
        map_texture=None,
        block_type: BlockTypeEnum = BlockTypeEnum.grass,
        hit_box_algorithm="None",
        hex_q=0,
        hex_r=0,
        hex_s=0,
    ):
        super().__init__(
            path_or_texture=map_texture,
            scale=TILE_SCALING,
            center_x=hex_to_pixel(
                HexCoords(hex_q, hex_r, hex_s),
                tile_width=TILE_SCALING * TILE_WIDTH,
                tile_height=TILE_SCALING * TILE_HEIGHT,
            )[0],
            center_y=hex_to_pixel(
                HexCoords(hex_q, hex_r, hex_s),
                tile_width=TILE_SCALING * TILE_WIDTH,
                tile_height=TILE_SCALING * TILE_HEIGHT,
            )[1],
        )
        # 这里横纵坐标里面的300是为了让地图居中显示，后面熟悉Camera之后使用camera将地图居中，这里就不需要再加300了
        self.hex_position = HexCoords(hex_q, hex_r, hex_s)
        self.block_type: BlockTypeEnum = block_type


# 下面是具体的地图图块定义，除了具体城镇，其他图块不用传入block_type参数
class grass_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[0],
            block_type=BlockTypeEnum.grass,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class little_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[1],
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class dense_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[2],
            block_type=BlockTypeEnum.dense_forest,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class rock_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[3],
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class spruce_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[4],
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class mountain_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[5],
            block_type=BlockTypeEnum.mountain,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class shallow_water_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[6],
            block_type=BlockTypeEnum.water,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class deep_water_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[7],
            block_type=BlockTypeEnum.water,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class town_block_no_fence(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[8],
            block_type=block_type,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class town_block_with_fence(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[9],
            block_type=block_type,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class town_block_high_fence(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[10],
            block_type=block_type,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[16],
            block_type=BlockTypeEnum.snow,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_little_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[17],
            block_type=BlockTypeEnum.snow,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_dense_forest_block(map_block):
    def __init__(self, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[18],
            block_type=BlockTypeEnum.snow,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_town_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[22],
            block_type=block_type,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class snow_castle_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[23],
            block_type=block_type,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class our_town_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[40],
            block_type=block_type,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


class tree_of_harmony_block(map_block):
    def __init__(self, block_type, hex_q, hex_r, hex_s):
        super().__init__(
            map_texture=Map_Textures[12],
            block_type=block_type,
            hex_q=hex_q,
            hex_r=hex_r,
            hex_s=hex_s,
        )


if __name__ == "__main__":
    # 测试代码
    print("测试代码")
    print("grass_block")

    block1 = map_block(texture_0)
    block2 = map_block(texture_1, hex_q=0, hex_r=1, hex_s=-1)

    class MyGame(arcade.Window):

        def __init__(self):
            """Initializer"""
            # Call the parent class initializer
            super().__init__(1200, 800)
            self.player_sprite = None
            self.block_list = None
            self.camera_map = arcade.SimpleCamera()

            self.left_pressed = False
            self.right_pressed = False
            self.up_pressed = False
            self.down_pressed = False

        def setup(self):
            self.block_list = arcade.SpriteList()
            self.block_list.append(block1)
            self.block_list.append(block2)

            self.block_list.sort(key=lambda x: x.hex_position.r, reverse=True)
            self.block_list.sort(key=lambda x: x.hex_position.s, reverse=False)
            self.view_left = 0
            self.view_bottom = 0

        def on_draw(self):
            """Draw everything"""
            self.clear()
            self.camera_map.use()
            self.block_list.draw(pixelated=True)

    window = MyGame()
    window.setup()
    arcade.run()
