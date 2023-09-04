import router from "@/router";
import store from "@/store";
import ACCESS_ENUM from "@/access/accessEnum";
import checkAccess from "@/access/checkAccess";
router.beforeEach(async (to, from, next) => {
  // 仅管理员可见，判断当前用户是否权限
  console.log(store.state.user.loginUser);
  // 编写权限管理和自动登录逻辑
  // 如果页面不需要登录，则直接跳过
  // 如果没登录过，则自动登录：
  const loginUser = store.state.user.loginUser;
  // 自动登录
  if (!loginUser || !loginUser.userRole) {
    //await是要等用户登录之后再执行其它代码
    await store.dispatch("user/getLoginUser");
  }
  const needAccess = (to.meta?.access as string) ?? ACCESS_ENUM.NOT_LOGIN;
  if (needAccess !== ACCESS_ENUM.NOT_LOGIN) {
    // 如果要跳转的页面不需要登录，则不需要登录
    if (!loginUser || !loginUser.userRole) {
      next("/user/login?redirect=${to.fullPath}");
      return;
    }
    if (!checkAccess(loginUser, needAccess)) {
      next("/noAuth");
      return;
    }
  }
  next();
});
