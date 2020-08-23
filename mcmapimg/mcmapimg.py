from __future__ import print_function
from argparse import ArgumentParser
from gzip import GzipFile
import sys
import os

import PIL.Image
from pynbt import NBTFile

from .colours import base_colours
from .icons import get_icon

DEFAULT_VERSION = '1.8.1+'
VERSIONS = '1.8.0-', '1.8.1+'
DEFAULT_WIDTH = 128
DEFAULT_HEIGHT = 128

ERROR_COLOUR = 248,0,248,255

try:
    range = xrange
except NameError:
    pass

def main():
    parser = ArgumentParser()
    parser.add_argument('in_file',   metavar='IN_DAT_FILE',
                        default='-', nargs='?')
    parser.add_argument('out_file',  metavar='OUT_PNG_FILE',
                        default='-', nargs='?'     )
    parser.add_argument('--version', metavar='|'.join(VERSIONS),
                        default=DEFAULT_VERSION, dest='version')
    args = parser.parse_args()

    if args.version not in VERSIONS:
        print(f"Error: {args.version} is not a recognised version.",
              file=sys.stderr)
        print(f"Acceptable versions are: {', '.join(VERSIONS)}.")
        sys.exit(2)

    if args.in_file == '-':
        in_file = os.fdopen(sys.stdin.fileno(), 'rb')
    else:
        in_file = open(args.in_file, 'rb')

    if args.out_file == '-':
        out_file = os.fdopen(sys.stdout.fileno(), 'wb')
    else:
        out_file = open(args.out_file, 'wb')

    with in_file, out_file:
        map_to_img(in_file, out_file, version=args.version, warn=True)

def map_to_img(nbt_file, img_file, version=DEFAULT_VERSION, warn=False):
    nbt = NBTFile(io=GzipFile(mode='r', fileobj=nbt_file))
    width = nbt['data']['width'].value if 'width' in nbt['data'] else None
    height = nbt['data']['height'].value if 'height' in nbt['data'] else None
    map_data_to_img(nbt['data']['colors'].value, img_file,
        version=version, warn=warn, width=width, height=height)

def map_data_to_img(
    data, img_file, version=DEFAULT_VERSION, warn=False, width=None, height=None
):
    width = width or DEFAULT_WIDTH
    height = height or DEFAULT_HEIGHT
    img = PIL.Image.new('RGBA', (width, height))
    unknown = set() if warn else None

    for i in range(width * height):
        colour_id = data[i]
        colour = colour_id_to_rgba(colour_id, version)

        if colour is None:
            if warn and colour_id not in unknown:
                print(f"Warning: unknown colour ID {colour_id}.", file=sys.stderr)
                unknown.add(colour_id)
            colour = ERROR_COLOUR

        y, x = divmod(i, width)
        img.putpixel((x, y), colour)
    img.save(img_file, 'png')

def colour_id_to_rgba(id, version=DEFAULT_VERSION):
    base_id, shade_id = divmod(id, 4)
    if base_id not in base_colours:
        return None
    r,g,b,a = base_colours[base_id]

    shade_mul = \
        180 if shade_id == 0 else \
        220 if shade_id == 1 else \
        255 if shade_id == 2 else \
        220 if shade_id == 3 and version == '1.8.0-' else \
        135 if shade_id == 3 and version == '1.8.1+' else None

    r,g,b = (r*shade_mul)//255, (g*shade_mul)//255, (b*shade_mul)//255
    return r,g,b,a

def map_icons_to_img(
    icons, img_file, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, margin=8,
    scale=1,
):
    img = PIL.Image.new('RGBA', ((width + 2*margin)*scale,
                                 (height + 2*margin)*scale))
    icons = list(icons)

    for (type, direction, (x, y)) in icons:
        icon = get_icon(type, direction, scale)
        point = (margin + ((x + width )*scale - icon.size[0])//2,
                 margin + ((y + height)*scale - icon.size[1])//2)
        img.paste(icon, point, icon)
    img.save(img_file, 'png')
