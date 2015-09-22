#!/usr/bin/env python2.7

from __future__ import print_function
import argparse
import gzip
import sys

import PIL.Image
import pynbt

from colours import base_colours
from icons import get_icon

DEFAULT_VERSION = '1.8.1'
VERSIONS = '1.8.0', '1.8.1'

ERROR_COLOUR = 255,0,0,255

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

    in_file = sys.stdin if args.in_file == '-' \
        else open(args.in_file)
    out_file = sys.stdout if args.out_file == '-' \
        else open(args.out_file, 'w')
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
    unknown = set()
    for i in xrange(width * height):
        colour_id = data[i]
        colour = colour_id_to_rgba(colour_id, version)
        if colour is None:
            if colour_id not in unknown and warn:
                unknown.add(colour_id)
                print('Warning: unknown colour ID %d.'
                    % colour_id, file=sys.stderr)
            colour = ERROR_COLOUR
        y, x = divmod(i, width)
        img.putpixel((x, y), colour)
    img.save(img_file, 'png')    

def map_icons_to_img(icons, img_file, width=128, height=128, margin=8, scale=1):
    img = PIL.Image.new('RGBA', (width*scale + 2*margin, height*scale + 2*margin))
    icons = list(icons)
    for (type, direction, (x, y)) in icons:
        icon = get_icon(type, direction, scale)
        point = (margin + ((x + width)*scale - icon.size[0])/2,
                 margin + ((y + height)*scale - icon.size[1])/2)
        img.paste(icon, point, icon)
    img.save(img_file, 'png')

def colour_id_to_rgba(id, version):
    base_id, shade_id = divmod(id, 4)
    if base_id not in base_colours:
        return None
    r,g,b,a = base_colours[base_id]
    shade_mul = \
        180 if shade_id == 0 else \
        220 if shade_id == 1 else \
        255 if shade_id == 2 else \
        220 if shade_id == 4 and version == '1.8.0' else \
        134 if shade_id == 4 and version == '1.8.1' else None
    r,g,b = (shade_mul*r)/255, (shade_mul*g)/255, (shade_mul*b)/255
    return r,g,b,a

if __name__ == '__main__':
    main()
