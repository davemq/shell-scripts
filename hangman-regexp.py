#!/usr/bin/env python

import argparse
import re
import string

class C:
    pass

global chars, outchars

chars = string.ascii_lowercase
outchars = r'[' + chars + r']'

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog='hangman-regexp', 
        description='Generate a regular expression from a hangman expression')
    parser.add_argument("-x", "--remove", 
                        help="remove character from generated regular expression",
                        action="append")
    parser.add_argument("phrase", help="hangman phrase")

    c = C()
    
    parser.parse_args(namespace=c)

    remove = []
    for ch in c.remove:
        remove.append(ch.lower())
        chars = chars.replace(ch.lower(), '')
        outchars = outchars.replace(ch.lower(), '')

    print(f'{c.phrase=} {remove=} {chars=} {outchars=}')
