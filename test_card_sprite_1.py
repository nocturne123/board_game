import arcade
from arcade import load_texture

SCREEN_TITLE = "Test Card Sprite"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650


class CardSprite(arcade.Sprite):
    def __init__(self):
        super().__init__(
            path_or_texture="resources/card_library/playable/actions/attacks/physical/物理攻击.png",
            hit_box_algorithm="None",
        )

        self.timer = 0
        self.frame_time = 0.1

        self.scale = 0.15


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.card_list = None
        self.card_camera = arcade.SimpleCamera()
        self.card_camera.move((-SCREEN_WIDTH / 2, -SCREEN_HEIGHT / 4))

    def setup(self):
        self.card_list = arcade.SpriteList()
        self.card_list.append(CardSprite())

    def on_draw(self):
        self.clear()
        self.card_camera.use()
        self.card_list.draw()


window = MyGame()
window.setup()
arcade.run()
