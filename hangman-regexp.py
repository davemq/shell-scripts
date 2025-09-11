#!/usr/bin/env python

import argparse
import string

global chars, outchars

chars = string.ascii_lowercase
outchars = r"[" + chars + r"]"

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
        outchars = outchars.replace(ch.lower(), "")

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
                outchars = outchars.replace(ch, "")

    # Write regexp
    regex = "\\" + "<"
    for w in words:
        wordchars = w.split(" ")
        unders = 0
        for ch in wordchars:
            if ch in string.ascii_lowercase:
                if unders > 0:
                    regex += outchars
                if unders > 1:
                    regex += f"\\{{{unders}\\}}"
                unders = 0
                regex += ch
            elif ch == "_":
                unders += 1
        if unders > 0:
            regex += outchars
        if unders > 1:
            regex += f"\\{{{unders}\\}}"
        regex += "  *"
    regex = regex.rstrip("*")
    regex = regex.rstrip(" ")
    regex += "\\" + ">"

    print(regex)
