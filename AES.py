from Crypto.Cipher import AES
from Crypto import Random

def encrypt_file(file_path, key):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(file_path, 'rb') as f:
        plaintext = f.read()

    padding_length = 16 - (len(plaintext) % 16)
    plaintext += bytes([padding_length]) * padding_length

    ciphertext = cipher.encrypt(plaintext)

    with open(file_path + ".enc", 'wb') as f:
        f.write(iv + ciphertext)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        iv_and_ciphertext = f.read()

    iv = iv_and_ciphertext[:16]
    ciphertext = iv_and_ciphertext[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)

    plaintext_with_padding = cipher.decrypt(ciphertext)

    padding_length = plaintext_with_padding[-1]
    plaintext = plaintext_with_padding[:-padding_length]

    with open(file_path[:-4] + ".dec", 'wb') as f:
        f.write(plaintext)


if __name__ == '__main__':
    key = b'This_is_an_example_key_for_demo!'
    if len(key) not in [16, 24, 32]:
        print("AES key must be either 16, 24, or 32 bytes long")
        exit(1)
    test_file = 'test.txt'

    encrypt_file(test_file, key)

    decrypt_file(test_file + ".enc", key)
