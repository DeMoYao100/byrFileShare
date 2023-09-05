import datetime
from cryptography import x509

def load_certificate_file(file_name):
    try:
        with open(file_name, 'r') as file:
            certificate = file.read()
        return certificate
    except FileNotFoundError:
        print(f"文件 {file_name} 未找到")
        return None
    except IOError:
        print("文件读取错误")
        return None


def verify_certificate(ca, ca_public_key):
    # 验证用户证书
    try:
        ca_public_key.verify(
            ca.signature,
            ca.tbs_certificate_bytes,
            x509.signature.SignatureAlgorithm.from_hazmat_signature_algorithm(ca.signature_hash_algorithm),
            x509.signature.Encoding.DER
        )
        print("证书验证成功")
        return True
    except Exception as e:
        print(f"证书验证失败: {e}")
        return False
