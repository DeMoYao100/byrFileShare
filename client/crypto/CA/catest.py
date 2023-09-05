import jwt
import json
import os
from datetime import datetime, timedelta

# CA密钥，实际中需要更安全的密钥管理
ca_secret_key = "ca_secret_key"

# CA生成的公钥，用于验证用户发送的CSR
ca_public_key = "ca_public_key"

# 指定目录来保存CSR和certificate
data_directory = "ca_data"

# 创建目录（如果不存在）
os.makedirs(data_directory, exist_ok=True)


def create_jwt_certificate(csr, ca_key):
    # 在实际应用中，使用真正的数字证书签名算法
    certificate_data = {
        "subject": csr["user_id"],
        "issuer": "CA",
        "valid_from": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "valid_to": (datetime.utcnow() + timedelta(days=912)).strftime('%Y-%m-%d %H:%M:%S'),
        "fingerprint": "sha256_fingerprint",
        "signature": "rsa_signature"
    }

    return jwt.encode(certificate_data, ca_key, algorithm='HS256')


def save_certificate_to_file(user_id, certificate):
    user_directory = os.path.join(data_directory, user_id)
    os.makedirs(user_directory, exist_ok=True)

    certificate_path = os.path.join(user_directory, "certificate.pem")

    with open(certificate_path, "w") as certificate_file:
        certificate_file.write(certificate)


def main(csr_file_path):
    with open(csr_file_path, "r") as csr_file:
        csr_data = json.load(csr_file)

    # 验证用户发送的CSR

    # 签署数字证书
    ca_signed_certificate = create_jwt_certificate(csr_data, ca_secret_key)

    # 保存数字证书到指定目录
    save_certificate_to_file(csr_data["user_id"], ca_signed_certificate)

    print("Certificate Created by CA and Saved.")


if __name__ == "__main__":
    csr_file_path = "user_data/gbg/user-csr.json"  # 指定CSR文件路径
    main(csr_file_path)
