#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
 Script designed to display size of a remote file.
Accepts one argument, an URL of the file.
File size is displayed the way determined by script's own name
(prefix, precisely): name beginning with 'qt' yields  PyQt window,
beginning with 'gtk' - PyGTK one, otherwise size gets printed to stdout.
'''

from __future__ import print_function
import re, sys, urllib2

UNITS = (None, " Kb", " Mb", " Gb", " Tb")
WIN_TITLE = "File size"

def die(text):
    ''' Die with 1 return code on error'''
    print(text, file=sys.stderr)
    sys.exit(1)

def findout(num, step=0):
    ''' Finds the best unit and number to display size '''
    if num < 1024 or step >= len(UNITS) - 1:
        return (num, step)
    else:
        return findout(int(num / 1024), step+1)

def main(url):
    ''' Processes URL '''
    rem_file = urllib2.urlopen(url)
    fdata = rem_file.info()
    size = int(fdata.getheader('content-length'))
    num, unit_no = findout(size)
    return str(num) + (UNITS[unit_no] or '')

def qt_display(size):
    ''' Displays PyQt window with given data '''
    try:
        from PyQt4 import QtGui
    except ImportError:
        die("Required PyQt modules not found")
    qtapp = QtGui.QApplication(sys.argv)
    ui = QtGui.QMessageBox()
    ui.setText("Size: " + size)
    ui.resize(320, 240)
    ui.setWindowTitle(WIN_TITLE)
    ui.show()
    sys.exit(qtapp.exec_())

def gtk_display(size):
    ''' Displays PyGTK window with given data '''
    try:
        import gtk
    except ImportError:
        die("Required PyGTK modules not found")
    dialog = gtk.MessageDialog(
        message_format="Size: %s" % size,
    )
    dialog.set_title(WIN_TITLE)
    dialog.connect('destroy', gtk.main_quit)
    dialog.show()
    gtk.main()

if __name__ == "__main__":
    # process and handle args etc.
    selfname = sys.argv[0].split('/')[-1]

    if len(sys.argv) != 2:
        die("Script requires only one URL argument, see --help", file=sys.stderr)
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print("Rename a file for its name to begin with 'qt' to get a Qt interface")
        print("or with 'gtk' for a GTK one, and provide one URL argument")
        sys.exit(0)

    url = re.compile(r'((?:ht|f)tps?):/{1,2}').sub("\\1://", sys.argv[1])
    try:
        size = main(url)
    except urllib2.URLError, exc:
        die(exc.args[0])

    if selfname.startswith("qt"):
        qt_display(size)
    elif selfname.startswith("gtk"):
        gtk_display(size)
    else:
        print("Size: " + size)

