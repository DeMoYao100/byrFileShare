<template>
  <a-alert
    v-if="showAlert"
    :type="alertType"
    :title="alertMessage"
    center
    show-icon
  />
  <div class="back-to-home">
    <router-link :to="{ path: '/' }">
      <a-button type="default">返回主页面</a-button>
    </router-link>
  </div>
  <div class="container">
    <div class="image-container">
      <img
        class="bac-img animate__animated animate__pulse"
        src="@/assets/loginbg.png"
        alt=""
        style="width: 100%; height: 100%"
      />
    </div>
    <div class="content-container">
      <div class="default-box">
        <a-form
          ref="loginForm"
          :model="form"
          class="login-box animate__animated animate__bounceIn"
          @submit="handleSubmit"
          auto-label-width
        >
          <h1 style="text-align: center">~安全网盘系统登录~</h1>
          <p class="tips">共筑网络安全，守护绿色家园</p>
          <a-form-item
            field="user"
            :rules="[{ required: true, message: '请输入标准邮箱地址' }]"
            :validate-trigger="['change', 'focus']"
            label="邮箱"
          >
            <a-input v-model="form.user" placeholder="邮箱地址..." />
          </a-form-item>
          <a-form-item
            field="psw"
            :rules="[{ required: true, message: '密码可使用6个6' }]"
            :validate-trigger="['change', 'focus']"
            label="密码"
          >
            <a-input-password v-model="form.psw" placeholder="密码输入..." />
          </a-form-item>
          <a-form-item>
            <a-button html-type="submit" type="primary" size="large" long
              >登录</a-button
            >
            <a-button @click="$refs.loginForm.resetFields()" size="large" long
              >重置</a-button
            >
          </a-form-item>
          <a-form-item>
            <p class="tips1">如还未注册账号，请点击此处注册</p>
            <router-link :to="{ path: '/user/register' }">
              <a-button size="small" type="primary">注册</a-button>
            </router-link>
          </a-form-item>
          <a-form-item>
            <p class="tips1">如忘记注册密码，请点击此处找回</p>
            <router-link :to="{ path: '/user/updatepwd' }">
              <a-button size="small" type="primary">找回</a-button>
            </router-link>
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import api from "@/axios-config"; // 使用你定义的api实例
import { useStore } from "vuex";
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const groupDrives = ref([]);
const router = useRouter();

// 用 ref 创建响应式变量
const form = ref({
  user: "",
  psw: "",
});

const alertType = ref<"success" | "info" | "warning" | "error">("success");
const alertMessage = ref("操作成功"); // 要显示的消息
const showAlert = ref(false); // 是否显示 alert
const store = useStore();

// 验证表单函数
const validForm = (form: { [key: string]: string }) => {
  let flag = true;
  for (let i in form) {
    if (!form[i]) {
      flag = false;
      break;
    }
  }
  return flag;
};

// 提交表单函数
const handleSubmit = async () => {
  console.log(1);
  if (validForm(form.value)) {
    console.log(2);

    try {
      const response = await api.post("/user/loginPwd", {
        email: form.value.user,
        password: form.value.psw,
      });

      if (response.data.message === "Login successful") {
        alertType.value = "success";
        alertMessage.value = "登录成功";
        showAlert.value = true;

        // 更新Vuex中的用户状态
        await store.dispatch("user/getLoginUser");

        // 跳转到首页
        router.push({
          path: "/",
          replace: true,
        });
      } else {
        console.log("登录失败");
        alertType.value = "error";
        alertMessage.value = "登录失败";
        showAlert.value = true;
      }
    } catch (error) {
      console.log("出现错误:", error);
      alertType.value = "error";
      alertMessage.value = "登录异常";
      showAlert.value = true;
    }
  } else {
    console.log("表单不完整");
    alertType.value = "warning";
    alertMessage.value = "请完善表单信息";
    showAlert.value = true;
  }
};
</script>

<style scoped>
.back-to-home {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 999; /* 确保在其他元素之上 */
}
.container {
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  height: 100vh; /* 设置高度 */
  width: 100%; /* 设置宽度 */
}

.image-container {
  flex: 1; /* 占据剩余空间 */
  padding: 20px; /* 可选：为图片容器添加一些内边距 */
}

.content-container {
  flex: 1; /* 占据剩余空间 */
}
.login-box {
  max-width: 400px;
  box-sizing: border-box;
  padding: 50px 30px;
  box-shadow: 0 0 6px #4b4b4b;
  border-radius: 9px;
  background-color: #e9f1fc;
  border: 1px solid #98a6f8; /* 添加边框，可以根据需要调整颜色和样式 */
}

.tips {
  color: #6b6b6b;
  text-align: center;
  margin-top: -9px;
}

.tips1 {
  color: #000000;
  text-align: left;
  margin-top: 15px;
  margin-left: -20px;
  margin-right: 20px;
}

@media (max-width: 1024px) {
  .bac-img {
    display: none;
  }
}
@media (max-width: 1000px) {
  .image-container {
    display: none; /* 隐藏图片 */
  }
  .content-container {
    margin: auto; /* 自动填充外边距，实现居中 */
  }
  /* 删除对.container的修改 */
}
</style>
