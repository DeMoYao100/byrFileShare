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
  <div class="sum-box">
    <div class="image-box">
      <img
        class="bac-img animate__animated animate__pulse"
        src="@/assets/loginbg.png"
        alt=""
        style="width: 100%; height: 100%"
      />
    </div>
    <div class="content-box">
      <div class="default-box">
        <a-form
          ref="loginEmailForm"
          :model="form"
          class="loginEmail-box animate__animated animate__bounceIn"
          @submit="handleSubmit"
          auto-label-width
        >
          <h1 style="text-align: center">~邮箱登录界面~</h1>
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
              >登录</a-button
            >
            <a-button
              @click="$refs.loginEmailForm.resetFields()"
              size="large"
              long
              >重置</a-button
            >
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import api from "@/axios-config"; // 注意这个路径应当根据你的项目结构来调整

// 导入需要的库和接口
import { ref, defineComponent } from "vue";
import axios from "axios";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();
const form = ref({
  user: "",
  captcha: "",
});
const alertType = ref<"success" | "info" | "warning" | "error">("success");
const alertMessage = ref("操作成功"); // 要显示的消息
const showAlert = ref(false); // 是否显示 alert
// 验证表单字段
const validForm = (form: { [key: string]: string }) => {
  let flag = [];
  for (let i in form) {
    if (!form[i]) flag.push(false);
    else flag.push(true);
  }
  return flag.every((el) => el);
};

// 获取验证码
const getVerifyCode = async () => {
  console.log("begin to get verify code");
  if (form.value.user) {
    try {
      const response = await api.post("/user/verifyCode", {
        userEmail: form.value.user,
      });

      if (
        response.status === 200 &&
        response.data.message === "verify code successfully sent"
      ) {
        alertType.value = "success";
        alertMessage.value = "验证码发送成功";
        showAlert.value = true;
        console.log("验证码发送成功");
      } else {
        alertType.value = "error";
        alertMessage.value = "验证码发送失败";
        showAlert.value = true;
        console.log("验证码发送失败");
      }
    } catch (error) {
      alertType.value = "error";
      alertMessage.value = "出现错误";
      showAlert.value = true;
      console.log("出现错误:", error);
    }
  } else {
    console.log("邮箱地址为空");
  }
};
// 提交注册信息
const handleSubmit = async () => {
  console.log("开始邮箱登录");
  console.log("现在表单数据是:", form.value);
  if (validForm(form.value)) {
    try {
      const response = await api.post("/user/loginEmail", {
        userEmail: form.value.user,
        verify_code: form.value.captcha, // 注意这里的字段名应该与 Flask 后端要求的一致
      });

      if (response.data.message === "Register successful") {
        alertType.value = "success";
        alertMessage.value = "注册成功";
        showAlert.value = true;
        console.log("注册成功");
        await store.dispatch("user/getLoginUser");
        router.push({ path: "/", replace: true });
      } else {
        alertType.value = "error";
        alertMessage.value = "注册失败";
        showAlert.value = true;
        console.log("注册失败");
      }
    } catch (error) {
      alertType.value = "error";
      alertMessage.value = "出现错误";
      showAlert.value = true;
      console.log("出现错误:", error);
    }
  } else {
    console.log("表单验证失败");
  }
};
</script>
<style scoped>
.sum-box {
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
}

.image-box {
  flex: 1; /* 占据剩余空间 */
  padding: 20px; /* 可选：为图片容器添加一些内边距 */
}

.content-box {
  flex: 1; /* 占据剩余空间 */
  /* 可选：为内容容器添加一些内边距或样式 */
}
.loginEmail-box {
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
  .loginEmail-box {
    width: 350px;
  }
}

@media (max-width: 330px) {
  .loginEmail-box {
    width: 300px;
  }
}
</style>
