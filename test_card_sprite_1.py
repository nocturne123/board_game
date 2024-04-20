import arcade
from arcade import load_texture
from pyglet.math import Vec2
from enum import Enum

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
    def __init__(self, card):
        super().__init__(
            path_or_texture="resources/card_library/playable/actions/物理攻击.png",
            hit_box_algorithm="None",
        )

        self.timer = 0
        self.frame_time = 0.1

        self.scale = 0.15

        self.getting_bigger = False

    def update_animation(self, delta_time: float = 1 / 60):
        if self.getting_bigger:
            if self.scale <= 0.35:
                self.scale += 0.01
                self.forward(5)

        else:
            if self.scale >= 0.15:
                self.scale -= 0.03
                if self.center_y > 0:
                    self.center_y -= 5
                else:
                    self.center_y = 0

    def lerp_y(self, y, speed):
        return self.y + (speed * (y - self.y))

    def move_to_y(self, y: float, speed):
        self.center_y = self.lerp_y(y, speed)
        if self.center_y == y:
            return True


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.AMAZON
        self.card_list = None
        self.card_camera = arcade.SimpleCamera()
        self.card_camera.move((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 4))

    def setup(self):
        self.card_list = arcade.SpriteList()
        self.card_list.append(CardSprite())

    def on_draw(self, blend_function=None):
        self.clear()
        self.card_camera.use()
        self.card_list.draw(pixelated=False)

    def on_update(self, delta_time):
        for card in self.card_list:
            card.update_animation()

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
