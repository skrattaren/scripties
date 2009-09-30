#!/usr/bin/env python

import os, re
from operator import itemgetter

CDDB_DIR = '/home/sterkrig/tmp/cddb/'
#CDDB_DIR = os.getenv('APPDATA') + '/foobar2000'
OUTPUT_FILE = '/home/sterkrig/tmp/fddb.txt'
SYMBOLS = '\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x16\r\t'
KWDS = ['album', 'artist', 'comment', 'date', 'genre',
        'title', 'totaltracks', 'tracknumber']



def print_dictlist(dict_list):
    for dicty in dict_list:
        for key, val in dicty.iteritems():
            print "%s: %s" % (key, val)
        print '-------'

def parse_file(cdfile):
    pattern = re.compile(
            r'[\s\w]+'
            , re.UNICODE)
    cdstring = cdfile.readline()
#    for line in cdfile:
#        line = line.decode("utf-8")
#    print pattern.findall(cdstring)
#    print re.compile(r'F.+?svinn').findall(cdstring)
    raw_list = cdstring.split('\x00')
    data_list = []
    for string in raw_list:
        try:
            string = string.strip(SYMBOLS)
            if string:
                string = string.decode("utf-8")
#                print string
                data_list.append(string)
        except Exception, e:
            pass
#    print data_list
    dict_list = []
    curr_dict = {}
    curr_key = None
    for string in data_list:
        if string in KWDS:
            curr_key = string
            if curr_dict.has_key(curr_key):
                dict_list.append(curr_dict)
                curr_dict = {}
        else:
            curr_dict[curr_key] = string
            curr_key = None
    dict_list.append(curr_dict)
    del(curr_dict)
    dict_list = sorted(dict_list, key=itemgetter('tracknumber'))
    print_dictlist(dict_list)


cdfile = open('%s%s0020918D' % (CDDB_DIR, os.sep),  'r')
parse_file(cdfile)
cdfile.close()

def main():
    for cdfilename in os.listdir(CDDB_DIR):
        cdfile = open('%s%s%s' % (CDDB_DIR, os.sep, cdfilename),  'r')
        parse_file(cdfile)
        cdfile.close()
