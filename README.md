# SeCloud - 您的安全网盘应用

## 项目简介

SeCloud 是一款集安全认证、加密传输和加密存储于一体的高级网盘应用。该应用从底层构建安全网盘应用，实现用户中心的加密和认证体制，确保服务器无法窃取任何用户数据。

## 特点

- **用户中心的加密和认证体制**：SeCloud服务器无法窃取任何用户数据，从而保证了用户的隐私和数据安全。
- **多重安全机制**：采用硬件安全模块（U盾）和多种密钥管理机制。
- **透明加密传输**：利用DH密钥交换协议和数字证书，实现了与HTTPS相似的加密通信信道。
- **文件加密管理**：使用层级密钥结构，由U盾中的主密钥生成不同的文件加密密钥。
- **P2P加密信道和U盾物理传递**：实现了共享网盘功能，保证了文件的安全传输和存储。

## 安装与运行

项目包含三部分：server(服务器)、client(客户端后端)、frontend(客户端前端)，运行该代码需要分别配置三部分环境。

每个部分的环境配置方法在其目录下，分别命名为：README_server.md、README_client.md、README_frontend.md
需要打开三个shell，分别cd进对应目录，按照对应目录的帮助文档进行代码运行

## 技术栈

### 后端技术栈

- **Python**: 后端开发语言
- **密码库协议、算法编程**: 使用Python的成熟密码库
- **Socket网络编程**: 使用Python的socket库进行底层通信
- **Flask**: 轻量级Web框架
- **数据库管理**: 用于存储用户信息和文件元数据
- **消息队列**: 使用socket实现

### 前端技术栈

- **Vue3**: 前端框架
- **Electron**: 跨平台APP开发
- **Axios**: 用于客户端与后端通信
- **Vue Router**: 前端路由管理
- **Vuex**: 应用级状态管理
- **acro design UI**: UI框架
- **Sass**: CSS预处理器

## 代码运行（推荐进入子目录下对应client、server、frontend下查看详细介绍）

### 客户端后端：
0. 进入 `client` 目录。
    ```bash
    cd client
    ```
1. 安装 Python 运行环境，推荐使用 3.11 版本以上。
    ```bash
    python --version
    ```
2. 安装依赖库：
    ```bash
    pip install pycryptodome flask flask_cors cryptography
    ```
3. 更改 `ip.txt` 为服务器 IP 地址。
4. 运行 `client.py`。

### 服务器端：
0. 进入 `server` 目录。
    ```bash
    cd server
    ```
   
1. 安装 Python 运行环境，推荐使用 3.9 版本以上。
    ```bash
    python --version
    ```
2. 安装 `pycryptodome` 库：
    ```bash
    pip install pycryptodome
    ```
3. 生成空数据库文件并创建存储目录：
    ```bash
    python db.py
    mkdir storage tmp
    ```
4. 运行 `server.py`。

### 客户端前端：

1. 安装 Node.js 和 npm。(npm安装教程:https://zhuanlan.zhihu.com/p/138279801)
2. 进入 `frontend` 目录并安装项目依赖：
    ```bash
    cd frontend
    npm install
    ```
3. 启动项目：
    ```bash
    npm run serve
    ```
