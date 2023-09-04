from flask import Flask, request, jsonify,send_from_directory
from conn import *
import json
import os
from layer_encrypt import *
from hashlib import md5


app = Flask(__name__)
fifo='./tmp'
file_id=''
UPLOAD_FOLDER='./download'
login=0
email=''
encrypted_bytes=None
U_dir='O:/'

'''
@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    message = data.get('message')
    # 处理消息
    response = {'response': '收到消息: {}'.format(message)}
    return jsonify(response)'''


app.route('/user/getLoginUser',methods=['POST'])
def get_login_user():
    return jsonify({'email':email}),200

app.route('/user/initlist',methods=['POST'])
def init_file_list():
    #从U盾初始化文件列表
    init_list=os.read(U_dir)
    init_list=[content for content in init_list if md5(email) not in content]
    init_list=[content.replace(".bin","") for content in init_list]
    return jsonify(init_list),200

app.route('/user/verifyCode',methods=['POST'])
def get_vercode():
    data=request.get_json()
    email=data.get('userEmail')
    send_data=jsonify({
    "op": "gen-authcode",
    "email": email
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    reply=json.loads(recv_message)
    if reply["status"]==200:
        return jsonify({'message':'verify code successfully sent'}), 200
    else:
        return jsonify({'message':'connection error'}),400
    
app.route('/user/loginPwd',methods=['POST'])
def loginPwd():
    data=request.get_json()
    email=data.get('userEmail')
    pwd=data.get('userPassword')
    if not all([email,pwd]):
        return jsonify({'error': 'Missing required parameters'}), 400
    send_data=jsonify({
    "op": "pwd-login",
    "email": email,
    "pwd": pwd
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    reply=json.loads(recv_message)
    if reply["status"]==200:
        login=1
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Login failed'}), 400
    
app.route('/user/loginEmail',methods=['POST'])
def loginVercode():
    data=request.get_json()
    email=data.get('userEmail')
    authcode=data.get('verify_code')
    if not all([email,authcode]):
        return jsonify({'error': 'Missing required parameters'}), 400
    send_data=jsonify({
    "op": "authcode-login",
    "email": email,
    "authcode": authcode
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    reply=json.loads(recv_message)
    if reply["status"]==200:
        login=1
        return jsonify({'message': 'Login successful'}),200
    else:
        return jsonify({'error': 'Login failed'}), 400
    
app.route('/user/forgetPwd',methods=['POST'])
def update_password():
    data=request.get_json()
    email=data.get('userEmail')
    pwd=data.get('userPassword')
    authcode=data.get('verify_code')
    if not all([email,authcode,pwd]):
        return jsonify({'error':'Missing required parameters'}),400
    send_data=jsonify({
    "op": "update-pwd",
    "email": email,
    "pwd": pwd,
    "authcode": authcode
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    reply=json.loads(recv_message)
    if reply["status"]==200:
        login=1
        return jsonify({'message': 'successfully changed password'}),200
    else:
        return jsonify({'error': 'failed to change password'}),400
    
app.route('/user/register', methods=['POST'])
def register():
    data=request.get_json()
    email=data.get('userEmail')
    pwd=data.get('userPassword')
    authcode=data.get('verify_code')
    if not all([email,pwd,authcode]):
        return jsonify({'error':'Missing required parameters'}),400
    send_data=jsonify({
    "op": "register",
    "email": email,
    "pwd": pwd,
    "authcode": authcode
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    reply=json.loads(recv_message)
    if reply["status"]==200:
        login=1
        return jsonify({'message': 'Register successful'}), 200
    else:
        return jsonify({'error': 'Register failed'}), 400
    
app.route('/user/filelist', methods=['POST'])
def get_file_list():
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')        #传邮箱或者群组的id
    path=data.get('path')           #传完整文件路径
    send_data=jsonify({
    "op": "get-dir-list",
    "id": id,
    "path": path
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    reply=json.loads(recv_message)
    if reply['status']==200:
        return jsonify(reply["list"]),200
        #返回list类型的文件列表
        '''
            "list": [
            {
                "name": "storage",
                "type": "dir",
                "size": null,
                "time": 1693707480
            },
            {
                "name": "README.md",
                "type": "file",
                "size": 14,
                "time": 1693567086
            }
        ]'''
    else:
        return jsonify({'error':'missing content'}),400

app.route('/user/uploadGetPath',methods=['POST'])
def upload_file_get_path():     #验证路径是否可用
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')       #传用户邮箱或群组id
    path=data.get('path')       #传服务器文件的完整路径
    send_data=jsonify({
    "op": "put-file",
    "id": id,
    "path": path
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv()
    reply=json.loads(recv_message)
    if reply['status']==200:
        if '@' in id:
            file_id=md5(id)
        else:
            file_id=id
        return jsonify({'message':'path available'}),200
    else:
        return jsonify({'error':'path already exist'}),400
    
app.route('/user/uplaodEncryptFile',methods=['POST'])
def upload_file_encrypt():
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    if 'fileInput' not in request.files:
        return jsonify({"error": "no file part"}) , 400
    file = request.files['fileInput']
    encrypted_bytes=layer_encrypt(file,file_id)
    if encrypted_bytes:
        return jsonify({'message':'file encrypted'}),200
    else:
        return jsonify({'error':'encrypt failed'}),400
    
app.route('/user/confirmUpload',methods=['POST'])
def start_upload_file():
    if login==0:
        return jsonify({'error':'need to login'}),400
    #data=request.get_json()
    connection.send(b'200')
    if connection.recv()==b'200' and encrypted_bytes!=None:
        connection.send(encrypted_bytes)
        recv_message=connection.recv().decode()
        result=json.loads(recv_message)
        if result['status']==200:
            return jsonify({'message':'successfully uploaded'}),200
        else:
            return jsonify({'error':'upload failed'}),400
        
app.route('/user/makedir',methods=['POST'])
def make_new_dir():
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')        #传用户的email或群组id
    path=data.get('path')
    send_data=jsonify({
    "op": "create-dir",
    "id": id,
    "path": path
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    result=json.loads(recv_message)
    if result['status']==200:
        return jsonify({'message':'successfully made new dir'}),200
    else:
        return jsonify({'error':'failed to make dir'}),400
    
app.route('/user/delete',methods=['POST'])
def delete_dir():
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')
    path=data.get('path')       #需要删除文件的服务器路径
    send_data=jsonify({
    "op": "del-dir",
    "id": id,
    "path": path
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    result=json.loads(recv_message)
    if result['status']==200:
        return jsonify({'message':'successfully deleted'}),200
    else:
        return jsonify({'error':'failed to delete dir'}),400
    
app.route('/user/download',methods=['POST'])
def download_file():        #从服务器下载文件
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')
    path=data.get('path')           #传需要下载的文件的服务器路径
    send_data=jsonify({
    "op": "get-file",
    "id": id,
    "path": path
    })
    recv_message=connection.recv_file(fifo)
    if recv_message:
        ############################
        #decrypt_file
        os.unlink(fifo)     #销毁管道
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True),200
    else:
        return jsonify({'error':'failed to download file'}),400
    
app.route('/user/joinGroup',methods=['POST'])
def join_group():
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('id')       #传目标用户组id
    send_data=jsonify({
    "op": "join-group",
    "id": id
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    result=json.loads(recv_message)
    if result['status']==200:
        return jsonify({'message':'joined group'}),200
    else:
        return jsonify({'error':'failed to join group'}),400


if __name__ == '__main__':
    login=0
    connection=ServerConn()
    app.run()
    
