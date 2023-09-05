from cryptography.hazmat.backends import default_backend
import datetime
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


# 加载CA的公钥
def load_ca_public_key(public_key_file):
    with open(public_key_file, 'rb') as ca_public_key_file:
        ca_public_key = serialization.load_pem_public_key(ca_public_key_file.read(), backend=default_backend())
    return ca_public_key

# 验证数字证书的签名是否有效
def verify_certificate_signature(certificate, ca_public_key):
    certificate_lines = certificate.split('\n')
    signature = certificate_lines[5].split(': ')[1]
    certificate_info = '\n'.join(certificate_lines[:-2])
    signature = base64.b64decode(signature)
    print(signature)
    # 验证签名
    try:
        ca_public_key.verify(
            signature,
            certificate_info.encode(),
            padding.PKCS1v15(),  # 使用PKCS1v15填充方案，与签名时一致
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Signature verification failed: {str(e)}")
        return False

# 验证证书是否在有效期内
def verify_certificate_validity(certificate):
    certificate_lines = certificate.split('\n')
    issue_date_str = certificate_lines[2].split(': ')[1]
    expiration_date_str = certificate_lines[3].split(': ')[1]
    issue_date = datetime.datetime.strptime(issue_date_str, '%Y-%m-%d %H:%M:%S.%f')
    expiration_date = datetime.datetime.strptime(expiration_date_str, '%Y-%m-%d %H:%M:%S.%f')

    current_date = datetime.datetime.now()

    if issue_date <= current_date <= expiration_date:
        return True
    else:
        print("数字证书不在有效期内")
        return False

# 主程序
def main():
    ca_public_key = load_ca_public_key("ca_public_key.pem")

    # 从文件加载数字证书
    with open("alice_certificate.txt", 'r') as certificate_file:
        certificate = certificate_file.read()

    # 验证数字证书的签名和有效性
    if verify_certificate_signature(certificate, ca_public_key) and verify_certificate_validity(certificate):
        print("数字证书有效")
    else:
        print("数字证书无效")

if __name__ == "__main__":
    main()
