from flask import Flask, request, jsonify, render_template
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

app = Flask(__name__)
def init_CA():
    with open("../pem/ca_certificate.pem", "rb") as ca_cert_file:
        ca_cert = x509.load_pem_x509_certificate(
            ca_cert_file.read(),
            default_backend()
        )
    return ca_cert

@app.route('/',methods = ['GET'])
def index():
    return render_template('./test.html')

@app.route('/api/send_CA', methods = ['GET'])
def send():
    ca = init_CA()
    data = {
        "CA" : ca
        # 这里补充公钥等等信息
    }
    
    return jsonify(ca)
    

if __name__ == '__main__':
    app.run(debug = True)