#!/usr/bin/env python
"""
classify.py is an out-of-the-box image classifer callable from the command line.

By default it configures and runs the Caffe reference ImageNet model.
"""
import numpy as np
import pandas as pd
import os
import sys
import argparse
import glob
import time
import shutil

import caffe
os.chdir('/home/andy/caffe/python')
myglob = []
labels = []
outdir = ''
batchsize = 100
classifier = []
args = []


def processresult(predictions, aglob):
    for j in range(len(predictions)):
        indices = (-predictions[j]).argsort()[:5]
        predicted_labels = labels[indices]
        meta = [
            (p, '%.5f' % predictions[j][i])
            for i, p in zip(indices, predicted_labels)
            ]

        print(aglob[j])
        if predictions[j][indices[0]] >= 0.0:
            classdir = outdir + '/' + predicted_labels[0]
            if not os.path.exists(classdir):
                os.makedirs(classdir)
            shutil.copy2(aglob[j], classdir)

        print(meta)


def process(mj):
    if mj < 0:
        aglob = myglob[mj:]
    else:
        aglob = myglob[mj * batchsize: (mj + 1) * batchsize]

    inputs = [caffe.io.load_image(im_f)
              for im_f in aglob]

    start = time.time()
    predictions = classifier.predict(inputs, not args.center_only)
    endtime = time.time() - start

    processresult(predictions, aglob)
    print("Done in %.2f s." % endtime)


def main(argv):
    pycaffe_dir = os.path.dirname(__file__)
    global myglob
    global labels
    global outdir
    global classifier
    global args

    parser = argparse.ArgumentParser()
    # Required arguments: input and output files.
    parser.add_argument(
        "input_file",
        help="Input image, directory, or npy."
    )
    parser.add_argument(
        "output_file",
        help="Output npy filename."
    )
    # Optional arguments.
    parser.add_argument(
        "--model_def",
        default=os.path.join(pycaffe_dir,
                             "../models/bvlc_reference_caffenet/deploy.prototxt"),
        help="Model definition file."
    )
    parser.add_argument(
        "--pretrained_model",
        default=os.path.join(pycaffe_dir,
                             "../models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"),
        help="Trained model weights file."
    )
    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation."
    )
    parser.add_argument(
        "--center_only",
        action='store_true',
        help="Switch for prediction from center crop alone instead of " +
             "averaging predictions across crops (default)."
    )
    parser.add_argument(
        "--images_dim",
        default='256,256',
        help="Canonical 'height,width' dimensions of input images."
    )
    parser.add_argument(
        "--mean_file",
        default=os.path.join(pycaffe_dir,
                             'caffe/imagenet/ilsvrc_2012_mean.npy'),
        help="Data set image mean of [Channels x Height x Width] dimensions " +
             "(numpy array). Set to '' for no mean subtraction."
    )
    parser.add_argument(
        "--input_scale",
        type=float,
        help="Multiply input features by this scale to finish preprocessing."
    )
    parser.add_argument(
        "--raw_scale",
        type=float,
        default=255.0,
        help="Multiply raw input by this scale before preprocessing."
    )
    parser.add_argument(
        "--channel_swap",
        default='2,1,0',
        help="Order to permute input channels. The default converts " +
             "RGB -> BGR since BGR is the Caffe default by way of OpenCV."
    )
    parser.add_argument(
        "--ext",
        default='jpg',
        help="Image file extension to take as input when a directory " +
             "is given as the input file."
    )
    parser.add_argument(
        "--labels_file",
        default=os.path.join(pycaffe_dir,
                             "../data/ilsvrc12/synset_words.txt"),
        help="Readable label definition file."
    )
    parser.add_argument(
        "--print_results",
        action='store_true',
        help="Write output text to stdout rather than serializing to a file."
    )
    args = parser.parse_args()

    image_dims = [int(s) for s in args.images_dim.split(',')]

    mean, channel_swap = None, None
    if args.mean_file:
        mean = np.load(args.mean_file)
    if args.channel_swap:
        channel_swap = [int(s) for s in args.channel_swap.split(',')]

    if args.gpu:
        caffe.set_mode_gpu()
        print("GPU mode")
    else:
        caffe.set_mode_cpu()
        print("CPU mode")

    # Make classifier.
    classifier = caffe.Classifier(args.model_def, args.pretrained_model,
                                  image_dims=image_dims, mean=mean,
                                  input_scale=args.input_scale, raw_scale=args.raw_scale,
                                  channel_swap=channel_swap)

    with open(args.labels_file) as f:
        labels_df = pd.DataFrame([
                                     {
                                         'synset_id': l.strip().split(' ')[0],
                                         'name': ' '.join(l.strip().split(' ')[1:]).split(',')[0]
                                     }
                                     for l in f.readlines()])

    labels = labels_df.sort('synset_id')['name'].values

    # Load numpy array (.npy), directory glob (*.jpg), or image file.
    args.input_file = os.path.expanduser(args.input_file)
    if args.input_file.endswith('npy'):
        print("Loading file: %s" % args.input_file)
        inputs = np.load(args.input_file)
    elif os.path.isdir(args.input_file):
        print("Loading folder: %s" % args.input_file)
        outdir = args.input_file + '/classified'

        myglob = glob.glob(args.input_file + '/*.' + args.ext)
        r = len(myglob) % batchsize
        w = int(len(myglob) / batchsize)

        for mj in range(0, w):
            process(mj)

        if r > 0:
            process(-r)

    else:
        print("Loading file: %s" % args.input_file)
        outdir = os.path.dirname(args.input_file) + '/classified'
        myglob.append(args.input_file)
        process(0)

        # Save
        # print("Saving results into %s" % args.output_file)
        # np.save(args.output_file, predictions)


if __name__ == '__main__':
    main(sys.argv)
