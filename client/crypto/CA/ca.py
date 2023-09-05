import jwt
import json
from datetime import datetime, timedelta

# CA密钥，实际中需要更安全的密钥管理
ca_secret_key = "ca_secret_key"

# CA生成的公钥，用于验证用户发送的CSR
ca_public_key = "ca_public_key"


def sign_certificate(csr, ca_key):
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


def main():
    while True:
        csr = input("Enter the CSR (in JSON format) from the user: ")

        # 验证用户发送的CSR
        try:
            decoded_csr = json.loads(csr)
        except json.JSONDecodeError:
            print("Invalid CSR format.")
            continue

        # 签署数字证书
        ca_signed_certificate = sign_certificate(decoded_csr, ca_secret_key)

        print("Certificate Signed by CA:")
        print(ca_signed_certificate)

        another = input("Do you want to sign another certificate? (yes/no): ")
        if another.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
