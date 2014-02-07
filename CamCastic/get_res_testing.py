#!/usr/bin/env python3.3

import os, sys

import gst

import struct

def get_size(blob):
    head = blob[0:24]
    check = struct.unpack('>i', head[4:8])[0]
    if check != 0x0d0a1a0a:
        return (0, 0)
        width, height = struct.unpack('>ii', head[16:24])
    return (width, height)

'''
important parts
    gst.Caps

    and

    buffer = pipeline.emit('convert-frame', caps)
    ...
    return buffer

remember the planella work on a port

using gst would be a better solution than using v4l2 directly...
someone else handles bugs for you
'''

def get_frame(path, offset=5, caps=gst.Caps('image/png')):
    pipeline = gst.parse_launch('playbin2')
    pipeline.props.uri = 'file://' + os.path.abspath(path)
    pipeline.props.audio_sink = gst.element_factory_make('fakesink')
    pipeline.props.video_sink = gst.element_factory_make('fakesink')
    pipeline.set_state(gst.STATE_PAUSED)
    # Wait for state change to finish.
    pipeline.get_state()
    assert pipeline.seek_simple(
        gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, offset * gst.SECOND)
    # Wait for seek to finish.
    pipeline.get_state()
    buffer = pipeline.emit('convert-frame', caps)
    pipeline.set_state(gst.STATE_NULL)
    return buffer

def main():
    buf = get_frame(sys.argv[1])
    get_size(buf)

if __name__ == '__main__':
    main()