#!/usr/bin/env python

import argparse
import string

global chars

chars = string.ascii_lowercase

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="hangman-regexp",
        description="Generate a regular expression from a hangman expression",
    )
    parser.add_argument(
        "-x",
        "--remove",
        help="remove character from generated regular expression",
        action="append",
    )
    parser.add_argument("phrase", help="hangman phrase")

    c = parser.parse_args()
    if not c.remove:
        c.remove = []

    remove = []
    for ch in c.remove:
        remove.append(ch.lower())
        chars = chars.replace(ch.lower(), "")

    c.phrase = c.phrase.lower()

    # Replace "   " or " / " with "XXX"
    c.phrase = c.phrase.replace("   ", " XXX ")
    c.phrase = c.phrase.replace(" / ", " XXX ")

    # Remove phrase alphabetical characters from chars and outchars
    words = c.phrase.split(" XXX ")
    for w in words:
        wordchars = w.split(" ")
        for ch in wordchars:
            if ch in chars:
                chars = chars.replace(ch, "")

    # Write regexp
    regex = ""
    separator = ""
    for w in words:
        regex += separator + "\\<"
        wordchars = w.split(" ")
        unders = 0
        for ch in wordchars:
            if ch != '_':
                if unders > 0:
                    regex += f'[{chars}]'
                if unders > 1:
                    regex += f"\\{{{unders}\\}}"
                unders = 0
                regex += ch
            else:
                unders += 1
        if unders > 0:
            regex += f'[{chars}]'
        if unders > 1:
            regex += f"\\{{{unders}\\}}"
        regex += "\\>"
        separator = "[[:space:]]\\+"

    print(regex)
