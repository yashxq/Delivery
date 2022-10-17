from secrets import token_bytes
from cryptography.fernet import Fernet
import getpass

class KeyGen():

    def __init__(self):
        pass

    def encrypt_password(self):
        try:
            password = getpass.getpass()
        except Exception as e:
            print("Error",e)
        else:
            print('Token and Cipher Generated')

        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(bytes(password.encode('utf-8')))

        token_file = open("encrypt_key.txt","w+")
        token_file.write(str(key,'utf-8'))
        token_file.close()

        token_file = open("encrypt_cipher.txt","w+")
        token_file.write(str(ciphered_text,'utf-8'))
        token_file.close()


tool = KeyGen()
tool.encrypt_password()
