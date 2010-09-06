#!/usr/bin/env python

from __future__ import print_function
import sys, urllib2

UNITS = (None, " Kb", " Mb", " Gb", " Tb")
WIN_TITLE = "File size"

def findout(num, step=0):
    if num < 1024 or step >= len(UNITS) - 1:
        return (num, step)
    else:
        return findout(int(num / 1024), step+1)

def main(url):
    rem_file = urllib2.urlopen(url)
    fdata = rem_file.info()
    size = int(fdata.getheader('content-length'))
    num, unit_no = findout(size)
    return str(num) + (UNITS[unit_no] or '')

def qt_display(size):
    from PyQt4 import QtGui
    qtapp = QtGui.QApplication(sys.argv)
    ui = QtGui.QMessageBox()
    ui.setText("Size: " + size)
    ui.resize(320, 240)
    ui.setWindowTitle(WIN_TITLE)
    ui.show()
    sys.exit(qtapp.exec_())

def gtk_display(size):
    import gtk
    dialog = gtk.MessageDialog(
        message_format="Size: %s" % size,
    )
    dialog.set_title(WIN_TITLE)
    dialog.connect('destroy', gtk.main_quit)
    dialog.show()
    gtk.main()

if __name__ == "__main__":
    selfname = sys.argv[0].split('/')[-1]
    if len(sys.argv) != 2:
        print("Script requires only one URL argument, see --help", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    try:
        size = main(url)
    except urllib2.URLError, exc:
        print(exc.args[0], file=sys.stderr)
        sys.exit(1)
    if selfname.startswith("qt"):
        qt_display(size)
    elif selfname.startswith("gtk"):
        gtk_display(size)
    else:
        print("Size: " + size)
        print("If you want a PyQt/PyGTK window, rename a script to")
        print("something starting with 'qt' or 'gtk', respectively")

