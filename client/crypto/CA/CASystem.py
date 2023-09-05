import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.x509.oid import NameOID


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem


ca_private_pem, ca_public_pem = generate_key_pair()

# 将CA的密钥保存为文件
with open("ca_private_key.pem", "wb") as f:
    f.write(ca_private_pem)
with open("ca_public_key.pem", "wb") as f:
    f.write(ca_public_pem)


def create_csr(private_key, public_key, user_name):
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, user_name),
    ])
    csr = x509.CertificateSigningRequestBuilder().subject_name(
        subject
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("localhost")]),
        critical=False,
    ).sign(private_key, hashes.SHA256(), default_backend())
    return csr


# 生成用户的密钥对
user_private_pem, user_public_pem = generate_key_pair()

# 从PEM格式载入用户的私钥
user_private_key = serialization.load_pem_private_key(user_private_pem, password=None, backend=default_backend())

# 创建CSR
user_csr = create_csr(user_private_key, None, "Alice")


def issue_certificate(csr, ca_private_key, ca_public_key):
    issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "CA"),
    ])
    subject = csr.subject
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).sign(ca_private_key, hashes.SHA256(), default_backend())
    return cert


# 从PEM格式载入CA的私钥
ca_private_key = serialization.load_pem_private_key(ca_private_pem, password=None, backend=default_backend())

# 签发证书
user_cert = issue_certificate(user_csr, ca_private_key, None)

# 保存用户证书到PEM文件
with open("user_cert.pem", "wb") as f:
    f.write(user_cert.public_bytes(serialization.Encoding.PEM))

def verify_certificate(cert, ca_public_key):
    try:
        # 用CA的公钥验证证书
        ca_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        return True
    except Exception as e:
        print(f"证书验证失败: {e}")
        return False

# 验证证书
is_valid = verify_certificate(user_cert, ca_private_key.public_key())
print("证书有效" if is_valid else "证书无效")
