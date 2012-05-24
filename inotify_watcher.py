#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Inotify watcher
***************

Quite simple script to watch file events via Linux kernel ``inotify`` subsystem
and take user-defined actions upon them.

 © 2010-2012 Nikolaj Sjujskij
Distributed under the terms of the GNU General Public License v3
'''

from optparse import OptionParser, OptionGroup
import os.path

import inotifyx
import docutils.core
from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import TerminalFormatter

implemented_actions = {}

def register_action(name=None, catalogue=implemented_actions):
    ''' Registration decorator, maintaining dictionary of implemented actions'''
    name = name or f.__name__
    def register_closure(f):
        catalogue[name] = f
        def tmp(*args, **kwargs):
            return f(*args, **kwargs)
        return tmp
    return register_closure

@register_action('hlite')
def highlight_watched(filename):
    ''' File contents highlighter '''
    with open(filename, 'r') as file_to_read:
        content = file_to_read.read()
    content = highlight(content,
                        guess_lexer_for_filename(filename, ""),
                        TerminalFormatter(bg='dark'))
    print(content)

@register_action('rsthtml')
def view_rst_as_html(filename):
    ''' Function converting reStructuredText to HTML for display in browser '''
    htmlfile = '/tmp/%s.html' % os.path.basename(filename)
    print('file://%s' % htmlfile)
    docutils.core.publish_file(source_path=filename, destination_path=htmlfile,
                               writer_name='html')

def ino_watch(file_to_watch, action, action_args=[], action_kwargs={}):
    ''' ``inotify``-based watcher, applying function on modification events '''
    watcher = inotifyx.init()
    inotifyx.add_watch(watcher, file_to_watch, inotifyx.IN_MODIFY)
    while True:
        action(file_to_watch, *action_args, **action_kwargs)
        inotifyx.get_events(watcher)

def main():
    ''' Mainloop function handling arguments and control flow '''
    usage = '''Usage: %prog [options] file_to_watch'''
    opt_parser = OptionParser(usage=usage)
    opt_parser.add_option("-a", "--action", dest="action",
                      help="action to be undertaken",
                      metavar="ACTION", default='hlite')
    (options, args) = opt_parser.parse_args()
    if len(args) > 1:
        print("How should I know what to watch from this list?\n"
              "Watching only first one, '%s'" % args[0])
        sleep(7)
    file_to_watch = args[0]
    action = implemented_actions.get(options.action)
    if not action:
        import sys
        sys.stderr.write("Unknown action: '%s'\n" % options.action)
        sys.exit(1)
    try:
        ino_watch(file_to_watch, action)
    except KeyboardInterrupt:
        print('\nCaught keyboard interrupt, exiting')

if __name__ == "__main__":
    main()

