import curses
from getpass import getpass

def readPassphrase():
    return getpass("Master passphrase: ")

def getDialog(screen, title, height=3, contents=""):
    width = max(len(title) + 2, len(contents) + 2)
    sh, sw = screen.getmaxyx()
    x = int((sw - width) / 2)
    y = int((sh - height) / 2)
    dialog = screen
    x_offset = 0
    if (width < sw):
        x_offset = 1
        dialog = curses.newwin(height, width, y, x)
        dialog.box()
    dialog.addstr(0, x_offset, title)
    dialog.addstr(1, x_offset, contents)
    return dialog

def readPassword(name):
    screen = curses.initscr()
    try:
        dialog = getDialog(screen, "Enter password for %s:"%name, height=5)
        return dialog.getstr()
    finally:
        curses.endwin()

def displayPassword(name, password):
    screen = curses.initscr()
    try:
        dialog = getDialog(screen, name, contents=password)
        curses.noecho()
        dialog.getstr()
    finally:
        curses.endwin()
