#!/usr/bin/env python

"""
Print random file name(s) from a set of directories and patterns.
"""

import argparse
import fnmatch
from os import environ
from pathlib import Path
import random

# constants
DIRS = [environ["HOME"], "/usr"]
NFILES = 1
PATTERNS = ["*.gif", "*.jpg", "*.png"]

files = set()

parser = argparse.ArgumentParser(prog="random_pic")
parser.add_argument(
    "-n",
    "--nfiles",
    type=int,
    default=NFILES,
    help="Number of files to print",
    nargs="?",
)
parser.add_argument(
    "-d", "--dir", action="extend", nargs="*", help="Directory to search"
)
args = parser.parse_args()
if args.nfiles <= 0:
    raise ValueError("nfiles must be a positive integer")
if args.dir is None:
    args.dir = DIRS

# Find pattern matches
for d in args.dir:
    p = Path(d)
    dev = p.stat().st_dev  # Save device number, to avoid crossing mount points
    for root, dirs, fs in p.walk(top_down=True):
        for d in dirs:
            if (root / d).stat().st_dev != dev:
                dirs.remove(d)  # Don't cross to another filesystem
        for pat in PATTERNS:
            files |= {root / f for f in fs if fnmatch.fnmatch(f, pat)}

if len(files) >= args.nfiles:
    l = list(files)
    for i in range(args.nfiles):
        print(str(random.choice(l)))
