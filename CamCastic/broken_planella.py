# Video thumbnailer, PyGI version, not working (creates unreadable thumbnails)
 
import os
import sys
 
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
Gst.init(None)
 
def get_frame(path, offset=5, caps=Gst.Caps.from_string('image/png')):
    pipeline = Gst.parse_launch('playbin')
    pipeline.props.uri = 'file://' + os.path.abspath(path)
    pipeline.props.audio_sink = Gst.ElementFactory.make('fakesink', 'fakeaudio')
    pipeline.props.video_sink = Gst.ElementFactory.make('fakesink', 'fakevideo')
    pipeline.set_state(Gst.State.PAUSED)
    # Wait for state change to finish.
    pipeline.get_state(Gst.CLOCK_TIME_NONE)
    assert pipeline.seek_simple(
        Gst.Format.TIME, Gst.SeekFlags.FLUSH, offset * Gst.SECOND)
    # Wait for seek to finish.
    pipeline.get_state(Gst.CLOCK_TIME_NONE)
    buffer = pipeline.emit('convert-sample', caps).get_buffer()
    pipeline.set_state(Gst.State.NULL)
    return buffer
 
def main():
    buf = get_frame(sys.argv[1])
 
    with file('frame.png', 'w') as fh:
        # This (i.e. getting the data from the buffer) does not work. See https://bugzilla.gnome.org/show_bug.cgi?id=678663
        fh.write(bytes(buf))
 
if __name__ == '__main__':
    main()