import v4l2
import fcntl

import ctypes

vd = open('/dev/video0', 'r+b', buffering=0)

cp = v4l2.v4l2_capability()
fmt = v4l2.v4l2_fmtdesc()
frmsize = v4l2.v4l2_frmsizeenum()
frmival = v4l2.v4l2_frmivalenum()


while( fcntl.ioctl(vd, v4l2.VIDIOC_ENUM_FRAMESIZES, frmsize) >= 0 ):
    print(frmsize.type)
    try:
        print(frmsize.discrete.width)
        print(frmsize.discrete.height)
        print(frmsize.stepwise.max_width)
        print(frmsize.stepwise.max_height)
    except:
        pass
    frmsize.index += 1

'''
enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    struct v4l2_fmtdesc fmt;
    struct v4l2_frmsizeenum frmsize;
    struct v4l2_frmivalenum frmival;

    fmt.index = 0;
    fmt.type = type;
    while (ioctl(fd, VIDIOC_ENUM_FMT, &fmt) >= 0) {
        frmsize.pixel_format = fmt.pixelformat;
        frmsize.index = 0;
        while (ioctl(fd, VIDIOC_ENUM_FRAMESIZES, &frmsize) >= 0) {
            if (frmsize.type == V4L2_FRMSIZE_TYPE_DISCRETE) {
                printf("%dx%d\n", 
                                  frmsize.discrete.width,
                                  frmsize.discrete.height);
            } else if (frmsize.type == V4L2_FRMSIZE_TYPE_STEPWISE) {
                printf("%dx%d\n", 
                                  frmsize.stepwise.max_width,
                                  frmsize.stepwise.max_height);
            }
                frmsize.index++;
            }
            fmt.index++;
    }
'''

#cp = v4l2.v4l2_capability()
#fcntl.ioctl(vd, v4l2.VIDIOC_QUERYCAP, cp)
#print(cp.driver)
#print(cp.card)
vd.close()
