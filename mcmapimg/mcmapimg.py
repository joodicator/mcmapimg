from __future__ import print_function
import argparse
import gzip
import sys
import os

import PIL.Image
import pynbt

from .colours import base_colours
from .icons import get_icon

DEFAULT_VERSION = '1.8.1'
VERSIONS = '1.8.0', '1.8.1'

ERROR_COLOUR = 255,0,0,255

try:
    range = xrange
except NameError:
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file',
        metavar='IN_DAT_FILE', default='-', nargs='?')
    parser.add_argument('out_file',
        metavar='OUT_PNG_FILE', default='-', nargs='?')
    parser.add_argument('--version', dest='version',
        metavar='|'.join(VERSIONS), default=DEFAULT_VERSION)
    args = parser.parse_args()

    if args.version not in VERSIONS:
        print('Error: "%s" is not a recognised version.'
            % args.version, file=sys.stderr)
        print('Acceptable versions are: %s.' % ', '.join(VERSIONS))
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
    nbt = pynbt.NBTFile(io=gzip.GzipFile(mode='r', fileobj=nbt_file))
    width, height = nbt['data']['width'].value, nbt['data']['height'].value
    map_data_to_img(nbt['data']['colors'].value, img_file,
        version=version, warn=warn, width=width, height=height)

def map_data_to_img(
    data, img_file, version=DEFAULT_VERSION, warn=False, width=128, height=128
):
    img = PIL.Image.new('RGBA', (width, height))
    unknown = set() if warn else None
    for i in range(width * height):
        colour_id = data[i]
        colour = colour_id_to_rgba(colour_id, version, unknown)
        if colour is None:
            if warn and ('colour', colour_id) not in unknown:
                unknown.add(('colour', colour_id))
                print('Warning: unknown colour ID %d.' % colour_id,
                      file=sys.stderr)
            colour = ERROR_COLOUR
        y, x = divmod(i, width)
        img.putpixel((x, y), colour)
    img.save(img_file, 'png')    

def map_icons_to_img(icons, img_file, width=128, height=128, margin=8, scale=1):
    img = PIL.Image.new('RGBA', (
        width*scale + 2*margin*scale, height*scale + 2*margin*scale))
    icons = list(icons)
    for (type, direction, (x, y)) in icons:
        icon = get_icon(type, direction, scale)
        point = (margin + ((x + width)*scale - icon.size[0])//2,
                 margin + ((y + height)*scale - icon.size[1])//2)
        img.paste(icon, point, icon)
    img.save(img_file, 'png')

def colour_id_to_rgba(id, version=VERSIONS[-1], unknown=None):
    base_id, shade_id = divmod(id, 4)
    if base_id not in base_colours:
        return None
    r,g,b,a = base_colours[base_id]
    shade_mul = \
        180 if shade_id == 0 else \
        220 if shade_id == 1 else \
        255 if shade_id == 2 else \
        220 if shade_id == 3 and version == '1.8.0' else \
        135 if shade_id == 3 and version == '1.8.1' else None
    if shade_mul is None:
        if unknown is not None and ('shade', shade_id) not in unknown:
            print('Warning: unknown shade ID %d.' % shade_id, file=sys.stderr)
            unknown.add(('shade', shade_id))
    else:
        r,g,b = (shade_mul*r)//255, (shade_mul*g)//255, (shade_mul*b)//255
    return r,g,b,a
