
import os.path
import math
import PIL.Image


SIZE = 8

def load_icons():
    icons = []
    path = os.path.join(os.path.dirname(__file__), 'assets', 'map_icons.png')
    with open(path, 'rb') as file:
        sheet = PIL.Image.open(file)
        sheet = sheet.convert('RGBA')
        for j in range(sheet.size[1]//SIZE):
            for i in range(sheet.size[0]//SIZE):
                x0, y0 = i*SIZE, j*SIZE
                x1, y1 = x0+SIZE, y0+SIZE
                icon = sheet.transform((SIZE,SIZE), PIL.Image.EXTENT, (x0,y0,x1,y1))
                icons.append(icon)
    return icons

def get_icon(type, direction, scale):
    icon = icon_cache.get((type, direction, scale))
    if icon is not None: return icon

    base = base_icons[type]
    icon = base.resize((scale*base.size[0], scale*base.size[1]))
    icon = icon.rotate(180.0 + direction*180.0/8, expand=True)

    icon_cache[(type, direction, scale)] = icon
    return icon

base_icons = load_icons()
icon_cache = dict()
