# -*- coding: utf-8 -*-

import argparse

import paille

parser = argparse.ArgumentParser(description='Paysannerie Assistée Informatiquement par Logiciel Libre Extensif')

parser.add_argument('filename', 
                    default=None,
                    help = 'Path to input file',
                    nargs='?')

args = parser.parse_args()

path = None
if args.filename:
    path = args.filename


paille.gui.start(path)