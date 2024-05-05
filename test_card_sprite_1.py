"""2024.4.24更新，考虑把卡牌出去的效果做到点击里面"""

import arcade
from arcade import load_texture
from pyglet.math import Vec2
from enum import Enum
from card import Card, MagicAttackCard

from arcade import easing

from pathlib import Path

SCREEN_TITLE = "Test Card Sprite"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

ORIGIN_CARD_SCALE = 0.15
OUT_CARD_SCALE = 0.20
EASING_GETOUT_ANIMATION_TIME = 0.45
EASING_GETIN_ANIMATION_TIME = 0.25

# 控制抽牌堆位置
DEFAULT_DRAW_PILE_POSITION_X = 100
DEFAULT_DRAW_PILE_POSITION_Y = SCREEN_HEIGHT / 12 * 7

# 控制抽牌堆动画，等待时间比例
EASING_DRAW_CARD_PILE_ANIMATION_RATE = 0.25

# 控制抽牌堆动画时间,0.75秒完成一次完整抽牌动画
EASING_DRAW_CARD_PILE_ANIMATION_TIME = 0.75


class CardState(Enum):
    """此属性还未在CardSprite中使用，暂时保留"""

    in_deck = 0
    on_draw = 1
    in_hand = 2
    on_choose = 3
    back_to_hand = 4
    on_board = 5
    on_discard = 5


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


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.AMAZON
        self.card_list = None
        self.card_camera = None

        self.hand_card_anchor_left = None
        self.hand_card_anchor_right = None

        self.anchor_list = None

        self.draw_card_pile = None

        self.on_held_card = None

    def setup(self):
        #
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
        for i in card_center_x:

            self.anchor_list.append(
                arcade.shape_list.create_ellipse_filled(
                    i, self.hand_card_anchor_right.y, 10, 10, arcade.color.YELLOW
                )
            )

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

        for card, anchor in zip(self.card_list, self.anchor_list):
            card.center_x = anchor.points[0][0]
            card.center_y = anchor.points[0][1]

    def on_draw(self, blend_function=None):
        self.clear()
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

    def on_update(self, delta_time):
        self.card_list.on_update(delta_time)
        self.draw_card_pile.on_update(delta_time)

    # 左键点击卡牌时，卡牌向上移动
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:

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

            # 左键点击抽牌堆时，抽牌
            # 现在这部分的逻辑会很长，后续考虑封装到函数里
            draw_pile = arcade.get_sprites_at_point((camera_cords), self.draw_card_pile)
            if draw_pile:
                # 测试先抽一张，后续考虑连续抽多张牌的情况
                draw_num = 4
                # 第一步，卡牌从牌堆中飞出，缓动到屏幕下方
                # 注：此处卡牌飞到抽牌堆的正下方、屏幕外，不是相对于卡牌自身的下方
                # 时间分配为：卡牌飞出的时间为(1/draw_num开方)，卡牌等待的时间为(1-1/draw_num开方)
                # 如何实现卡牌等待？
                if draw_num == 1:
                    card = self.draw_card_pile[-1]
                    card.time_in_card_pile = 0
                    ex, ey = easing.ease_position(
                        card.position,
                        (DEFAULT_DRAW_PILE_POSITION_X, -SCREEN_HEIGHT / 7),
                        time=EASING_DRAW_CARD_PILE_ANIMATION_TIME,
                        ease_function=easing.ease_out,
                    )
                    card.easing_x_data = ex
                    card.easing_y_data = ey
                elif draw_num > 1:

                    card_fly_time = EASING_DRAW_CARD_PILE_ANIMATION_TIME * (
                        draw_num**0.5
                    )
                    card_wait_time = (
                        EASING_DRAW_CARD_PILE_ANIMATION_TIME - card_fly_time
                    )
                    out_card_list = []
                    for i in range(draw_num):
                        card = self.draw_card_pile[-i]
                        card.time_in_card_pile = (
                            card_wait_time * (i - 1) / (draw_num - 1)
                        )
                        ex, ey = easing.ease_position(
                            card.position,
                            (DEFAULT_DRAW_PILE_POSITION_X, -SCREEN_HEIGHT / 7),
                            time=card_fly_time,
                            ease_function=easing.ease_out,
                        )
                        card.easing_x_data = ex
                        card.easing_y_data = ey

        # 点击鼠标右键时，所有卡牌回到锚点
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.on_held_card = None
            for card in self.card_list:
                card.is_held = False

        # 先更新卡牌动画，后更新锚点
        self.card_ease_update()
        self.anchor_update()

    # # 老式的移动卡牌放大写不出来，修改为点击卡牌，卡牌向上移动
    # def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
    #     camera_cords = self.card_camera.get_map_coordinates((x, y))
    #     cards = arcade.get_sprites_at_point((camera_cords), self.card_list)
    #     if cards:
    #         card = cards[-1]
    #         for _ in self.card_list:
    #             _.is_on_mouse = False
    #         card.is_on_mouse = True
    #     else:
    #         for _ in self.card_list:
    #             _.is_on_mouse = False


window = MyGame()
window.setup()
arcade.run()
