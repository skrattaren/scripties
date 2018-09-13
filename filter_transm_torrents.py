#!/usr/bin/env python
'''
Filter and remove torrents inactive for a given time
'''

from __future__ import print_function, unicode_literals

import argparse

from datetime import datetime

import transmissionrpc

# Python 2 hack
try:
    input = raw_input
except NameError:
    pass


def get_args():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filter_text', help="word or phrase to look for",
                        nargs='?')
    parser.add_argument('--age', '-a', type=int, default=7,
                        help="allowed inactivity (in days), default is 7")
    parser.add_argument('--ratio', '-r', type=float, default=1.0,
                        help="minimum required ratio, default is 1.0")
    parser.add_argument('--case-insensitive', '-i', action='store_true',
                        help="ignore case when searching for text")
    args = parser.parse_args()
    if not args.case_insensitive:
        return args
    if not args.filter_text:
        parser.error("`--case-insensitive` is useless without `filter_text`")
    args.filter_text = args.filter_text.lower()
    return args


def inactive_for(t):
    '''
    Return "inactive for " timedelta for torrent
    '''
    now = datetime.now()
    return (now - t.date_active)


def main():
    '''
    Main wrapping function
    '''
    args = get_args()

    filter_list = []
    if args.filter_text:
        filter_list.append(lambda t: args.filter_text
                           in (t.name.lower() if args.case_insensitive
                               else t.name))
    if args.age:
        filter_list.append(lambda t: inactive_for(t).days >= args.age)
    if args.ratio:
        filter_list.append(lambda t: t.ratio >= args.ratio)

    t_cl = transmissionrpc.Client()
    torrents = filter(lambda t: all(f(t) for f in filter_list),
                      t_cl.get_torrents())
    ids_to_remove = []
    for t in torrents:
        print("'{}' is safe to be removed (ratio: {}, inactive for {})"
              "".format(t.name, t.ratio, inactive_for(t)))
        answer = input("Remove? [Y/n] ").lower()
        if answer and answer != 'y':
            if answer != 'n':
                print("Answer not understood, skipping torrent")
            continue
        ids_to_remove.append(t.id)
    if ids_to_remove:
        t_cl.remove_torrent(ids_to_remove, delete_data=True)
    else:
        print("No torrents to remove")


if __name__ == '__main__':
    main()
