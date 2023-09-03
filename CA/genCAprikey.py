from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime

# 生成CA私钥
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# 保存CA私钥到文件
with open("ca_private_key.pem", "wb") as private_key_file:
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_file.write(private_key_pem)

# 构建自签名CA证书
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Example Corp"),
    x509.NameAttribute(NameOID.COMMON_NAME, "Example CA"),
])

builder = x509.CertificateBuilder().subject_name(
    subject
).issuer_name(
    issuer
).public_key(
    private_key.public_key()
).serial_number(
    x509.random_serial_number()
).not_valid_before(
    datetime.datetime.utcnow()
).not_valid_after(
    datetime.datetime.utcnow() + datetime.timedelta(days=365)
).add_extension(
    x509.BasicConstraints(ca=True, path_length=None),
    critical=True,
).add_extension(
    x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()),
    critical=False,
).add_extension(
    x509.AuthorityKeyIdentifier.from_issuer_public_key(private_key.public_key()),
    critical=False,
)

# 签名自签名CA证书
ca_certificate = builder.sign(
    private_key=private_key,
    algorithm=hashes.SHA256(),
    backend=default_backend()
)

# 保存自签名CA证书到文件
with open("ca_certificate.pem", "wb") as cert_file:
    cert_pem = ca_certificate.public_bytes(
        encoding=serialization.Encoding.PEM
    )
    cert_file.write(cert_pem)

print("自签名CA证书生成完成：ca_certificate.pem")
