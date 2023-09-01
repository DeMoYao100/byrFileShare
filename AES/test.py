from flask import Flask, request, jsonify, render_template
import os

from Crypto.Cipher import AES
from Crypto import Random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('./test.html')

@app.route('/',methods = ['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return jsonify({"error": "no file part"}) , 400
    file = request.files['fileInput']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 保存文件
    if file:
        filename = file.filename
        file_path = os.path.join('uploads', filename)

        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        file.save(file_path)

# 测试解密代码：
    def decrypt_file(file_path, key):
        with open(file_path, 'rb') as f:
            iv_and_ciphertext = f.read()

        iv = request.files['iv'].read()
        ciphertext = iv_and_ciphertext

        cipher = AES.new(key, AES.MODE_CBC, iv)

        plaintext_with_padding = cipher.decrypt(ciphertext)

        padding_length = plaintext_with_padding[-1]
        plaintext = plaintext_with_padding[:-padding_length]

        with open(file_path[:-4] + ".dec", 'wb') as f:
            f.write(plaintext)

    decrypt_file(file_path,b'This_is_an_example_key_for_demo!')
    return jsonify({"message": f"File {filename} has been uploaded successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
    
