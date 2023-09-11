# byrFileShare



[参考知乎](https://zhuanlan.zhihu.com/p/430760821)

##### 1.打包python文件

##### 2.修改js中调用python的代码

##### 3.构建文件并打包electron

---

##### 1.打包python文件

- nuitka打包

`pip install nuitka`

`python -m nuitka frontend.py --follow-imports` (--follow-imports 会附带打包依赖)

- pyinstaller

`pyinstaller -F C:\Users\18238\Downloads\packTest\byrFileShare-frontend\client\frontend.py`

##### 2.修改js中调用python的代码

打包方法：
``` js
const { spawn } = require('child_process');
const python = spawn('python', ['\frontend.exe']);
```

![image](https://github.com/DeMoYao100/byrFileShare/assets/104621303/9d163e61-07ca-49a0-8810-381bd400fe27)


##### 3.构建文件并打包electron

`npm install electron --save-dev`

`npm init`

```json
# package.json
{
  "name": "your-app",
  "version": "1.0.0",
  "main": "C:/Users/18238/Downloads/packTest/byrFileShare-frontend/frontend/main.js",
  "scripts": {
    "start": "electron .",
    "package": "electron-packager ./ test --platform=win32 --arch=x64"
  },
  "dependencies": {
    "electron-packager": "^17.1.2"
  },
  "devDependencies": {
    "electron": "^latest-version"
  }
}

```

`npm run package`
