# SeCloud 客户端后端项目文档

## 项目简介

SeCloud 是一款专注于密码学设计的网盘应用，旨在提供安全认证、加密传输和加密存储功能。应用保证用户数据的绝对安全，服务器端无法窃取任何用户数据。SeCloud 提供了与传统网盘应用相似的用户体验，是一个安全、可信、便捷的网盘解决方案。

本readme是对SeCloud中的后端界面部分的代码做介绍

## 环境准备
进入client目录
```bash
cd client
```
部署前，需要安装 Python 运行环境。推荐使用 3.11 版本以上的 Python 环境，过低的版本可能导致程序异常。在终端中输入
```bash
python --version
```
以查看当前环境 Python 版本。

部署服务器环境需要安装 一些依赖 库。在终端中输入
```bash
pip install pycryptodome
pip install flask
pip install flask_cors
pip install cryptography
```

运行: 1.更改ip.txt为服务器ip地址 2.运行client.py

主要文件/文件夹功能介绍:

client.py:客户端后端主体代码

conn.py:客户端后端与服务器交互部分代码

cry文件夹:加密通信系统

ca_public_key.pem:CA公钥文件

dowmload文件夹:从服务器下载文件的存放地址

## 加密部分

1. **导入模块和库**：
   - 代码开头导入了所需的模块和库，包括`os`等。

2. **导入自定义模块**：
   - 代码中使用了自定义的加密相关模块，包括`cry.EncryptFile`、`cry.GenerateSalt`、`cry.GenerateSubKey`、`cry.HMAC`、`cry.GenerateMainKey`。

3. **加密函数**：`layer_encrypt(input_file, keyID)`
   - 这个函数用于执行文件加密操作。它接受输入文件路径和密钥ID作为参数，并返回加密后的数据。
   - 在函数内部，首先生成随机盐（salt），然后尝试加载主密钥文件。
   - 使用主密钥和盐生成子密钥，然后使用子密钥对输入文件进行加密。
   - 计算用于生成HMAC的密钥，然后生成HMAC值。
   - 最后，将salt、keyID、加密后的文件数据、初始化向量（iv）和HMAC值拼接成一个二进制数据块，并返回。

4. **保存主密钥函数**：`save_main_key(main_key, keyID)`
   - 这个函数用于保存主密钥到U盘中。它接受主密钥和密钥ID作为参数，并将主密钥保存为二进制文件。
   - 主密钥文件名以密钥ID命名，然后文件保存到U盘的特定路径。

5. **主要逻辑**：
   - 在主函数 `layer_encrypt(input_file, keyID)` 中，首先生成盐，然后尝试加载主密钥。
   - 接着，生成子密钥，使用子密钥对输入文件进行加密，并计算HMAC值。
   - 最后，将所有信息拼接在一起以创建加密后的数据块，或者在生成主密钥时将主密钥保存到U盘。

6. **异常处理**：
   - 在保存主密钥时，代码包含异常处理以处理可能的错误。

7. **注释**：
   - 代码中包含了一些注释，但注释量相对较少。可能需要更多注释来解释代码的详细逻辑和用途。

这个代码结构相对简单，有两个主要功能：文件加密和主密钥保存。在主函数中，根据输入的条件执行其中一个功能。

## 解密部分

1. **导入模块和库**：
   - 代码一开始导入了所需的模块和库，包括`hashlib`、`hmac`、`Crypto.Cipher`、`Crypto.Protocol.KDF`等。

2. **从加密文件中提取值**：
   - `extract_values_from_encrypted_file(file_path)` 函数用于从加密文件中提取盐（salt）、密钥ID（keyID）、密文数据（cipher_data）、初始化向量（iv）和HMAC。

3. **加载二进制文件**：
   - `load_binary_file(file_path)` 函数用于从文件加载二进制数据。

4. **生成子密钥**：
   - `generate_sub_key(main_key, salt, key_length=32, iterations=100000)` 函数使用PBKDF2从主密钥和盐生成子密钥。

5. **解密函数**：
   - `layer_decrypt(cipher_file)` 函数用于解密数据。它首先验证HMAC以确保数据完整性，然后加载主密钥，生成子密钥，并使用AES-CTR模式解密数据。

6. **主要逻辑**：
   - 在 `layer_decrypt` 函数中，首先提取加密文件中的关键信息，然后验证HMAC。接着，构建主密钥文件的路径并加载主密钥。最后，生成子密钥并使用它来解密密文数据。

7. **异常处理**：
   - 在加载二进制文件时，代码包含了异常处理以处理可能的错误。

8. **注释**：
   - 添加了详细的注释，解释了每个函数和代码段的功能和作用。

这个代码结构清晰，每个函数都有特定的任务，并使用注释提供了代码的文档说明。