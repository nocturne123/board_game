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
OUT_CARD_SCALE = 0.27
EASING_GETOUT_ANIMATION_TIME = 0.45
EASING_GETIN_ANIMATION_TIME = 0.25


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

    def setup(self):
        self.card_list = arcade.SpriteList()
        self.card_list.append(CardSprite())

        self.draw_card_pile = arcade.SpriteList()

        self.card_camera = arcade.SimpleCamera()
        # 手牌的坐标按照左右锚点决定
        # 所以现在先不移动卡牌的相机
        # self.card_camera.move((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 4))

        # 手牌的左右锚点
        self.hand_card_anchor_left = Vec2(SCREEN_WIDTH / 7, SCREEN_HEIGHT / 8)
        self.hand_card_anchor_right = Vec2(SCREEN_WIDTH / 7 * 6, SCREEN_HEIGHT / 8)

        self.anchor_list = arcade.shape_list.ShapeElementList()

        for i in range(8):
            self.card_list.append(CardSprite())

        # 根据前面的卡牌数，这里有4张牌

        for i in self.card_list:
            print(i.position)

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

    # 左键点击卡牌时，卡牌向上移动
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            camera_cords = self.card_camera.get_map_coordinates((x, y))
            cards = arcade.get_sprites_at_point((camera_cords), self.card_list)
            if cards:
                card = cards[-1]

                print(f"点击了{cards[0].position}")
                # 点击卡牌，卡牌向上移动
                if not card.is_held:

                    # 向上移动
                    ex, ey = easing.ease_position(
                        card.position,
                        (card.center_x, card.center_y + 100),
                        time=EASING_GETOUT_ANIMATION_TIME,
                        # rate=180,
                        ease_function=easing.ease_out,
                    )
                    card.easing_x_data = ex
                    card.easing_y_data = ey

                    # 放大
                    escale = easing.ease_value(
                        card.scale,
                        OUT_CARD_SCALE,
                        time=EASING_GETOUT_ANIMATION_TIME,
                        # 这里的rate需要谨慎处理
                        # rate=0.2,
                        ease_function=easing.ease_out,
                    )
                    card.easing_scale_data = escale
                card.is_held = True

        # 点击鼠标右键时，所有卡牌回到锚点
        if button == arcade.MOUSE_BUTTON_RIGHT:
            for card, anchor in zip(self.card_list, self.anchor_list):
                card.is_held = False
                ex, ey = easing.ease_position(
                    card.position,
                    anchor.points[0],
                    time=EASING_GETIN_ANIMATION_TIME,
                    # rate=180,
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

    # 老式的移动卡牌放大写不出来，修改为点击卡牌，卡牌向上移动
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        camera_cords = self.card_camera.get_map_coordinates((x, y))
        cards = arcade.get_sprites_at_point((camera_cords), self.card_list)
        if cards:
            card = cards[-1]
            for _ in self.card_list:
                _.is_on_mouse = False
            card.is_on_mouse = True
        else:
            for _ in self.card_list:
                _.is_on_mouse = False


window = MyGame()
window.setup()
arcade.run()
