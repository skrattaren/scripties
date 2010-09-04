#!/usr/bin/env python

import sys, urllib2

UNITS=(None, " Kb", " Mb", " Gb", " Tb")

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
    ui.setWindowTitle("GTF^H^HFS")
    ui.show()
    sys.exit(qtapp.exec_())

if __name__ == "__main__":
    url = sys.argv[1]
    size = main(url)
    qt_display(size)
