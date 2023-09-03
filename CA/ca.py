from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
from user import generate_csr  # 导入用户的生成CSR函数

def extract_client_identity(csr):
    subject = csr.subject
    common_name = None
    for attribute in subject:
        if attribute.oid == x509.NameOID.COMMON_NAME:
            common_name = attribute.value
            break
    return common_name

def query_user_directory(common_name):

    if common_name in user_directory:
        return user_directory[common_name]
    return None

# 加载CA的私钥和证书
with open("ca_private_key.pem", "rb") as ca_private_key_file:
    ca_private_key = serialization.load_pem_private_key(
        ca_private_key_file.read(),
        password=None,  # 如果私钥有密码，需要提供密码
        backend=default_backend()
    )

with open("ca_certificate.pem", "rb") as ca_cert_file:
    ca_cert = x509.load_pem_x509_certificate(
        ca_cert_file.read(),
        default_backend()
    )

# CA处理CSR，生成数字证书
def sign_csr(csr):
    if ca_private_key is None or ca_cert is None:
        raise ValueError("CA私钥和证书未设置")

    issuer_name = ca_cert.subject
    builder = x509.CertificateBuilder().subject_name(csr.subject)
    builder = builder.issuer_name(issuer_name)
    builder = builder.not_valid_before(datetime.datetime.utcnow())
    builder = builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=730))  # 有效期2年
    builder = builder.public_key(csr.public_key())
    builder = builder.serial_number(x509.random_serial_number())

    # 添加扩展，例如SHA-256指纹
    builder = builder.add_extension(
        x509.SubjectKeyIdentifier.from_public_key(csr.public_key()),
        critical=False,
    )
    builder = builder.add_extension(
        x509.AuthorityKeyIdentifier.from_issuer_public_key(ca_private_key.public_key()),  # 修复此处
        critical=False,
    )

    # 使用CA的私钥对CSR进行签名
    certificate = builder.sign(
        private_key=ca_private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend()
    )

    return certificate

if __name__ == "__main__":
    # 模拟的用户目录
    user_directory = {
        "user1": {"common_name": "AO", "email": "user1@example.com"},
        "user2": {"common_name": "用户二", "email": "user2@example.com"},
    }
    # 生成用户的CSR
    generate_csr()

    # 从文件中加载CSR
    with open("user_csr.pem", "rb") as csr_file:
        csr = x509.load_pem_x509_csr(csr_file.read(), default_backend())

    # 从CSR中提取客户身份信息
    common_name = extract_client_identity(csr)

    if common_name:
        # 查询用户目录
        user_info = query_user_directory(common_name)

        if user_info:
            # 用户存在，更新数字证书
            user_certificate = sign_csr(csr)

            # 将更新后的证书保存到文件
            with open("user_certificate.pem", "wb") as cert_file:
                cert_pem = user_certificate.public_bytes(serialization.Encoding.PEM)
                cert_file.write(cert_pem)
            print(f"已更新{common_name}的数字证书。")
        else:
            # 用户不存在，生成数字证书
            user_certificate = sign_csr(csr)

            # 将数字证书保存到文件
            with open("user_certificate.pem", "wb") as cert_file:
                cert_pem = user_certificate.public_bytes(serialization.Encoding.PEM)
                cert_file.write(cert_pem)
            print(f"已为{common_name}生成数字证书。")
    else:
        print("无法从CSR中提取客户身份信息。")
