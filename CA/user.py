from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
import datetime

def generate_csr():
    # 用户信息
    user_info = {
        "organization_name": "bupt",
        "common_name": "AO",
    }

    # 生成用户的公钥和私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # 将私钥保存到文件
    with open("user_private_key.pem", "wb") as private_key_file:
        private_key_pem = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        )
        private_key_file.write(private_key_pem)

    # 生成CSR
    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(x509.NameOID.ORGANIZATION_NAME, user_info["organization_name"]),
        x509.NameAttribute(x509.NameOID.COMMON_NAME, user_info["common_name"]),
    ])).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(user_info["common_name"])]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())

    # 将CSR保存到文件
    with open("user_csr.pem", "wb") as csr_file:
        csr_pem = csr.public_bytes(Encoding.PEM)
        csr_file.write(csr_pem)

if __name__ == "__main__":
    generate_csr()
