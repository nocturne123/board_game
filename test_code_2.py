from itertools import cycle


animation_sequance = [1, 0, 1, 2]
cur_texture = cycle(animation_sequance).__next__()

print(cur_texture)
print(cur_texture)
print(cur_texture)
