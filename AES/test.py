from flask import Flask, request, jsonify, render_template, send_from_directory
import os

from Crypto.Cipher import AES
from Crypto import Random

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('./test.html')

UPLOAD_FOLDER = 'E:\\大三上\\小学期\\加密\\AES\\download' #test

@app.route('/',methods = ['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return jsonify({"error": "no file part"}) , 400
    file = request.files['fileInput']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = file.filename
        file_path = os.path.join('uploads', filename)
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        file.save(file_path)

# 测试解密代码：
    # def decrypt_file(file_path, key):
    #     with open(file_path, 'rb') as f:
    #         iv_and_ciphertext = f.read()

    #     iv = request.files['iv'].read()
    #     ciphertext = iv_and_ciphertext

    #     cipher = AES.new(key, AES.MODE_CBC, iv)

    #     plaintext_with_padding = cipher.decrypt(ciphertext)

    #     padding_length = plaintext_with_padding[-1]
    #     plaintext = plaintext_with_padding[:-padding_length]

    #     with open(file_path[:-4] + ".dec", 'wb') as f:
    #         f.write(plaintext)

    # decrypt_file(file_path,b'This_is_an_example_key_for_demo!')
    return jsonify({"message": f"File {filename} has been uploaded successfully!"}), 200

@app.route('/download',methods = ['GET'])
def download_index():
    return render_template('./download.html')


@app.route('/download/<filename>',methods = ['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    