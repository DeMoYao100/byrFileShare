import hashlib
import rsa
import datetime

# 模拟用户目录，存储用户信息（用户名和公钥）
user_directory = {}

# 生成用户的公钥和私钥
def generate_key_pair():
    publicKey, privateKey = rsa.newkeys(2048)
    return publicKey, privateKey

# 创建CSR请求
def generate_csr(user_common_name, organization_name, user_public_key):
    csr = f"User Common Name: {user_common_name}\n"
    csr += f"Organization Name: {organization_name}\n"
    csr += f"User Public Key: {user_public_key}\n"
    return csr

# CA颁发数字证书
def issue_certificate(user_common_name, ca_name, user_public_key, private_key):
    certificate_info = f"Subject: {user_common_name}\n"
    certificate_info += f"Issuer: {ca_name}\n"
    certificate_info += f"Issue Date: {datetime.datetime.now()}\n"
    certificate_info += f"Expiration Date: {datetime.datetime.now() + datetime.timedelta(days=365)}\n"

    # 计算SHA256指纹
    sha256_fingerprint = hashlib.sha256(certificate_info.encode()).hexdigest()

    if private_key is not None:
        # 使用CA的私钥对证书信息进行签名
        signature = rsa.sign(certificate_info.encode(), private_key, 'SHA-256')
    else:
        signature = None

    certificate = f"{certificate_info}SHA-256 Fingerprint: {sha256_fingerprint}\n"
    certificate += f"RSA Signature: {signature}\n"

    return certificate

# 模拟CA接收CSR请求并处理
def process_csr(csr, ca_name):
    # 解析CSR，提取用户信息
    csr_lines = csr.split('\n')
    user_common_name = csr_lines[0].split(': ')[1]
    organization_name = csr_lines[1].split(': ')[1]
    user_public_key = csr_lines[2].split(': ')[1]

    # 查询用户目录，检查用户是否存在
    if user_common_name in user_directory:
        # 如果用户存在，更新数字证书
        user_public_key, user_private_key = generate_key_pair()
    else:
        # 如果用户不存在，生成数字证书
        user_directory[user_common_name] = user_public_key
        user_private_key = None  # 在实际情况下，应将私钥存储起来以供后续更新使用

    certificate = issue_certificate(user_common_name, ca_name, user_public_key, user_private_key)
    return certificate

# 模拟用户向CA申请证书的过程
def apply_for_certificate(user_common_name, organization_name, ca_name):
    user_public_key, user_private_key = generate_key_pair()
    csr = generate_csr(user_common_name, organization_name, user_public_key)
    certificate = process_csr(csr, ca_name)
    return csr, certificate

# 保存数字证书到文件
def save_certificate_to_file(certificate, file_name):
    with open(file_name, 'w') as file:
        file.write(certificate)

# 模拟CA接收CSR请求并颁发证书
ca_name = "MyCA"
user_common_name = "Alice"
organization_name = "ABC Corp"

csr, certificate = apply_for_certificate(user_common_name, organization_name, ca_name)

# 保存数字证书到文件
certificate_file_name = "alice_certificate.txt"
save_certificate_to_file(certificate, certificate_file_name)

# 打印CSR请求和证书文件名
print("CSR请求:")
print(csr)
print("\n数字证书已保存到文件:", certificate_file_name)
