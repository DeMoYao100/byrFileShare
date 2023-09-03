<template>
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
            :rules="[{ required: true, message: '密码可使用任意格式' }]"
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
            <a-button html-type="submit" type="primary" size="medium"
              >获取验证码</a-button
            >
          </a-form-item>
          <a-form-item>
            <a-button html-type="submit" type="primary" size="large" long
              >注册</a-button
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

<script lang="ts">
import { ref, defineComponent } from "vue";
export default defineComponent({
  name: "LoginView",
  setup() {
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

    const handleSubmit = () => {
      if (validForm(form.value)) {
        // 这里原本是和后端的交互代码，暂时不包括
      }
    };

    return {
      form,
      validForm,
      handleSubmit,
    };
  },
});
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
