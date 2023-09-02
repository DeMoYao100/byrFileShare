<template>
  <div id="userLayout">
    <a-layout style="min-height: 100vh">
      <a-layout-header class="header"> 用户布局 </a-layout-header>
      <a-layout-content class="content">
        <router-view />
      </a-layout-content>
      <a-layout-footer class="footer">
        <a href="https://google.com" target="_blank"> 谷歌搜索 </a>
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<style scoped>
#userLayout {
}

#userLayout .header {
  //background: red;
  margin-bottom: 16px;
}

#userLayout .content {
  background: linear-gradient(to right, #eee, #fff);
  margin-bottom: 16px;
  padding: 20px;
}

#userLayout .footer {
  background: #efefef;
  margin-bottom: 16px;
  padding: 16px;
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
  text-align: center;
}
</style>
<script setup lang="ts"></script>
