"""2024.4.24更新，考虑把卡牌出去的效果做到点击里面"""

import arcade
from arcade import load_texture
from pyglet.math import Vec2
from enum import Enum
from card import Card, MagicAttackCard

from arcade import easing

SCREEN_TITLE = "Test Card Sprite"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650


class CardState(Enum):
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
            path_or_texture="resources/card_library/playable/actions/物理攻击.png",
            hit_box_algorithm="None",
        )

        self.timer = 0
        self.frame_time = 0.1

        self.scale = 0.15

        self.getting_bigger = False

    # def update_animation(self, delta_time: float = 1 / 60):
    #     if self.getting_bigger:
    #         ex, ey = easing.ease_position(
    #             self.position,
    #             (self.center_x, self.center_y + 30),
    #             rate=180,
    #             ease_function=easing.smoothstep,
    #         )


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.AMAZON
        self.card_list = None
        self.card_camera = None

        self.hand_card_anchor_left = None
        self.hand_card_anchor_right = None

        self.anchor_list = None

    def setup(self):
        self.card_list = arcade.SpriteList()
        self.card_list.append(CardSprite())

        self.card_camera = arcade.SimpleCamera()
        # 手牌的坐标按照左右锚点决定
        # 所以现在先不移动卡牌的相机
        # self.card_camera.move((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 4))

        # 手牌的左右锚点
        self.hand_card_anchor_left = Vec2(SCREEN_WIDTH / 7, SCREEN_HEIGHT / 8)
        self.hand_card_anchor_right = Vec2(SCREEN_WIDTH / 7 * 6, SCREEN_HEIGHT / 8)

        self.anchor_list = arcade.shape_list.ShapeElementList()

        self.card_list.append(CardSprite())
        self.card_list.append(CardSprite())
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

    def on_draw(self, blend_function=None):
        self.clear()
        self.card_camera.use()
        self.card_list.draw(pixelated=False)
        self.anchor_list.draw()

    def on_update(self, delta_time):

        for card in self.card_list:
            card.update_animation()

        for card, anchor in zip(self.card_list, self.anchor_list):

            card.center_x = anchor.points[0][0]
            card.center_y = anchor.points[0][1]

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        camera_cords = self.card_camera.get_map_coordinates((x, y))
        cards = arcade.get_sprites_at_point((camera_cords), self.card_list)
        if cards:
            cards[0].getting_bigger = True
            print(f"{cards[0].scale:.2f} at {cards[0].position}")
        else:
            for card in self.card_list:
                card.getting_bigger = False
            print(f"{self.card_list[0].position}")


window = MyGame()
window.setup()
arcade.run()
