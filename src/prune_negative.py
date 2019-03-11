#!/usr/bin/env python3
"""
this module contains functions that can prune negative samples
"""

import sys
import random
import numpy as np
import matplotlib.pyplot as plt

random.seed(10)


def _has_digits(string):
    return any(char.isdigit() for char in string)


def _has_parenthese(string):
    return any(char in ['(', ')'] for char in string)


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: >> python {} <in_filename> <out_filename> <black_filename> <train or test>".format(
                sys.argv[0]))
        sys.exit(1)
    in_filename, out_filename, black_filename = sys.argv[1:4]
    train = True if sys.argv[-1] == "train" else False
    blacklist = set()
    with open(black_filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        blacklist.add(line.strip())
    print("load {} words from {}".format(len(blacklist), black_filename))
    with open(in_filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    count = 0
    if train:
        # training: pick 1200 negative samples(570 single words, 600 double words, 30 triple words)
        numbers = [570, 600, 30]
        lst = [[], [], []]
        lens = set()
        for line in lines:
            word = line.split(", ")[0]
            tokens = word.lower().split()
            for token in tokens:
                if token in blacklist or _has_digits(
                        token) or _has_parenthese(token):
                    break
            else:
                lens.add(len(tokens))
                lst[len(tokens) - 1].append(line)
                count += 1
        print(
            "negative sample are pruned from {:d} to {:d}".format(
                len(lines), count))
        picked = []
        picked.extend(random.sample(lst[0], numbers[0]))
        picked.extend(random.sample(lst[1], numbers[1]))
        picked.extend(random.sample(lst[2], numbers[2]))
    else:
        #testing: pick 200 negative samples
        n_samples = 200
        lst = []
        lens = set()
        for line in lines:
            word = line.split(", ")[0]
            tokens = word.lower().split()
            for token in tokens:
                if token in blacklist or _has_digits(
                        token) or _has_parenthese(token):
                    break
            else:
                lens.add(len(tokens))
                lst.append(line)
                count += 1
        print(
            "negative sample are pruned from {:d} to {:d}".format(
                len(lines), count))
        picked = random.sample(lst, n_samples)

    with open(out_filename, 'w') as f:
        for line in picked:
            f.write(line + "\n")
    print("write {:d} samples to {}".format(len(picked), out_filename))


if __name__ == "__main__":
    main()
