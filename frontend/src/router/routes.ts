import { RouteRecordRaw } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import AdminView from "@/views/AdminView.vue";
import NoAuthView from "@/views/NoAuthView.vue";
import ACCESS_ENUM from "@/access/accessEnum";
import UserLoginView from "@/views/user/UserLoginView.vue";
import UserRegisterView from "@/views/user/UserRegisterView.vue";
import UserUpdatepwdView from "@/views/user/UserUpdatepwdView.vue";
import PanView from "@/views/PanView.vue";
import UserLoginByEmailView from "@/views/user/UserLoginByEmailView.vue";

export const routes: Array<RouteRecordRaw> = [
  {
    path: "/user/login",
    name: "用户登录",
    // component: UserLayout,
    children: [
      {
        path: "/user/login",
        name: "用户登录",
        component: UserLoginView,
      },
      {
        path: "/user/register",
        name: "用户注册",
        component: UserRegisterView,
      },
      {
        path: "/user/updatepwd",
        name: "密码重置",
        component: UserUpdatepwdView,
      },
      {
        path: "/user/loginEmail",
        name: "邮箱登录",
        component: UserLoginByEmailView,
      },
    ],
  },
  {
    path: "/",
    name: "主页",
    component: HomeView,
  },
  {
    path: "/pan/:folderName?", // 添加一个可选的参数 folderName
    name: "我的网盘",
    component: PanView,
  },
  {
    path: "/hide",
    name: "隐藏题目",
    component: HomeView,
    meta: {
      hideInMenu: true,
    },
  },
  {
    path: "/noAuth",
    name: "无权限",
    component: NoAuthView,
  },
  {
    path: "/about",
    name: "关于我的",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
  {
    path: "/admin",
    name: "管理员可见",
    component: AdminView,
    meta: {
      access: ACCESS_ENUM.ADMIN,
    },
  },
];
