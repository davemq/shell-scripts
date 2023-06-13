#!/usr/bin/env python

import argparse
from os import environ
from pathlib import Path
import random

# constants
DIRS      = [environ['HOME'], '/usr']
NFILES    = 1

files     = []
patterns  = ['*.gif', '*.jpg', '*.png']

parser = argparse.ArgumentParser(prog='random_pic')
parser.add_argument('nfiles', type=int, default=NFILES, help='Number of files to print', nargs='?')
parser.add_argument('-d', '--dir', action='extend', nargs='*', help='Directory to search')
args = parser.parse_args()
if args.nfiles <= 0:
    raise ValueError('nfiles must be a positive integer')
if args.dir is None:
    args.dir = DIRS

for d in args.dir:
    p = Path(d)
    for pat in patterns:
        files += [f for f in p.rglob(pat)]

for i in range(args.nfiles):
    print(str(random.choice(files)))
