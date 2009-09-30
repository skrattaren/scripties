#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  This script is designed to parse local AudioCD database of foobar2000
## audio player (http://foobar2000.org/)
##
## Should work both on Win32 and operating systems (-;E
## Developed under Python 2.6, but 2.4 and 2.5 should suffice
## (report if they don't)
##
## Aimed to satisfy my personal needs, so it'll be polished and expanded
## only if you ask me to. Or edit it yourself.
##
## Released under GNU GPL v3 or later
## http://www.gnu.org/copyleft/gpl.html
##
## 2009 © Stjujsckij Nickolaj (krigstask)
##
## Report issues and post suggestions here:
## http://code.google.com/p/krigstasks-samling/issues/list


import os
from operator import itemgetter

# These vars will be set from commandline some day
CDDB_DIR = '/home/sterkrig/tmp/cddb/'
#CDDB_DIR = os.getenv('APPDATA') + '\\foobar2000'
OUTPUT_FILE = '/home/sterkrig/tmp/fddb.txt'

# Some constants
SYMBOLS = '\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x16\r\t'
KWDS = ['album', 'artist', 'comment', 'date', 'genre',
        'title', 'totaltracks', 'tracknumber']


def print_dictlist(dict_list):
    ''' Prints list of dictionaries [DEBUG] '''
    for dicty in dict_list:
        for key, val in dicty.iteritems():
            print "%s: %s" % (key, val)
        print '-------'

def parse_file(cdfile):
    ''' Parses file object and returns list of track dictionaries '''
#   This regexp might be needed
#    pattern = re.compile(
#            r'[\s\w]+'
#            , re.UNICODE)
    cdstring = cdfile.readline()            # read file
    raw_list = cdstring.split('\x00')       # split by special symbols

    data_list = []
    for string in raw_list:
        try:
#           strip strings from special symbols and try to decode them
            string = string.strip(SYMBOLS)
            if string:
                string = string.decode("utf-8")
                data_list.append(string)
        except UnicodeDecodeError:
            pass                            # fail silently and skip string

    dict_list = []; curr_dict = {}; curr_key = None
    for string in data_list:
        if string in KWDS:
            curr_key = string                   # remember string as key
            if curr_dict.has_key(curr_key):
                dict_list.append(curr_dict)     # remember trackdict
                curr_dict = {}                  # and start new one
        else:
            curr_dict[curr_key] = string        # add key-val to trackdict
            curr_key = None                     # forget current key
    dict_list.append(curr_dict)             # remember last trackdict
    del(curr_dict); del(data_list)

    dict_list = sorted(dict_list, key=itemgetter('tracknumber'))   # sort tracks

    return dict_list

# try with this file
cdfile = open('%s%s0020918D' % (CDDB_DIR, os.sep),  'r')
print_dictlist(parse_file(cdfile))
cdfile.close()


def main():
    ''' Cycles through directory and parses files '''
    for cdfilename in os.listdir(CDDB_DIR):
        cdfile = open('%s%s%s' % (CDDB_DIR, os.sep, cdfilename),  'r')
        parse_file(cdfile)
        cdfile.close()
