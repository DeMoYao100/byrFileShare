from flask import Flask, request, jsonify,send_from_directory
from conn import *
import json
import os
from cry.LayerEncrypt import *
from cry.LayerDecrypt import *
from hashlib import md5
import platform
import subprocess
from flask_cors import CORS
from time import sleep
from cry.GenerateMainKey import *

app = Flask(__name__)
CORS(app)
fifo='./tmp'        #fifo pipe文件存储的目录
file_id=''            #传文件到服务器时用的id
UPLOAD_FOLDER='./download/'        #下载文件时用的文件夹

login=0                           #记录用户是否登录，登录后为1，否则为0
email=''                          #保存用户邮箱
U_dir='O:/'                       #U盾的目录
encrypted_bytes=None              #上传文件时加密后转为bytes的文件数据
connection=ServerConn()
sleep(1)


'''
@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    message = data.get('message')
    # 处理消息
    response = {'response': '收到消息: {}'.format(message)}
    return jsonify(response)'''

@app.route('/user/getLoginUser',methods=['POST'])
def get_login_user():
    #print(login)
    global login
    global email
    global connection
    #用于返回登录后用户的邮箱
    if login==0:
        return jsonify({'error':'need to login'}),400
    print("getLoginUser:",email)
    return jsonify({'email':email}),200

@app.route('/user/initlist',methods=['POST'])
def init_file_list():
    #从U盾初始化群组列表
    global connection
    init_list=os.read(U_dir)
    init_list=[content for content in init_list if md5(email) not in content]
    init_list=[content.replace(".bin","") for content in init_list]
    return jsonify(init_list),200

@app.route('/user/verifyCode',methods=['POST'])
def get_vercode():
    #得到验证码
    from flask_cors import CORS
    global login
    global email
    global connection
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
    
@app.route('/user/loginPwd',methods=['POST'])
def loginPwd():
    #使用密码登录
    global login
    global email
    global connection
    data=request.get_json()
    # print('login : ',data)
    email=data.get('userEmail')
    pwd=data.get('userPassword')
    if not all([email,pwd]):
        return jsonify({'error': 'Missing required parameters'}), 400
    send_data=jsonify({
        "op": "pwd-login",
        "email": email,
        "pwd": pwd
    })
    # print(send_data.get_data())
    connection.send(send_data.get_data())
    sleep(0.2)
    recv_message = connection.recv().decode()
    print(" 1 : ",recv_message)
    reply=json.loads(recv_message)
    if reply["status"] == 200:
        login = 1
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Login failed'}), 400
    
@app.route('/user/loginEmail',methods=['POST'])
def loginVercode():
    global login
    global email
    global connection
    #验证码登录
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
    
@app.route('/user/forgetPwd',methods=['POST'])
def update_password():
    #忘记密码
    global login
    global email
    global connection
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
    
@app.route('/user/register', methods=['POST'])
def register():
    #注册
    global login
    global email
    global connection
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
        print(login)
        user_id=generate_personal_key_id(email)
        layer_encrypt(None,user_id)
        return jsonify({'message': 'Register successful'}), 200
    else:
        return jsonify({'error': 'Register failed'}), 400
    
@app.route('/user/filelist', methods=['POST'])
def get_file_list():
    #返回文件列表
    global login
    global email
    global connection
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')        #传邮箱或者群组的id
    print("fileList:userEmaio",id)
    path=data.get('path')           #传完整文件路径
    send_data=jsonify({
    "op": "get-dir-list",
    "id": id,
    "path": path
    })
    connection.send(send_data.get_data())
    sleep(0.1)
    recv_message=connection.recv().decode()
    # print('5 : recv_message=connection.recv().decode() : ',recv_message)
    print("get_file_list函数中，发送的数据：",send_data)
    reply=json.loads(recv_message)
    print("get_file_list函数中，接收的数据：",reply)
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

@app.route('/user/uploadGetPath',methods=['POST'])
def upload_file_get_path():     
    #验证路径是否可用
    global login
    global email
    global file_id
    global connection
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')       #传用户邮箱或群组id
    path=data.get('path')       #传服务器文件的完整路径，包括文件名

    send_data=jsonify({
    "op": "put-file",
    "id": id,
    "path": path
    })
    connection.send(send_data.get_data())
    recv_message=connection.recv()
    reply=json.loads(recv_message)
    if reply==200:
        if '@' in id:
            MD_5 = hashlib.md5()
            MD_5.update("hello".encode('utf-8'))
            file_id=MD_5.hexdigest()
            print("file_id:",file_id)
        else:
            file_id=id
        return jsonify({'message':'path available'}),200
    else:
        return jsonify({'error':'path already exist'}),400
    
@app.route('/user/uploadEncryptFile',methods=['POST'])
def upload_file_encrypt():
    #对需要上传的文件进行本地加密
    global login
    global email
    global file_id
    global connection
    global encrypted_bytes
    if login==0:
        return jsonify({'error':'need to login'}),400
    # data=request.get_json()
    if 'fileInput' not in request.files:
        print("uploadEncryptFile: no file part")
        print("uploadEncryptFile: request.files",request.files)
        return jsonify({"error": "no file part"}) , 400
    file = request.files['fileInput']
    print("uploadEncryptFile: file",file)
    print("uploadEncryptFile: type(file)", type(file))
    encrypted_bytes=layer_encrypt(file.read(),file_id)
    if encrypted_bytes:
        return jsonify({'message':'file encrypted'}),200
    else:
        return jsonify({'error':'encrypt failed'}),400
    
