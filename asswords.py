#!/usr/bin/env python2

import argparse
import os
from versionedStorage import VersionedStorage
import ui

home = os.path.expanduser("~")
dbDir = os.path.join(home, ".asswords")

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
    db = VersionedStorage(dbDir, ui.readPassphrase())
    db.verifyMasterPassword()
    name = args.name
    password = ui.readPassword(name)
    db.setPassword(name, password)

def cmdDelete(args):
    idx = args.idx - 1
    db = VersionedStorage(dbDir, "dummypass")
    db.delete(idx)

def cmdPush(args):
    db = VersionedStorage(dbDir, "dummypass")
    db.push()

def cmdGet(args):
    db = VersionedStorage(dbDir, ui.readPassphrase())
    idx = args.idx - 1
    name = db.getNames()[idx]
    password = db.getPassword(idx)
    ui.displayPassword(name, password)

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
