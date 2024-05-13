# -*- coding: utf-8 -*-

import argparse

import panis

parser = argparse.ArgumentParser(description='Commandes et pesées de boulangerie au levain')

parser.add_argument('filename', 
                    default=None,
                    help = 'Path to input file',
                    nargs='?')

args = parser.parse_args()

path = None
if args.filename:
    path = args.filename


panis.gui.start(path)
