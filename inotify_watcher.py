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

from optparse import OptionParser
import os.path
import subprocess
import time

import inotifyx

implemented_actions = {}

PAGER_OPTS = ['less', '-']
NROFF_OPTS = ['nroff', '-Tutf8', '-man', '-']


def register_action(name=None, is_firsttimer=False,
                               catalogue=implemented_actions):
    ''' Registration decorator, maintaining dict of implemented actions'''

    def register_closure(f):
        # it'd be nice to have `nonlocal` here in Python 2.x
        add_kwargs = {}
        if is_firsttimer:
            add_kwargs['first_time'] = True

        def tmp(*args, **kwargs):
            if add_kwargs.get('first_time', False):
                kwargs['first_time'] = True
                add_kwargs['first_time'] = False
            return f(*args, **kwargs)

        catalogue[name or f.__name__] = tmp
        # we won't really need it, but return nevertheless
        return tmp

    return register_closure


def page_output(f):
    ''' Pipes output through pager (i.e. `less`) '''
    def paging_wrapper(*args, **kwargs):
        import sys
        output = f(*args, **kwargs)
        if isinstance(output, unicode):
            output = output.encode('utf-8')
        pager = subprocess.Popen(PAGER_OPTS, stdin=subprocess.PIPE)
        pager.stdin.write(output)
        pager.stdin = sys.stdin
        return None
    return paging_wrapper


@register_action('hlite')
@page_output
def highlight_watched(filename):
    ''' File contents highlighter '''
    from pygments import highlight
    from pygments.lexers import guess_lexer_for_filename
    from pygments.formatters import TerminalFormatter
    with open(filename, 'r') as file_to_read:
        content = file_to_read.read()
    content = highlight(content,
                        guess_lexer_for_filename(filename, ""),
                        TerminalFormatter(bg='dark'))
    return content


@register_action('rsthtml', is_firsttimer=True)
def view_rst_as_html(filename, first_time=False):
    ''' Function converting reStructuredText to HTML for display in browser '''
    import docutils.core
    htmlfile = '/tmp/%s.html' % os.path.basename(filename)
    if first_time:
        #TODO: use logging
        print('file://%s' % htmlfile)
    docutils.core.publish_file(source_path=filename, destination_path=htmlfile,
                               writer_name='html')


@register_action('rstman')
@page_output
def rst2man(filename):
    ''' Render rST-file as a manpage '''
    import docutils.core
    content = docutils.core.publish_file(source_path=filename,
                                         writer_name='manpage')
    nroffer = subprocess.Popen(NROFF_OPTS, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE)
    output, errors = nroffer.communicate(input=content)
    return output.decode('utf-8'
                                ).encode('latin1', errors='replace'
                                ).decode('utf-8', errors='replace')


def ino_watch(file_to_watch, action, action_args=[], action_kwargs={}):
    ''' ``inotify``-based watcher, applying function upon
        *write-and-close* events '''
    watcher = inotifyx.init()
    dirname = os.path.dirname(file_to_watch) or '.'
    basename = os.path.basename(file_to_watch)
    # we watch for CLOSE_WRITE events in directory and filter them by file name
    # because editors like vim do save&rename instead of simple modification
    inotifyx.add_watch(watcher, dirname, inotifyx.IN_CLOSE_WRITE)
    # wrap action to avoid code duplication
    action_lambda = lambda: action(file_to_watch, *action_args,
                                                  **action_kwargs)
    # run the first time
    action_lambda()
    while True:
        events = inotifyx.get_events(watcher)
        if basename in (ev.name for ev in events):
            action_lambda()


def main():
    ''' Mainloop function handling arguments and control flow '''
    usage = '''Usage: %prog [options] file_to_watch'''
    opt_parser = OptionParser(usage=usage)
    opt_parser.add_option("-a", "--action", dest="action",
                          help="action to be undertaken",
                          metavar="ACTION", default='hlite')
    (options, args) = opt_parser.parse_args()
    if len(args) > 1:
        #TODO: use logging
        print("How should I know what to watch from this list?\n"
              "Watching only first one, '%s'" % args[0])
        time.sleep(7)
    file_to_watch = args[0]
    action = implemented_actions.get(options.action)
    if not action:
        import sys
        #TODO: use logging
        sys.stderr.write("Unknown action: '%s'\n" % options.action)
        sys.exit(1)
    try:
        ino_watch(file_to_watch, action)
    except KeyboardInterrupt:
        #TODO: use logging
        print('\nCaught keyboard interrupt, exiting')


if __name__ == "__main__":
    main()
