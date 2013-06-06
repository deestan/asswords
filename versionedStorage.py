import os
from subprocess import check_call, call
from fileStorage import FileStorage

DBFILE = "passwords"

class VersionedStorage:
    def __init__(self, dbDir, password):
        self.dbDir = dbDir
        dbPath = os.path.join(dbDir, DBFILE)
        if not os.path.isdir(dbDir):
            raise Exception("Data folder not found: " + dbDir)
        self.pull()
        self.fs = FileStorage(dbPath, password)

    def getNames(self):
        return self.fs.getNames()

    def setPassword(self, name, password):
        self.fs.setPassword(name, password)
        self.commit("Added or updated entry %s"%name)

    def getPassword(self, idx):
        return self.fs.getPassword(idx)

    def delete(self, idx):
        name = self.fs.delete(idx)
        self.commit("Deleted entry %s"%name)

    def pull(self):
        call([ "git", "pull", "-q", "--strategy=ours", "origin", "master" ], cwd=self.dbDir)

    def push(self):
        self.commit("Pushing offline changes.")

    def commit(self, what):
        check_call([ "git", "add", DBFILE ], cwd=self.dbDir)
        check_call([ "git", "commit", "-m", what ], cwd=self.dbDir)
        call([ "git", "push", "-q", "origin", "master" ], cwd=self.dbDir)
