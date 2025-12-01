import colorsys

def hex_to_rgb(hex_color):
    """
    Converts a HEX color string to an RGB tuple (0-255).
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """
    Converts an RGB tuple to a HEX color string.
    """
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def rgb_to_hsv(rgb):
    """
    Converts an RGB tuple (0-255) to an HSV tuple (0-1).
    """
    return colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

def hsv_to_rgb(hsv):
    """
    Converts an HSV tuple (0-1) to an RGB tuple (0-255).
    """
    r, g, b = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    return (int(r*255), int(g*255), int(b*255))