@app.route('/user/confirmUpload',methods=['POST'])
def start_upload_file():
    #上传文件
    global login
    global email
    global encrypted_bytes
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
        
@app.route('/user/makedir',methods=['POST'])
def make_new_dir():
    #新开目录
    global login
    global email
    global connection
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
    
@app.route('/user/delete',methods=['POST'])
def delete_dir():
    #删除文件夹/文件
    global login
    global email
    global connection
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
    
# app.route('/user/download',methods=['POST'])
# def download_file():        #从服务器下载文件
#     if login==0:
#         return jsonify({'error':'need to login'}),400
#     data=request.get_json()
#     id=data.get('userEmail')
#     path=data.get('path')           #传需要下载的文件的服务器路径
#     send_data=jsonify({
#     "op": "get-file",
#     "id": id,
#     "path": path
#     })
#     recv_message=connection.recv_file(fifo)
#     if recv_message:
#         ############################
#         #decrypt_file
#         os.unlink(fifo)     #销毁管道
#         return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True),200
#     else:
#         return jsonify({'error':'failed to download file'}),400

# ----------
# 切成两个路由，方便前端

'''
# 获取可以下载的文件列表
#可下载的文件列表放在找用户列表里了

@app.route('/user/download',methods = ['POST'])
def init_download():
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id=data.get('userEmail')
    path=data.get('path')
    send_data=jsonify({        #源代码这里的send_data得发出去但是好像没有， 你们看看对着server是咋发的数据
        "op": "get-file-list", #这里先获取一次list
        "id": id,
        "path": path
    })
    connection.send(send_data)
    data = connection.recv().decode()
    # todo : 这里需要添加一个申请网盘文件列表并且转化为前端 ，等一下前端要的格式, 暂时先把file_list上传 ，server要多给一个list
    return data.get('file_list')'''

filedata = []

#@app.route('/user/download/<filename>', methods = ['GET'])
#def download_file(filename):

@app.route('/user/download',methods=['POST'])
def download_file():
    #下载指定的文件
    # 这里不需要再次鉴权，因为这里是上面鉴权后才能获取文件
    global login
    global email
    global connection
    global fifo
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    print(" 6 : ", data)
    id=data.get('userEmail')
    filename=data.get('path')
    send_data=jsonify({ # 同理这里需要把send_data发出去
    "op": "get-file",
    "id": id,        # id 我不知道是啥，但是感觉可以删掉的，这里不用鉴权
    "path": filename    #这个filename得是完整的路径
    })
    connection.send(send_data.get_data())
    '''
    print(" 7 : ", send_data.get_data())
    if not os.path.exists(fifo):
        # print("12 : file create success")
        os.mkfifo(fifo)
    else :
        print("12 : file exist")
    _ = connection.recv_file(fifo)
    sleep(0.1)
    
    with open(fifo,"rb") as file:
        recv_message=file.read()
        os.unlink(fifo)
    print(" 10 : ",recv_message)'''
    recv_message=connection.recv()
    print('rcvd file', len(recv_message))
    print("fifo:",fifo)
    with open(fifo ,'wb') as f:
        f.write(recv_message)
    # todo: 解密文件 ，存在recv_message就行
    file = UPLOAD_FOLDER + filename.split('/')[-1]
    # with open(file, "wb") as wfile:
    #     wfile.write(recv_message)
    decrypted_info=layer_decrypt(fifo)
    #decrypted_info = recv_message
    with open(file,"wb") as f:
        f.write(decrypted_info)
    '''
    # 跨平台返回文件
    if platform.system() == "Windows":
        os.startfile(file)
    elif (platform.system() == "Darwin"):
        subprocess.run(["open", file])'''
    return jsonify({'status':'success'}), 200

# @app.route('/user/delete/<filename>', methods = ['POST'])
# def delete_file(filename):
#     if (not filedata.index(filename)):
#         return jsonify({"show":"file not exist"}), 400 #这里前端可以直接提取出来做回显
#         send_data=jsonify({ # 同理这里需要把send_data发出去
#         "op": "del-file",
#         "id": id,
#         "path": filename
#         })
#     recv = connection.recv().decode()
#     return jsonify(recv), 200

# ----------


@app.route('/user/joinGroup',methods=['POST'])
def join_group():
    #加入群组
    global login
    global email
    global connection
    if login==0:
        return jsonify({'error':'need to login'}),400
    data=request.get_json()
    id = data.get('id')  # 传目标用户组id
    with open(id+'.bin','r') as f:
        main_key=f.read()
    if id=='':
        id=generate_group_key_id()
        layer_encrypt(None,id)
        
    send_data=jsonify({
    "op": "join-group",
    "id": id        #群组id
    })
    if id=='':
        id=generate_group_key_id()
        main_key_path=id+'.bin'
        main_key=generate_secure_key()
        with open(main_key_path,'w') as f:
            f.write(main_key)
    if main_key!=None:
        save_main_key(main_key,id)
    else:
        return jsonify({'error':'no main_key'}),400
    connection.send(send_data.get_data())
    recv_message=connection.recv().decode()
    result=json.loads(recv_message)
    if result['status']==200:
        return jsonify({'message':'joined group','main_key':main_key}),200
    else:
        return jsonify({'error':'failed to join group'}),400


if __name__ == '__main__':
    login=0
    #connection=ServerConn()
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(port= 5001,host='0.0.0.0',debug=True)
    
