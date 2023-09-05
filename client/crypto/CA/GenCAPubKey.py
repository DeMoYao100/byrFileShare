from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# 从私钥文件中加载私钥
def load_private_key(private_key_file, password=None):
    with open(private_key_file, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=password,
            backend=default_backend()
        )
    return private_key

# 从私钥派生公钥
def derive_public_key(private_key):
    public_key = private_key.public_key()
    return public_key

# 将公钥序列化为PEM格式并保存到文件
def serialize_public_key_to_pem(public_key, file_path):
    with open(file_path, 'wb') as key_file:
        key_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

if __name__ == "__main__":
    # 加载CA的私钥
    ca_private_key_file = "ca_private_key.pem"
    ca_private_key = load_private_key(ca_private_key_file, password=None)

    # 派生公钥
    ca_public_key = derive_public_key(ca_private_key)

    # 将公钥保存到文件
    ca_public_key_file = "ca_public_key.pem"
    serialize_public_key_to_pem(ca_public_key, ca_public_key_file)

    print(f"CA公钥已保存到 {ca_public_key_file}")
