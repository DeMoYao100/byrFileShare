# SeCloud 前端项目文档

## 项目简介

SeCloud 是一款专注于密码学设计的网盘应用，旨在提供安全认证、加密传输和加密存储功能。应用保证用户数据的绝对安全，服务器端无法窃取任何用户数据。SeCloud 提供了与传统网盘应用相似的用户体验，是一个安全、可信、便捷的网盘解决方案。

本readme是对SeCloud中的前端界面部分的代码做介绍

## 环境准备

1. Node.js
2. npm

## 项目初始化

进入 `frontend` 目录并运行以下命令以安装项目依赖：

```bash
cd frontend
npm install
```

## 运行项目

启动项目：

```bash
npm run serve
```

项目将在 `localhost` 上以开发模式运行。

## 主要 UI 模块

### main.ts

该模块初始化 Vue 3 应用并配置了诸如 Arco Design UI 组件库、状态管理和路由等插件。

### App.vue

这是主组件，负责根据当前路由动态渲染页面。页面加载时会执行一个全局初始化函数。

### HomeView.vue

这是欢迎页面，展示了项目标题、图片和成员列表等。

### PanView.vue

这是文件管理核心界面，支持文件上传、下载、删除等功能。该界面使用 Vue 3 和 Anco Design 组件库构建。

### UserLoginView.vue 和 UserLoginByEmailView.vue

这两个模块提供了用户登录界面，支持邮箱登录。使用 Vue 3 和 Anco Design 组件库，并通过 API 与后端交互。

### UserRegisterView.vue 和 UserUpdatepwdView.vue

这两个模块分别用于用户注册和更新密码。同样使用 Vue 3 和 Anco Design 组件库，并与后端 API 进行交互。

### user.ts 和 pan.ts (Vuex)

这两个 Vuex 模块分别用于管理用户信息和文件管理状态。

### routes.ts

这里定义了 Vue 路由，映射 URL 到相应的 Vue 组件。

## 项目文件结构

```
.
├── babel.config.js                # Babel 编译配置文件
├── main.js                        # 与eletron打包相关的文件
├── package-lock.json              # npm 依赖版本锁文件
├── package.json                   # 项目依赖和脚本配置文件
├── public
│  ├── favicon.ico                 # 网站图标
│  └── index.html                  # HTML 入口文件
├── readmd_前端项目文档.md           # 项目文档
├── src
│  ├── App.vue                     # 主 Vue 组件，负责动态路由渲染
│  ├── access
│  │  ├── accessEnum.ts            # 定义访问权限枚举
│  │  ├── checkAccess.ts           # 检查访问权限的逻辑
│  │  └── index.ts                 # 权限控制模块入口
│  ├── assets
│  │  └── ...                      # 存放静态资源如图片、样式文件等
│  ├── axios-config.ts             # Axios 配置，用于 HTTP 请求
│  ├── components
│  │  └── GlobalHeader.vue         # 全局头部组件
│  ├── layouts
│  │  └── BasicLayout.vue          # 基础布局组件
│  ├── main.ts                     # Vue 项目主入口
│  ├── router
│  │  ├── index.ts                 # 路由配置主文件
│  │  └── routes.ts                # 定义具体路由规则
│  ├── store
│  │  ├── index.ts                 # Vuex 主文件，集中管理状态
│  │  ├── pan.ts                   # 管理文件存储状态
│  │  └── user.ts                  # 管理用户状态
│  └── views
│    ├── HomeView.vue              # 首页视图
│    ├── PanView.vue               # 文件管理视图
│    └── user
│      ├── UserLoginByEmailView.vue  # 通过邮箱登录的视图
│      ├── UserLoginView.vue         # 用户登录视图
│      ├── UserRegisterView.vue      # 用户注册视图
│      └── UserUpdatepwdView.vue     # 更新密码视图
├── tsconfig.json                  # TypeScript 配置文件
└── vue.config.js                  # Vue CLI 配置文件

```
