from cryptography.fernet import Fernet
import base64

key = Fernet.generate_key()
print(key)
crypter = Fernet(key)
with open('fernet_key.txt','wb') as f: 
    f.write(key)

with open('castle.jpg','rb') as f: 
    data = f.read()
with open('test.html','rb') as f:
    test = f.read()
    with open('enc_castle.jpg','wb') as f:
        cryp_data = crypter.encrypt(data)
        f.write(cryp_data)
    with open('enc_test.html','wb') as f:
        cryp_data = crypter.encrypt(test)
        f.write(cryp_data)
    
    print('> Encrypted')

# Decryption 

with open('fernet_key.txt','rb') as f: 
    key = f.read()
crypter = Fernet(key)

with open('enc_castle.jpg','rb') as f:
    data = f.read()
with open('dec_castle.jpg','wb') as f: 
    decrypt_data = crypter.decrypt(data)
    f.write(decrypt_data)

with open('enc_test.html','rb') as f:
    data = f.read()
with open('dec_test.html','wb') as f:
    decrypt_data = crypter.decrypt(data)
    f.write(decrypt_data)

print('> Decrypted')


