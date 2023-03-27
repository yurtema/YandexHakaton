from PIL import Image


def recolor_hand(photo: str, rgb_base: tuple, rgb_dec: tuple):
    hand = Image.open(f'media/{photo}_hand.png').convert('RGBA')
    base = Image.open(f'media/{photo}_base.png').convert('RGBA')
    dec = Image.open(f'media/{photo}_dec.png').convert('RGBA')

    base = change_color(base, rgb_base)
    dec = change_color(dec, rgb_dec)

    hand.paste(base, (0, 0), base)
    hand.paste(dec, (0, 0), dec)
    print(f'saved media/temp/{photo[-1]}_{rgb_base}_{rgb_dec}.png')
    hand.save(f'media/temp/{photo[-1]}_{rgb_base}_{rgb_dec}.png')

    return f'media/temp/{photo[-1]}_{rgb_base}_{rgb_dec}.png'


def change_color(photo: Image, requested_color: tuple):
    image_color = photo.convert('RGBA')
    image_grey = photo.convert('LA')

    for x in range(image_color.width):
        for y in range(image_color.height):
            if image_color.getpixel((x, y))[-1] != 0:
                image_color.putpixel((x, y), tuple(requested_color) + (image_color.getpixel((x, y))[-1],))

    for x in range(image_grey.width):
        for y in range(image_grey.height):
            color = image_grey.getpixel((x, y))
            if color[-1] != 0:
                image_grey.putpixel((x, y), (color[0], abs(color[0] - 128) * 2))

    return Image.alpha_composite(image_color, image_grey.convert('RGBA'))
