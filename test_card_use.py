"""这个文件将前期工作组合起来，实现在地图上打出一张攻击牌的效果
具体需要实现的包括：从player_data到player_action到player到player_sprite的创建
地图的创建
完善卡牌的打出逻辑，把card的逻辑和card_sprite的逻辑分开
card负责生效，card_sprite负责处理在手中、打出、打出后的逻辑
现在还不用管game、轮次相关的逻辑，先把牌打出来一张再说

2024年5月13日，正式将卡牌做进来，开始打牌"""

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

from arcade import easing
from card import PhysicalAttackCard

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

# 卡牌相关全局变量
ORIGIN_CARD_SCALE = 0.15
OUT_CARD_SCALE = 0.20
EASING_GETOUT_ANIMATION_TIME = 0.45
EASING_GETIN_ANIMATION_TIME = 0.25

DEFAULT_DRAW_PILE_POSITION_X = 100
DEFAULT_DRAW_PILE_POSITION_Y = SCREEN_HEIGHT / 12 * 7


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


class CardSprite(arcade.Sprite):
    def __init__(self):
        super().__init__(
            hit_box_algorithm="None",
        )

        # 卡牌缩放
        self.scale = ORIGIN_CARD_SCALE

        # 缓动数据
        self.easing_angle_data = None
        self.easing_x_data = None
        self.easing_y_data = None
        self.easing_scale_data = None

        # 当卡牌被点击时，此属性为True，卡牌将展示绿色碰撞框
        self.is_held = False

        # 当鼠标在卡牌上时，此属性为True，卡牌将展示黄色碰撞框
        self.is_on_mouse = False

        # 以下属性和方法参考solitary
        self.is_face_up = False
        self.face_down_texture = load_texture(
            Path(r"resources\card_library\playable\摸牌堆.png")
        )
        self.face_up_texture = load_texture(
            Path(r"resources\card_library\playable\actions\物理攻击.png")
        )
        self.texture = self.face_down_texture

        self.timer = 0
        self.time_in_card_pile = 0
        self.card = PhysicalAttackCard()

    def face_up(self):
        self.is_face_up = True
        self.texture = self.face_up_texture

    def face_down(self):
        self.is_face_up = False
        self.texture = self.face_down_texture

    @property
    def is_face_down(self):
        return not self.is_face_up

    def on_update(self, delta_time: float = 1 / 60):
        # 卡牌在抽牌堆中的时间
        # 如果计时器小于卡牌在抽牌堆中的时间，不更新
        self.timer += delta_time
        if self.timer < self.time_in_card_pile:
            return
        self.timer = 0
        self.time_in_card_pile = 0
        if self.easing_angle_data is not None:
            done, self.angle = easing.ease_angle_update(
                self.easing_angle_data, delta_time
            )
            if done:
                self.easing_angle_data = None

        if self.easing_x_data is not None:
            done, self.center_x = easing.ease_update(self.easing_x_data, delta_time)
            if done:
                self.easing_x_data = None

        if self.easing_y_data is not None:
            done, self.center_y = easing.ease_update(self.easing_y_data, delta_time)
            if done:
                self.easing_y_data = None

        if self.easing_scale_data is not None:
            done, self.scale = easing.ease_update(self.easing_scale_data, delta_time)
            if done:
                self.easing_scale_data = None


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

        self.active_player = None

        # 卡牌相关
        self.card_list = None
        self.card_camera = None

        self.hand_card_anchor_left = None
        self.hand_card_anchor_right = None

        self.anchor_list = None

        self.draw_card_pile = None

        self.on_held_card = None

    def setup(self):
        self.camera_map = arcade.SimpleCamera()
        self.camera_map.position.x = -SCREEN_WIDTH / 2
        self.camera_map.position.y = -SCREEN_HEIGHT / 2

        # 玩家列表
        self.player_list = arcade.SpriteList()
        self.player_list.append(maud_pie_sprite)
        self.player_list.append(sun_burst_sprite)
        self.player_list.append(derpy_sprite)

        # 灰琪负责打牌
        self.active_player = maud_pie_sprite

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
            color=arcade.color.WHITE,
            multiline=True,
            width=200,
        )

        # 以上为地图相关的初始化

        # 下面是卡牌相关的初始化
        self.card_list = arcade.SpriteList()

        # 卡牌抽牌堆
        self.draw_card_pile = arcade.SpriteList()

        # 给抽牌堆生成12张卡牌
        for i in range(12):
            card = CardSprite()
            card.center_x = DEFAULT_DRAW_PILE_POSITION_X
            card.center_y = DEFAULT_DRAW_PILE_POSITION_Y
            self.draw_card_pile.append(card)

        self.card_camera = arcade.SimpleCamera()
        # 手牌的坐标按照左右锚点决定
        # 所以现在先不移动卡牌的相机
        # self.card_camera.move((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 4))

        # 手牌的左右锚点
        self.hand_card_anchor_left = Vec2(SCREEN_WIDTH / 7, SCREEN_HEIGHT / 8)
        self.hand_card_anchor_right = Vec2(SCREEN_WIDTH / 7 * 6, SCREEN_HEIGHT / 8)

        self.anchor_list = arcade.shape_list.ShapeElementList()

        # 生成手里的卡牌
        for i in range(4):
            card = CardSprite()
            card.face_up()
            self.card_list.append(card)

        self.anchor_update()

    def card_ease_update(self):
        # 所有没有被拿住的卡牌回到锚点，被拿住的卡牌向上移动
        for card, anchor in zip(self.card_list, self.anchor_list):
            # 如果卡牌没有被拿住，卡牌回到锚点
            if not card.is_held:
                ex, ey = easing.ease_position(
                    card.position,
                    anchor.points[0],
                    time=EASING_GETIN_ANIMATION_TIME,
                    # rate=0.2,
                    ease_function=easing.ease_out,
                )
                card.easing_x_data = ex
                card.easing_y_data = ey

                escale = easing.ease_value(
                    card.scale,
                    ORIGIN_CARD_SCALE,
                    time=EASING_GETIN_ANIMATION_TIME,
                    # rate=0.2,
                    ease_function=easing.ease_out,
                )
                card.easing_scale_data = escale

            # 如果卡牌被拿住，卡牌向上移动
            elif card.is_held:
                ex, ey = easing.ease_position(
                    card.position,
                    (card.center_x, card.center_y + 100),
                    time=EASING_GETOUT_ANIMATION_TIME,
                    # rate=180,
                    ease_function=easing.ease_out,
                )
                card.easing_x_data = ex
                card.easing_y_data = ey

                escale = easing.ease_value(
                    card.scale,
                    OUT_CARD_SCALE,
                    time=EASING_GETOUT_ANIMATION_TIME,
                    # rate=0.2,
                    ease_function=easing.ease_out,
                )
                card.easing_scale_data = escale

    def anchor_update(self):
        # 计算手牌的锚点
        # 先获取手牌数，手牌间隔 =（右锚点-左锚点）/(手牌数+1)
        # 手牌的锚点 = 左锚点+（手牌间隔*卡牌数）
        card_num = len(self.card_list)
        card_spacing = (
            self.hand_card_anchor_right.x - self.hand_card_anchor_left.x
        ) / (card_num + 1)
        card_center_x = [
            self.hand_card_anchor_left.x + card_spacing * (i + 1)
            for i in range(card_num)
        ]
        self.anchor_list.clear()
        for i in card_center_x:

            self.anchor_list.append(
                arcade.shape_list.create_ellipse_filled(
                    i, self.hand_card_anchor_right.y, 10, 10, arcade.color.YELLOW
                )
            )

        for card, anchor in zip(self.card_list, self.anchor_list):
            card.center_x = anchor.points[0][0]
            card.center_y = anchor.points[0][1]

        self.anchor_list.append(
            arcade.shape_list.create_ellipse_filled(
                self.hand_card_anchor_left.x,
                self.hand_card_anchor_left.y,
                10,
                10,
                arcade.color.BLUE,
            )
        )
        self.anchor_list.append(
            arcade.shape_list.create_ellipse_filled(
                self.hand_card_anchor_right.x,
                self.hand_card_anchor_right.y,
                10,
                10,
                arcade.color.RED,
            )
        )

    def card_ease_update(self):
        # 所有没有被拿住的卡牌回到锚点，被拿住的卡牌向上移动
        for card, anchor in zip(self.card_list, self.anchor_list):
            # 如果卡牌没有被拿住，卡牌回到锚点
            if not card.is_held:
                ex, ey = easing.ease_position(
                    card.position,
                    anchor.points[0],
                    time=EASING_GETIN_ANIMATION_TIME,
                    # rate=0.2,
                    ease_function=easing.ease_out,
                )
                card.easing_x_data = ex
                card.easing_y_data = ey

                escale = easing.ease_value(
                    card.scale,
                    ORIGIN_CARD_SCALE,
                    time=EASING_GETIN_ANIMATION_TIME,
                    # rate=0.2,
                    ease_function=easing.ease_out,
                )
                card.easing_scale_data = escale

            # 如果卡牌被拿住，卡牌向上移动
            elif card.is_held:
                ex, ey = easing.ease_position(
                    card.position,
                    (card.center_x, card.center_y + 100),
                    time=EASING_GETOUT_ANIMATION_TIME,
                    # rate=180,
                    ease_function=easing.ease_out,
                )
                card.easing_x_data = ex
                card.easing_y_data = ey

                escale = easing.ease_value(
                    card.scale,
                    OUT_CARD_SCALE,
                    time=EASING_GETOUT_ANIMATION_TIME,
                    # rate=0.2,
                    ease_function=easing.ease_out,
                )
                card.easing_scale_data = escale

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
                # 点击到灰琪时，走移动逻辑
                if players[-1] is self.active_player:
                    self.held_player = players[-1]
                    self.held_player_original_hex_position = (
                        self.held_player.hex_position
                    )
                # 点击到其他玩家时，出牌
                elif players[-1] is not self.active_player:
                    if self.on_held_card:
                        print("点击到其他玩家，出牌")
                        if self.on_held_card:

                            # 卡牌生效
                            self.on_held_card.card.effect(
                                self.active_player.player, players[-1].player
                            )

                            # 卡牌生效后，从手牌中移除
                            self.on_held_card.is_held = False
                            self.card_list.remove(self.on_held_card)
                            self.on_held_card = None
                            self.anchor_update()

                            # 如果目标生命值小于0，从玩家列表中移除
                            if players[-1].player.data.health <= 0:
                                self.player_list.remove(players[-1])

            # 卡牌逻辑
            camera_cords = self.card_camera.get_map_coordinates((x, y))
            cards = arcade.get_sprites_at_point((camera_cords), self.card_list)
            if cards:
                self.on_held_card = cards[-1]
                self.on_held_card.is_held = True

                print(f"点击了{cards[0].position}")
            elif not cards:
                self.on_held_card = None
            for card in self.card_list:
                if card is not self.on_held_card:
                    card.is_held = False

            # 抽牌堆逻辑
            draw_pile = arcade.get_sprites_at_point((camera_cords), self.draw_card_pile)
            if draw_pile:
                card = self.draw_card_pile[-1]
                self.draw_card_pile.remove(card)
                card.face_up()
                self.card_list.append(card)
                self.anchor_update()

        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.on_held_card = None
            for card in self.card_list:
                card.is_held = False

        # 先更新卡牌动画，后更新锚点
        self.card_ease_update()
        self.anchor_update()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        map_cords = self.camera_map.get_map_coordinates((x, y))
        blocks = arcade.get_sprites_at_point((map_cords), self.block_list)

        # 文字显示的逻辑
        players = arcade.get_sprites_at_point((map_cords), self.player_list)

        if players:
            player_sprite = players[-1]
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
            self.held_block = blocks[-1]
        else:
            self.held_block = None

        # 抓取玩家，移动玩家的逻辑
        if self.held_player:
            self.held_player.center_x += dx
            self.held_player.center_y += dy

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.held_player:
                map_cords = self.camera_map.get_map_coordinates((x, y))
                blocks = arcade.get_sprites_at_point((map_cords), self.block_list)
                if blocks:
                    block = blocks[-1]
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
        self.card_list.on_update(delta_time)
        self.draw_card_pile.on_update(delta_time)

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
        self.card_camera.use()
        self.draw_card_pile.draw()
        self.card_list.draw(pixelated=False)
        for card in self.card_list:
            if card.is_on_mouse:
                card.draw_hit_box(color=arcade.color.YELLOW)
            elif card.is_held:
                card.draw_hit_box(color=arcade.color.GREEN)
            else:
                card.draw_hit_box(color=arcade.color.RED)
        self.anchor_list.draw()


window = MyGame()
window.setup()
arcade.run()
