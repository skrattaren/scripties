#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Inotify watcher '''

from optparse import OptionParser, OptionGroup
import inotifyx, logging, os, subprocess, sys
from time import sleep

from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename, CppLexer
from pygments.formatters import TerminalFormatter

LOG_FILE = '/tmp/inotify_viewer.log'

def inotify_watch(wfile, debug=False, log=LOG_FILE):

    if debug:
        logging.basicConfig(filename=log, level=logging.DEBUG)

    # Initting inotifyx
    watcher = inotifyx.init()

    inotifyx.add_watch(watcher, wfile, inotifyx.IN_MODIFY)

    try:
        logging.debug('Starting infinite loop…\n')
        while True:
            logging.debug('Starting iteration…\n')

            # it's possible to get output text somehow differently... some day
            with open(wfile, 'r') as file_to_read:
                string = file_to_read.read()

            # probably it'd be optional
            string = highlight(string,
                               guess_lexer_for_filename(wfile, ""),
                               TerminalFormatter(bg='dark'))

            # all right, may be even output should be optional!
            logging.debug('Spawning less…\n')
            less = subprocess.Popen(['less', '-'],
                                    stdin=subprocess.PIPE)
            logging.debug('less spawned, piping data…\n')
            less.stdin.write(string)
            less.stdin = sys.stdin

            logging.debug('Data piped, waiting for inotification…\n')
            inotifyx.get_events(watcher)
            logging.debug('Inotified, killing less\n')
            less.terminate()
            logging.debug('_______________________\n')


    except KeyboardInterrupt:
        logging.debug('Interruption caught, closing everything\n')
        less.terminate()
        os.close(watcher)


def main():
    ''' Main function. Parses arguments and passes them ... '''

    usage = '''Usage: %prog [options] file_to_watch'''
    opt_parser = OptionParser(usage=usage)

    log_group = OptionGroup(opt_parser, "Debugging options")
    log_group.add_option("-d", "--debug", action="store_false", default=True,
                      help="log debug messages (see '--log')", dest="debug")
    log_group.add_option("-l", "--log", dest="log",
                      help="log debug ouput to LOG_FILE file (see '--debug')",
                      metavar="LOG_FILE", default=LOG_FILE)

#    watch_group = OptionGroup(opt_parser, "General options")
#    watch_group.add_option("--watch-file", dest="watch_file",
#                        metavar='FILE', help="file to watch")

    opt_parser.add_option_group(log_group)
#    opt_parser.add_option_group(watch_group)

    (options, args) = opt_parser.parse_args()

    if options.log and not options.debug:
        opt_parser.error("there's no sense in specifying logfile without debug mode (see --help)")
    if options.debug and not options.log:
        print "Log file for debug mode not specified, using default", LOG_FILE
        sleep(7)

    if len(args) > 1:
        print "How should I know what to watch from this list?"
        print "Watching only first one, '{first}'".format(first=args[0])
        sleep(7)

    inotify_watch(wfile=args[0], debug=options.debug, log=options.log)


if __name__=="__main__":
    # If run directly
    main()
