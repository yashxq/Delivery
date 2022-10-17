from cryptography.fernet import Fernet 

class PassKeyDecrypter():
    def __init__(self):
        pass

    def decrypt_password(self):
        token_file = open("encrypt_key.txt","r")
        key = token_file.read()

        token_file = open("encrypt_cipher.txt","r")
        ciphered_text = token_file.read()

        cipher_suit = Fernet(key)

        uncipher_text = cipher_suit.decrypt(bytes(ciphered_text.encode('utf-8')))
        uncipher_text = str(uncipher_text,'utf-8')

        return uncipher_text

if __name__ == 'main':
    decypt_tool = PassKeyDecrypter()
    decrypt_tool.decrypt_password()
