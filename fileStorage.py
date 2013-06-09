import os
from codec import RowEncoder, SSE

class InvalidPassword(Exception):
    pass

class FileStorage:
    __SANITY_PHRASE = "-~=* EXCELLENT *=~-";

    def __init__(self, dataFile, password):
        self.dataFile = dataFile
        self.entryEncoder = RowEncoder(password)
        self.sanityEncoder = SSE(password)

        if not os.path.exists(self.dataFile):
            self.entries = []
            self.sane = True
            return
        # read entries
        lines_unclean = open(self.dataFile, "rb").read().split("\n")
        lines = filter(bool, lines_unclean)
        sanityCertificate, self.entries = lines[0], lines[1:]
        check = self.sanityEncoder.decrypt(sanityCertificate)
        self.sane = check == self.__SANITY_PHRASE
    
    def getNames(self):
        return map(self.entryEncoder.decodeName, self.entries)

    def getPassword(self, idx):
        if not self.sane:
            raise InvalidPassword()
        entry = self.entries[idx]
        return self.entryEncoder.decodePassword(entry)

    def setPassword(self, name, password):
        if not self.sane:
            raise InvalidPassword()
        newEntry = self.entryEncoder.encode(name, password)
        replaced = False
        for i in range(len(self.entries)):
            entry = self.entries[i]
            if self.entryEncoder.decodeName(entry) == name:
                self.entries[i] = newEntry
                replaced = True
                break
        if not replaced:
            self.entries.append(newEntry)
        self.persist()

    def delete(self, idx):
        if not self.sane:
            raise InvalidPassword()
        entry = self.entries.pop(idx)
        self.persist()
        return self.entryEncoder.decodeName(entry)

    def persist(self):
        tmpName = self.dataFile + ".temp"
        sanityCertificate = self.sanityEncoder.encrypt(self.__SANITY_PHRASE)
        w = open(tmpName, "wb")
        w.write(sanityCertificate + "\n")
        for entry in self.entries:
            w.write(entry + "\n")
        w.close()
        try:
            os.rename(tmpName, self.dataFile)
        except WindowsError:
            # atomic replace not as easy Windows
            os.remove(self.dataFile)
            os.rename(tmpName, self.dataFile)
