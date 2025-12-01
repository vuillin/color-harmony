import random
from color_utils import hex_to_rgb, rgb_to_hsv, hsv_to_rgb, rgb_to_hex

def generate_harmonies(base_hex):
    """
    Generates a dictionary containing different color harmonies based on a base HEX color.
    Returns Complementary, Triadic, Analogous, Split Complementary, Monochrome, and Pastel.
    """
    rgb = hex_to_rgb(base_hex)
    h, s, v = rgb_to_hsv(rgb)
    
    palettes = {}

    # Complementary
    comp_h = (h + 0.5) % 1.0
    palettes['Complementary'] = [base_hex, rgb_to_hex(hsv_to_rgb((comp_h, s, v)))]

    # Triadic
    tri_h1 = (h + 1/3) % 1.0
    tri_h2 = (h + 2/3) % 1.0
    palettes['Triadic'] = [
        base_hex,
        rgb_to_hex(hsv_to_rgb((tri_h1, s, v))),
        rgb_to_hex(hsv_to_rgb((tri_h2, s, v)))
    ]

    # Analogous
    ana_h1 = (h - 1/12) % 1.0
    ana_h2 = (h + 1/12) % 1.0
    palettes['Analogous'] = [
        rgb_to_hex(hsv_to_rgb((ana_h1, s, v))),
        base_hex,
        rgb_to_hex(hsv_to_rgb((ana_h2, s, v)))
    ]

    # Monochrome
    palettes['Monochrome'] = [
        base_hex,
        rgb_to_hex(hsv_to_rgb((h, max(0, s - 0.3), v))),
        rgb_to_hex(hsv_to_rgb((h, min(1, s + 0.2), max(0, v - 0.2)))),
        rgb_to_hex(hsv_to_rgb((h, s, max(0, v - 0.4)))),
        rgb_to_hex(hsv_to_rgb((h, max(0, s - 0.5), min(1, v + 0.3))))
    ]

    # Pastel
    palettes['Pastel'] = [
        rgb_to_hex(hsv_to_rgb((h, 0.3, 0.95))),
        rgb_to_hex(hsv_to_rgb(((h + 0.2) % 1.0, 0.3, 0.95))),
        rgb_to_hex(hsv_to_rgb(((h + 0.4) % 1.0, 0.3, 0.95))),
        rgb_to_hex(hsv_to_rgb(((h + 0.6) % 1.0, 0.3, 0.95))),
        rgb_to_hex(hsv_to_rgb(((h + 0.8) % 1.0, 0.3, 0.95)))
    ]

    return palettes

def generate_random_palette(count=5):
    """
    Generates a random aesthetically pleasing palette.
    """
    base_h = random.random()
    colors = []
    for i in range(count):
        hue = (base_h + (i * (1/count))) % 1.0
        sat = random.uniform(0.4, 0.7)
        val = random.uniform(0.7, 0.95)
        colors.append(rgb_to_hex(hsv_to_rgb((hue, sat, val))))
    return colors