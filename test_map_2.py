import pytiled_parser
import arcade
from pathlib import Path
from pprint import pprint

SCREEN_TITLE = "Test Map"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

TILE_SCALING = 1

map_path = Path("resources/tiled_maps/board_map.json")

map = pytiled_parser.parse_map(map_path)
# print(dir(map))
pprint(map)


block_sprite_grass = arcade.Sprite(
    filename="resources/images/fantasyhextiles_v3.png",
    scale=TILE_SCALING,
    image_x=0,
    image_y=0,
    image_width=32,
    image_height=48,
    center_x=300,
    center_y=300,
)

block_sprite_little_forest = arcade.Sprite(
    filename="resources/images/fantasyhextiles_v3.png",
    scale=TILE_SCALING,
    image_x=32,
    image_y=0,
    image_width=32,
    image_height=48,
    center_x=324,
    center_y=288,
)


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
        self.player_list.append(block_sprite_grass)
        self.player_list.append(block_sprite_little_forest)

    def on_draw(self):
        """Draw everything"""
        self.clear()
        self.player_list.draw(pixelated=True)


window = MyGame()
window.setup()
arcade.run()
