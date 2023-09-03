import jwt
import json
import os
from datetime import datetime, timedelta

# CA公钥
ca_public_key = "ca_public_key"

# 指定目录来保存CSR和certificate
data_directory = "user_data"

# 创建目录（如果不存在）
os.makedirs(data_directory, exist_ok=True)


def generate_key_pair():
    # 在实际应用中，使用真正的密钥生成算法
    private_key = "user_private_key"
    public_key = "user_public_key"
    return private_key, public_key


def generate_csr(user_id, org_name, public_key):
    csr_data = {
        "user_id": user_id,
        "org_name": org_name,
        "public_key": public_key
    }

    # 保存CSR到指定目录
    csr_path = os.path.join(data_directory, user_id, "user-csr.json")
    with open(csr_path, "w") as csr_file:
        json.dump(csr_data, csr_file)

    return json.dumps(csr_data)


def create_jwt_certificate(csr, ca_key):
    # 在实际应用中，使用真正的数字证书签名算法
    certificate_data = {
        "subject": csr["user_id"],
        "issuer": "CA",
        "valid_from": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "valid_to": (datetime.utcnow() + timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S'),
        "fingerprint": "sha256_fingerprint",
        "signature": "rsa_signature"
    }

    return jwt.encode(certificate_data, ca_key, algorithm='HS256')


def save_data_to_file(user_id, private_key, certificate):
    user_directory = os.path.join(data_directory, user_id)
    os.makedirs(user_directory, exist_ok=True)

    private_key_path = os.path.join(user_directory, "private_key.pem")
    certificate_path = os.path.join(user_directory, "certificate.pem")

    with open(private_key_path, "w") as private_key_file:
        private_key_file.write(private_key)

    with open(certificate_path, "w") as certificate_file:
        certificate_file.write(certificate)


def main():
    while True:
        user_id = input("Enter your user ID: ")
        org_name = input("Enter your organization name: ")

        # 生成用户密钥对
        private_key, public_key = generate_key_pair()

        # 生成CSR
        csr = generate_csr(user_id, org_name, public_key)

        # 发送CSR给CA并接收数字证书
        ca_signed_certificate = create_jwt_certificate(json.loads(csr), ca_public_key)

        # 保存私钥和数字证书到指定目录
        save_data_to_file(user_id, private_key, ca_signed_certificate)

        print("User Key Pair Generated.")
        print("CSR Generated and Saved.")
        print("Certificate Created by CA and Saved.")

        another = input("Do you want to request another certificate? (yes/no): ")
        if another.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
