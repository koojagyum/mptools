from PIL import Image

from . import debug

def resize(im, size, resample=Image.BILINEAR):
    return im.resize(size, resample=resample)


def process_resize(imgpath, outpath, size, use_png=True):
    # debug.enable_log = True
    debug.log('path: {}'.format(imgpath))
    im = Image.open(imgpath)
    debug.log('im: {}'.format(im))
    im_ = resize(im, size)
    if im_.mode != 'RGB':
        debug.log('mod was changed: {}'.format(imgpath))
        im_ = im_.convert('RGB')

    if use_png:
        outpath = outpath[:-4] + '.png'
        im_.save(outpath)
    else:
        im_.save(outpath, 'JPEG', quality=100)

    return True
