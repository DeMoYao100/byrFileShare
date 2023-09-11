import { RouteRecordRaw } from "vue-router";
import HomeView from "@/views/HomeView.vue";
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
];
