import toml

grass_hex_list = [
    [-4, 4],
    [-5, 3],
    [-4, 2],
    [-3, 1],
    [-2, 0],
    [1, 3],
    [3, 3],
    [5, 3],
    [7, 3],
    [0, 2],
    [4, 2],
    [-1, 1],
    [1, 1],
    [3, 1],
    [5, 1],
    [7, 1],
    [-3, -1],
    [-1, -1],
    [1, -1],
    [3, -1],
    [7, -1],
    [2, 0],
    [0, -2],
    [3, -3],
    [-3, -5],
    [-1, -5],
    [1, -5],
    [3, -5],
    [5, -5],
    [7, -5],
    [-2, -6],
    [2, -6],
    [6, -6],
]


mountain_hex_list = [
    [-2, 4],
    [4, 4],
    [8, 4],
    [9, 3],
    [10, 2],
    [9, 1],
    [4, -2],
    [12, 0],
    [11, -1],
    [7, -3],
    [5, -3],
    [6, -4],
    [-5, 1],
    [-7, 1],
]


dense_forest_hex_list = [
    [6, 4],
    [2, 4],
    [-3, 3],
    [-6, 2],
    [-6, 0],
    [-5, -1],
    [-7, -1],
    [-4, -2],
    [-3, -3],
    [-1, -3],
    [4, -4],
    [2, -4],
    [-2, -4],
    [-4, -4],
]

snow_hex_list = [[8, 2], [11, 1], [8, 0], [9, -1], [10, -2], [9, -3]]

water_hex_list = [[0, 4], [6, 0], [8, -2], [-1, -3], [0, -4], [5, -1]]

"""
# 手动录入的所有城镇方块
town_block1 = snow_castle_block(BlockTypeEnum.crystal_empire, 10, 0)
town_block2 = our_town_block(BlockTypeEnum.our_town, 8, -4)
town_block3 = town_block_no_fence(BlockTypeEnum.cloudsdale, 6, 2)
town_block4 = town_block_high_fence(BlockTypeEnum.canterlot, 6, -2)
town_block5 = town_block_with_fence(BlockTypeEnum.castle_of_friendship, 4, 0)
town_block6 = town_block_no_fence(BlockTypeEnum.manehattan, 4, -6)
town_block7 = town_block_no_fence(BlockTypeEnum.sweet_apple_acres, 2, 2)
town_block8 = town_block_no_fence(BlockTypeEnum.rainbow_dash_house, 2, -2)
town_block9 = town_block_no_fence(BlockTypeEnum.town_hall, 0, 0)
town_block10 = town_block_with_fence(BlockTypeEnum.baltimare, 0, -6)
town_block11 = town_block_no_fence(BlockTypeEnum.sugar_cube_corner, -2, 2)
town_block12 = town_block_no_fence(BlockTypeEnum.carousel_boutique, -4, 0)
town_block13 = town_block_no_fence(BlockTypeEnum.fluttershy_house, -2, -2)
town_block14 = town_block_no_fence(BlockTypeEnum.zecora_house, -8, 0)
town_block15 = snow_castle_block(BlockTypeEnum.old_castle, -6, -2)
town_block16 = tree_of_harmony_block(BlockTypeEnum.tree_of_harmony, -5, -3)
"""


town_hex_list = [
    (10, 0),
    (8, -4),
    (6, 2),
    (6, -2),
    (4, 0),
    (4, -6),
    (2, 2),
    (2, -2),
    (0, 0),
    (0, -6),
    (-2, 2),
    (-4, 0),
    (-2, -2),
    (-8, 0),
    (-6, -2),
    (-5, -3),
]

a = [1, 2, 3, 4, 5, 6]
dst_file = "map.toml"
with open(dst_file, "w") as f:
    r3 = toml.dump(a)
