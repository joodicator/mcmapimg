#!/usr/bin/env python

import sys
import os
import cgi

import cgitb
cgitb.enable()

try:
    from io import BytesIO as StringIO
except ImportError:
    from cStringIO import StringIO

from mcmapimg import mcmapimg    

fields = cgi.FieldStorage()

if fields['version'].value not in mcmapimg.VERSIONS:
    raise Exception(f"Unknown version: {fields['version']}.")
out_buffer = StringIO()
mcmapimg.map_to_img(fields['in_file'].file, out_buffer)
out_data = out_buffer.getvalue()

print('Content-Type: image/png')
print('Cache-Control: no-store')
print('')
sys.stdout.flush()

os.write(sys.stdout.fileno(), out_data)