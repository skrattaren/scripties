#!/usr/bin/env python
'''
Filter and remove torrents inactive for a given time
'''

from __future__ import print_function, unicode_literals

import argparse

from datetime import datetime

import transmissionrpc


def get_args():
    '''
    Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filter_text', help="word or phrase to look for")
    parser.add_argument('--age', '-a', type=int, default=7,
                        help="allowed inactivity (in days), default is 7")
    parser.add_argument('--ratio', '-r', type=float, default=1.0,
                        help="minimum required ratio, default is 1.0")
    return parser.parse_args()


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
        filter_list.append(lambda t: args.filter_text in t.name)
    if args.age:
        filter_list.append(lambda t: inactive_for(t).days >= args.age)
    if args.ratio:
        filter_list.append(lambda t: t.ratio >= args.ratio)

    t_cl = transmissionrpc.Client()
    torrents = filter(lambda t: all(f(t) for f in filter_list),
                      t_cl.get_torrents())
    ids_to_remove = []
    for t in torrents:
        print("'{}' is safe to be removed (inactive for {})"
              "".format(t.name, inactive_for(t)))
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
