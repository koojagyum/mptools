import argparse
import os
import sys

from . import imresize_impl_pi as impl
# from . import imresize_impl_tf as impl


args = None


def collect_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        '--outdir', '-o',
        required=True,
        type=str,
        help='Dirpath of output image'
    )
    parser.add_argument('--width', '-W', type=int, required=True)
    parser.add_argument('--height', '-H', type=int, required=True)
    parser.add_argument(
        '--overwrite',
        dest='overwrite',
        action='store_true',
    )
    parser.add_argument(
        '--no-overwrite',
        dest='overwrite',
        action='store_false',
    )
    parser.set_defaults(overwrite=False)

    return parser.parse_known_args()[0]


def init():
    global args
    args = collect_args()


def process(imgpath):
    global args

    imgname = os.path.basename(imgpath)
    outpath = os.path.join(args.outdir, imgname)

    result = process_resize(
        imgpath,
        outpath,
        size=(args.width, args.height),
        overwrite=args.overwrite,
        use_png=True
    )

    return result


def process_resize(imgpath, outpath, size, overwrite=False, use_png=True):
    if use_png:
        outpath = outpath[:-4] + '.png'
    if not overwrite:
        if os.path.exists(outpath):
            # print('{} is already exists'.format(outpath))
            return False

    return impl.process_resize(imgpath, outpath, size, use_png=use_png)
