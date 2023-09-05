import hashlib
import rsa

# 模拟CA的公钥
ca_public_key, _ = rsa.newkeys(2048)  # 实际中应该加载CA的真实公钥

# 验证证书并提取证书公钥
def verify_certificate(certificate, ca_public_key):
    # 将证书内容分行存储为列表
    certificate_lines = certificate.strip().split('\n')

    # 提取证书信息
    subject = certificate_lines[0].split(': ')[1]
    issuer = certificate_lines[1].split(': ')[1]
    issue_date = certificate_lines[2].split(': ')[1]
    expiration_date = certificate_lines[3].split(': ')[1]
    sha256_fingerprint = certificate_lines[4].split(': ')[1]
    rsa_signature = certificate_lines[5].split(': ')[1]

    # 构建证书信息字符串（除RSA签名部分）
    certificate_info = '\n'.join(certificate_lines[:-1])

    # 使用CA的公钥验证证书的签名
    try:
        rsa.verify(certificate_info.encode(), rsa_signature, ca_public_key)
        print("证书验证成功！")
        print("Subject:", subject)
        print("Issuer:", issuer)
        print("Issue Date:", issue_date)
        print("Expiration Date:", expiration_date)
        print("SHA256 Fingerprint:", sha256_fingerprint)

        # 提取证书公钥
        certificate_public_key = rsa.PublicKey.load_pkcs1(user_public_key.encode(), format='PEM')
        return certificate_public_key

    except rsa.pkcs1.VerificationError:
        print("证书验证失败！")
        return None

# 从文件加载证书
def load_certificate_from_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()

# 证书文件名
certificate_file_name = "alice_certificate.txt"

# 从文件加载证书
certificate = load_certificate_from_file(certificate_file_name)

# 验证证书并提取证书公钥
certificate_public_key = verify_certificate(certificate, ca_public_key)

# 如果验证成功，可以使用 certificate_public_key 进行后续操作
if certificate_public_key is not None:
    print("\n证书公钥信息:")
    print(certificate_public_key)
