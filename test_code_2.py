image_x_list = range(0, 225, 32)
image_y_list = range(0, 241, 48)
image_location_list = [(x, y, 32, 48) for y in image_y_list for x in image_x_list]
for x in image_location_list:
    print(x)
print(image_y_list)
