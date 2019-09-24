import numpy as np
import os
import tensorflow as tf

from PIL import Image

from . import debug


def save(img, outpath, use_png):
    if use_png:
        outpath = outpath[:-4] + '.png'

    img_pi = Image.fromarray(np.uint8(img))
    img_pi.save(outpath)


def process_resize(imgpath, outpath, size, use_png=True):
    ext_jpeg = ['.jpg', '.JPG', '.JPEG', '.jpeg']
    ext_png = ['.png', '.PNG']

    _, ext = os.path.splitext(outpath)

    img = tf.io.read_file(imgpath)
    if ext in ext_jpeg:
        img = tf.image.decode_jpeg(img, channels=3)
    elif ext in ext_png:
        img = tf.image.decode_png(img, channels=3)
    else:
        img = tf.image.decode_image(img, channels=3)

    img = tf.image.resize(img, size)
    img = img.numpy()

    save(img, outpath, use_png)

    return True
