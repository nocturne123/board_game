from PIL import Image


def remove_non_transparent_pixels(image_path):
    # Open the image
    image = Image.open(image_path)

    # Get the pixel data
    pixels = image.load()

    # Find the leftmost transparent pixel
    leftmost_transparent_pixel = None
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y][3] == 0:  # Check if the pixel is transparent
                leftmost_transparent_pixel = (x, y)
                break
        if leftmost_transparent_pixel is not None:
            break

    # Remove everything except the island of the leftmost transparent pixel
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y][3] != 0 and (x, y) != leftmost_transparent_pixel:
                pixels[x, y] = (0, 0, 0, 0)  # Set the pixel to transparent

    # Save the modified image
    image.save("output.png")


# Usage example
remove_non_transparent_pixels("derpy.png")
