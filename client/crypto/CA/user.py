import jwt
import json
from datetime import datetime, timedelta

# CA公钥
ca_public_key = "ca_public_key"

# 用户数据存储
user_data = {}


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
    return json.dumps(csr_data)


def create_jwt_token(data, secret_key):
    return jwt.encode(data, secret_key, algorithm='HS256')


def main():
    while True:
        user_id = input("Enter your user ID: ")
        org_name = input("Enter your organization name: ")

        # 生成用户密钥对
        private_key, public_key = generate_key_pair()

        # 生成CSR
        csr = generate_csr(user_id, org_name, public_key)

        # 发送CSR给CA并接收数字证书
        ca_signed_certificate = input("Enter the CA-signed certificate: ")

        # 验证CA签名
        try:
            decoded_csr = jwt.decode(ca_signed_certificate, ca_public_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print("Certificate has expired.")
            continue
        except jwt.DecodeError:
            print("Certificate signature verification failed.")
            continue

        # 用户保存私钥和数字证书
        user_data[user_id] = {
            "private_key": private_key,
            "certificate": decoded_csr
        }

        print("User Key Pair Generated.")
        print("CSR Generated.")
        print("Certificate Verified and Saved.")

        another = input("Do you want to request another certificate? (yes/no): ")
        if another.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
