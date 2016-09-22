# -*- coding: utf-8 -*-

import getopt
import sys

import pngquant


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hf:d:', ['help', 'file=', 'dir='])
    except getopt.GetoptError:
        # usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            # usage()
            sys.exit()
        elif opt in ('-f', 'file'):
            quant_file = arg
        elif opt in ('-d', '--dir'):
            quant_dir = arg

    pngquant.config(quant_file)
    pngquant.quant_dir(quant_dir)


if __name__ == '__main__':
    main(sys.argv[1:])
