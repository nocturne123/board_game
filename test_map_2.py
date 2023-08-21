import pytiled_parser
import arcade
from pathlib import Path
from pprint import pprint

SCREEN_TITLE = "Test Map"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

TILE_SCALING = 3

map_path = Path("resources/tiled_maps/board_map.json")

map = pytiled_parser.parse_map(map_path)
# print(dir(map))
pprint(map.layers)
pprint(map.layers[0])
