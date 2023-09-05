<template>
  <div class="image-container">
    <img
      class="logo1"
      src="@/assets/logo1.png"
      alt=""
      style="width: 20%; height: 20%"
    />
    <h1>SeCloud</h1>
    <p class="tips">
      成员：王迪、陈子瑞、何冠立、林鹭乾、李翔宇、张一鸣、夏锦熠、张原赫
    </p>
    <div class="introduce">
      <p>介绍巴拉巴拉。。。</p>
    </div>
    <router-link :to="{ path: '/user/login' }">
      <a-button size="large" type="primary">登录</a-button>
    </router-link>
    <p class="bottom-statement">_</p>
  </div>
</template>

<style scoped>
.image-container {
  margin-top: -10px;
  margin-bottom: -50px;
  text-align: center;
  background: linear-gradient(45deg, #fff5d8, #dbf3ff, #f4f8db);
  background-size: 400% 400%;
  animation: gradientAnimation 5s ease infinite;
}

@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* 样式可以根据你的需要进行调整 */
h1 {
  font-size: 50px;
  margin-top: 30px;
  color: white; /* 标题颜色 */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* 添加文本阴影效果 */
}

.logo1 {
  margin-top: 100px;
}

.introduce {
  font-size: 30px;
  margin-top: 30px;
  color: white; /* 字体颜色 */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* 添加文本阴影效果 */
}

.bottom-statement {
  margin-top: 200px; /* 根据需要调整底边距大小 */
  color: rgba(255, 255, 255, 0);
}
</style>
<script setup lang="ts"></script>
