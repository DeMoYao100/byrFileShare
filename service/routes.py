import service
from flask import request, jsonify
from flask_login import logout_user, login_required, current_user
from flask import Blueprint
api = Blueprint('api', __name__)

# todo 继续写api文档里的其它接口，比如文件上传下载，文件夹创建删除，文件重命名等等
@api.route('/user/register', methods=['POST'])
def user_register():
    data = request.get_json()
    user_email = data.get('userEmail')
    user_password = data.get('userPassword')
    authcode = data.get('authCode')
    if not all([user_email,user_password,authcode]):
        return jsonify({'error': 'Missing required parameters'}), 400
    try:
        if service.register(user_email, user_password, authcode):
            return jsonify({'message': 'Register successful'}), 200
        else:
            return jsonify({'error': 'Register failed'}), 400
    except Exception:  # 替换为你想捕获的异常类型
        return jsonify({'error': 'An error occurred'}), 400

@api.route('/user/login', methods=['POST'])
def user_login():
    data = request.get_json()
    user_email = data.get('userEmail')
    user_password = data.get('userPassword')
    if not all([user_email,user_password]):
        return jsonify({'error': 'Missing required parameters'}), 400
    if service.pwd_login_verify(user_email,user_password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Login failed'}), 400

@api.route('/user/logout', methods=['POST'])
@login_required
def user_logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@api.route('/user/get/login', methods=['GET'])
def get_login_user():
    if current_user.is_authenticated:
        return jsonify(username=current_user.username, email=current_user.email), 200
    else:
        return jsonify({'error': 'User not found'}), 400