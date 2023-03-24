from PIL import Image


def make_desired(template, color):
    return None


def change_color(photo, requested_color):
    image_color = photo.convert('RGBA')
    image_grey = photo.convert('LA')

    for x in range(image_color.width):
        for y in range(image_color.height):
            if image_color.getpixel((x, y))[-1] != 0:
                image_color.putpixel((x, y), requested_color)

    for x in range(image_grey.width):
        for y in range(image_grey.height):
            color = image_grey.getpixel((x, y))
            if color[-1] != 0:
                image_grey.putpixel((x, y), (color[0], abs(color[0] - 128) * 2))

    return Image.alpha_composite(image_color, image_grey.convert('RGBA'))
