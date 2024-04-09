from PIL import Image

# Open the image
image_path = "触发事件.png"
image = Image.open(image_path)

# Convert the image to RGBA mode if it's not already
if image.mode != "RGBA":
    image = image.convert("RGBA")

# Get the alpha channel
alpha_channel = image.split()[3]

# Show the alpha channel
alpha_channel.show()

# Open another image
other_image_path = "物理攻击.png"
other_image = Image.open(other_image_path)

# Convert the other image to RGBA mode if it's not already
if other_image.mode != "RGBA":
    other_image = other_image.convert("RGBA")

# Apply the alpha channel from the first image to the other image
other_image.putalpha(alpha_channel)

# Show the modified other image
other_image.show()
