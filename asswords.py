#!/usr/bin/env python2

import curses
import argparse
import os
from getpass import getpass
from versionedStorage import VersionedStorage

home = os.path.expanduser("~")
dbDir = os.path.join(home, ".asswords")
db = None # set after arg parse

def readPassphrase(query="Master passphrase: "):
    return getpass(query)

def displayPassword(screen, password):
    title = "PRESS ENTER WHEN DONE"
    width = max(len(title) + 4, len(password) + 2)
    sh, sw = screen.getmaxyx()
    x = int((sw - width) / 2)
    y = int((sh - 1) / 2)
    dialog = screen
    x_offset = 0
    if (width < sw):
        x_goffset = 1
        dialog = curses.newwin(3, width, y, x)
        dialog.box()
    dialog.addstr(0, x_offset + 1, title)
    dialog.addstr(1, x_offset + 0, password)
    curses.noecho()
    dialog.getstr()
    
def cmdList(args):
    db = VersionedStorage(dbDir, "dummypass")
    names = db.getNames()
    if not names:
        print "No entries yet."
        return
    print "Entries:"
    for x in range(len(names)):
        print " %d %s"%(x+1, names[x])

def cmdAdd(args):
    db = VersionedStorage(dbDir, readPassphrase())
    name = args.name
    password = readPassphrase("Password for %s: "%name)
    db.setPassword(name, password)

def cmdDelete(args):
    idx = args.idx - 1
    db.deletePassword(idx)

def cmdPush(args):
    db.push()

def cmdGet(args):
    db = VersionedStorage(dbDir, readPassphrase())
    idx = args.idx - 1
    password = db.getPassword(idx)
    screen = curses.initscr()
    try:
        displayPassword(screen, password)
    finally:
        curses.endwin()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help="Commands:")

parser_list = subparsers.add_parser("list", help="List all entry names.")
parser_list.set_defaults(func=cmdList)

parser_add = subparsers.add_parser("add", help="Add new entry.")
parser_add.add_argument("name", type=str, help="entry name, e.g. 'Facebook'")
parser_add.set_defaults(func=cmdAdd)

parser_get = subparsers.add_parser(
    "get",
    help="Read a password entry.  The password will be temporarily written to the terminal."
    )
parser_get.add_argument("idx", type=int, help="entry index number in list, e.g. '4'")
parser_get.set_defaults(func=cmdGet)

parser_delete = subparsers.add_parser("delete", help="Delete entry.")
parser_delete.add_argument("idx", type=int, help="entry index number in list, e.g. '4'")
parser_delete.set_defaults(func=cmdDelete)

parser_push = subparsers.add_parser(
    "push",
    help="Push changes to server.  This is normally attempted automatically on 'add' and 'delete', but will need to be done manually if the automatic push failed (e.g. no network connection)."
    )
parser_push.set_defaults(func=cmdPush)

args = parser.parse_args()
args.func(args)
