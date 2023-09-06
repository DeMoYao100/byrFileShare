from flask import Flask, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
import service
from flask import request, jsonify
from flask_login import logout_user, login_required, login_user, current_user
from flask_session import Session
from model import *

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your-secret-key'
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

#todo 找回密码逻辑
@app.route('/user/verifyCode', methods=['POST'])
def get_ver_code():
    data = request.get_json()
    user_email = data.get('userEmail')
    result = service.gen_authcode(user_email)
    if result:
        return jsonify({'message': 'verify code successfully sent'}), 200
    else:
        return jsonify({'error': 'failed to send verify code'}), 400


@app.route('/user/register', methods=['POST'])
def user_register():
    data = request.get_json()
    user_email = data.get('userEmail')
    user_password = data.get('userPassword')
    authcode = data.get('authCode')
    print(user_email, user_password, authcode)
    if not all([user_email, user_password, authcode]):
        return jsonify({'error': 'Missing required parameters'}), 400
    try:
        if service.register(user_email, user_password, authcode):
            return jsonify({'message': 'Register successful'}), 200
        else:
            return jsonify({'error': 'Register failed'}), 400
    except Exception:  # 替换为你想捕获的异常类型
        return jsonify({'error': 'An error occurred'}), 400


@app.route('/user/loginPwd', methods=['POST'])
def user_login_pwd():
    data = request.get_json()
    user_email = data.get('userEmail')
    user_password = data.get('userPassword')
    print("flask层收到:", user_email, user_password)
    if not all([user_email, user_password]):
        return jsonify({'error': 'Missing required parameters'}), 400
    if service.pwd_login_verify(user_email, user_password):
        user = User(user_email)
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Login failed'}), 400

@app.route('/user/loginEmail', methods=['POST'])
def user_login_email():
    data = request.get_json()
    user_email = data.get('userEmail')
    ver_code = data.get('verify_code')
    if not all([user_email, ver_code]):
        return jsonify({'error': 'Missing required parameters'}), 400
    if service.authcode_login_verify(user_email, ver_code):
        user = User(user_email)
        user.authenticate()
        login_user(user)
        print("*",current_user.email)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Login failed'}), 400


@app.route('/user/forgetPwd', methods=['POST'])
def user_forget_email():
    data = request.get_json()
    user_email = data.get('userEmail')
    ver_code = data.get('verify_code')
    new_pwd = data.get('userPassword')  # 传需要改的新口令
    if not all([user_email, ver_code, new_pwd]):
        return jsonify({'error': 'Missing required parameters'}), 400
    if service.update_pwd(user_email, new_pwd, ver_code):
        return jsonify({'message': 'successfully changed password'}), 200
    else:
        return jsonify({'error': 'failed to change password'}), 400


@app.route('/user/logout', methods=['POST'])
@login_required
def user_logout():
    current_user.is_authenticated = False
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/user/get/login', methods=['POST'])
def get_login_user():
    if current_user.is_authenticated:
        return jsonify(email=current_user.email), 200
    else:
        return jsonify({'error': 'User not login'}), 400


@app.route('/user/filelist', methods=['POST'])
@login_required
def get_user_file_list():
    data = request.get_json()
    path = data.get('path')  # 传入所需要取出的文件夹完整路径，如111/414124，为文件路径
    content = service.get_dir_list(current_user.email, path)
    if content:
        return jsonify(content), 200  # 如果成功就返回文件列表,content为一个二元元组，个数为([],[]),其中第一个list内的为文件夹，第二个list内的为文件
    else:
        return jsonify({'error': 'missing content'}), 400


@app.route('/user/download', methods=['POST'])
@login_required
def download_file():
    data = request.get_json()
    path = data.get('path')  # 需要下载的文件的完整路径
    content = service.get_file(current_user.email, path)  # 如果成功就直接返回文件，为bytes形式
    if content:
        return jsonify(content), 200
    else:
        return jsonify({'error': 'missing content'}), 400


@app.route('/user/upload', methods=['POST'])
@login_required
def upload_file():
    data = request.get_json()
    path = data.get('path')  # 需要上传的文件的完整路径
    file = data.get('file')  # 需要上传的文件，bytes形式
    result = service.put_file(current_user.email, path, file)
    if result == FileOpStatus.Ok:
        return jsonify({'message': 'successfully uploaded'}), 200
    else:
        return jsonify({'error': 'file already exist'}), 400


@app.route('/user/delete', methods=['POST'])
@login_required
def delete_target():
    data = request.get_json()
    path = data.get('path')  # 需要删除的文件/文件夹的完整路径
    result = service.del_dir(current_user.email, path)
    if result == FileOpStatus.Ok:
        return jsonify({'message': 'successfully deleted'}), 200
    else:
        return jsonify({'error': 'targeted dir not exist'}), 400


@app.route('/user/makedir', methods=['POST'])
@login_required
def make_new_dir():
    data = request.get_json()
    path = data.get('path')
    result = service.create_dir(current_user.email, path)
    if result == FileOpStatus.Ok:
        return jsonify({'message': 'dir created'}), 200
    else:
        return jsonify({'error': 'dir already exist'}), 400


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=5001)
