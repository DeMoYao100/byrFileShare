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
          <h1 style="text-align: center">~密码找回~</h1>
          <p class="tips">共筑网络安全，守护绿色家园</p>
          <a-form-item
            field="user"
            :rules="[{ required: true, message: '请输入标准邮箱地址' }]"
            :validate-trigger="['change', 'focus']"
            label="邮  箱"
          >
            <a-input v-model="form.user" placeholder="邮箱地址..." />
          </a-form-item>
          <a-form-item
            field="psw"
            :rules="[{ required: true, message: '密码可使用6个6' }]"
            :validate-trigger="['change', 'focus']"
            label="密  码"
          >
            <a-input-password v-model="form.psw" placeholder="密码输入..." />
          </a-form-item>
          <a-form-item
            field="psw"
            :rules="[{ required: true, message: '请输入相同密码' }]"
            :validate-trigger="['change', 'focus']"
            label="密码确认"
          >
            <a-input-password v-model="form.repsw" placeholder="输入相同密码" />
          </a-form-item>
          <a-form-item
            field="psw"
            :rules="[{ required: true, message: '请从邮箱获取验证码' }]"
            :validate-trigger="['change', 'focus']"
            label="验证码"
          >
            <a-input v-model="form.captcha" placeholder="验证码输入..." />
            <a-button @click="getVerifyCode" type="primary" size="medium"
              >获取验证码</a-button
            >
          </a-form-item>
          <a-form-item>
            <a-button html-type="submit" type="primary" size="large" long
              >找回</a-button
            >
            <a-button @click="$refs.loginForm.resetFields()" size="large" long
              >重置</a-button
            >
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import api from "@/axios-config";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();
// import "element-plus/lib/theme-chalk/index.css";
// import { ElAlert } from "element-plus";
const alertType = ref<"success" | "info" | "warning" | "error">("success");
const alertMessage = ref("操作成功"); // 要显示的消息
const showAlert = ref(false); // 是否显示 alert

const form = ref({
  user: "",
  psw: "",
  repsw: "",
  captcha: "",
});

const validForm = (form: { [key: string]: string }) => {
  let flag = [];
  for (let i in form) {
    if (!form[i]) flag.push(false);
    else flag.push(true);
  }
  return flag.every((el) => el);
};

// 提交表单函数
const handleSubmit = async () => {
  console.log("开始提交表单");
  // 验证表单是否完整
  if (validForm(form.value)) {
    // 验证两次密码是否一致
    if (form.value.psw !== form.value.repsw) {
      alertType.value = "error";
      alertMessage.value = "两次密码不一致";
      showAlert.value = true;
      return;
    }
    try {
      console.log("开始修改密码，向后端传的参数为：", {
        userEmail: form.value.user,
        userPassword: form.value.psw,
        verify_code: form.value.captcha,
      });
      const response = await api.post("/user/forgetPwd", {
        userEmail: form.value.user,
        userPassword: form.value.psw,
        verify_code: form.value.captcha,
      });

      // 根据返回状态进行处理
      if (response.data.message === "successfully changed password") {
        alertType.value = "success";
        alertMessage.value = "密码已成功更改";
        showAlert.value = true;
        await store.dispatch("user/getLoginUser");

        // 跳转到首页
        router.push({
          path: "/",
          replace: true,
        });
      } else {
        alertType.value = "error";
        alertMessage.value = response.data.error || "更改密码失败";
        showAlert.value = true;
      }
    } catch (error) {
      console.log("出现错误:", error);
      alertType.value = "error";
      alertMessage.value = "服务器异常";
      showAlert.value = true;
    }
  } else {
    alertType.value = "warning";
    alertMessage.value = "请完善表单信息";
    showAlert.value = true;
  }
};

// 获取验证码
const getVerifyCode = async () => {
  console.log("begin to get verify code");
  console.log("ger Verify Code 中 form.value.user:", form.value.user);
  if (form.value.user) {
    try {
      const response = await api.post("/user/verifyCode", {
        userEmail: form.value.user,
      });

      if (
        response.status === 200 &&
        response.data.message === "verify code successfully sent"
      ) {
        console.log("验证码发送成功");
      } else {
        console.log("验证码发送失败");
      }
    } catch (error) {
      console.log("出现错误:", error);
    }
  } else {
    console.log("邮箱地址为空");
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
}

.image-container {
  flex: 1; /* 占据剩余空间 */
  padding: 20px; /* 可选：为图片容器添加一些内边距 */
}

.content-container {
  flex: 1; /* 占据剩余空间 */
  /* 可选：为内容容器添加一些内边距或样式 */
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

@media (max-width: 390px) {
  .login-box {
    width: 350px;
  }
}

@media (max-width: 330px) {
  .login-box {
    width: 300px;
  }
}
</style>
