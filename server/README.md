# byrFileShare

## 服务器

服务器用来管理个人空间和群组空间文件，维护用户信息，支持多用户并发连接，能够实时对客户端请求进行回显。

### 部署
进入server目录
```bash
cd server
```
部署前，需要安装 Python 运行环境。推荐使用 3.9 版本以上的 Python 环境，过低的版本可能导致程序异常。在终端中输入
```bash
python --version
```
以查看当前环境 Python 版本。

部署服务器环境需要安装 pycryptodome 库。在终端中输入
```bash
pip install pycryptodome
```
来安装这个库。

部署时还需要生成空数据库文件并创建存储目录供程序运行时使用。在服务器目录下运行
```bash
python db.py
```
来生成空数据库文件。在服务器目录下运行
```bash
mkdir storage tmp
```
来生成存储目录。

### 运行

在服务器目录下运行
```bash
python server.py
```
来启动服务器。正常启动后，终端应显示
```
Server running at 0.0.0.0:2057
```

### 作者

夏锦熠

Email：
```bash
echo 'amlueWkueGlhQGJ1cHQuZWR1LmNuCg==' | base64 -d
```