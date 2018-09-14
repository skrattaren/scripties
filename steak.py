#!/usr/bin/env python
"""
Utility script to help frying steaks and suchlike =)
"""

from __future__ import division, print_function, unicode_literals

import argparse

DEFAULT_INTERVAL = 30


def beep():
    """
    Play audio signal with SoX
    """
    pass


def to_ternary_list(num):
    """
    Convert a number to ternary numeral list for audio "encoding"
    """
    if num < 3:
        return [num]
    return to_ternary_list(num // 3) + [num % 3]


def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', '--interval', default=DEFAULT_INTERVAL,
                        help="interval between beeps", type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    print(to_ternary_list(args.interval))


if __name__ == '__main__':
    main()
