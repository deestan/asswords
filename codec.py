from Crypto import Random
from Crypto.Cipher import AES
from hashlib import sha256

class RowEncoder:
    def __init__(self, passphrase):
        self.SEP = "\x80"
        self.sse = SSE(passphrase)
    
    def encode(self, name, password):
        n = name.encode("punycode")
        p = self.sse.encrypt(password)
        return n + self.SEP + p

    def decodeName(self, row):
        punyname = row.split(self.SEP)[0]
        return punyname.decode("punycode")

    def decodePassword(self, row):
        data = row.split(self.SEP)[1]
        return self.sse.decrypt(data)

class SSE:
    """ Salted Serializing Encrypter """
    def __init__(self, passphrase):
        self.SALT_SIZE = 2
        self.encrypter = Encrypter(passphrase)

    def encrypt(self, plaintext):
        salt = Random.get_random_bytes(self.SALT_SIZE)
        data = self.encrypter.encrypt(salt + plaintext)
        return data.encode("hex")

    def decrypt(self, ciphertext):
        raw = ciphertext.decode("hex")
        data = self.encrypter.decrypt(raw)
        return data[self.SALT_SIZE:]

class Encrypter:
    def __init__(self, passphrase):
        self.PAD_LENGTH = 32
        key = sha256(passphrase).digest()
        self.cipher = AES.new(key)

    def encrypt(self, plaintext):
        def _pad(text):
            p = self.PAD_LENGTH - (len(text) % self.PAD_LENGTH)
            pads = Random.get_random_bytes(p - 1)
            return text + pads + chr(p)
        padded = _pad(plaintext)
        return self.cipher.encrypt(padded)

    def decrypt(self, ciphertext):
        def _unpad(text):
            p = ord(text[-1])
            return text[:-p]
        padded = self.cipher.decrypt(ciphertext)
        return _unpad(padded)
