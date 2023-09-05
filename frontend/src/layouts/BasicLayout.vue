<template>
  <a-layout class="main-layout">
    <a-layout-header style="padding-left: 20px">
      <div class="header-container">
        <div class="logo">
          <!-- 在这里添加你的Logo图像或文本 -->
          Logo
        </div>
        <div class="user-action">
          <a-avatar @click="handleUserAction" v-if="isUserLoggedIn">
            {{ usernameShort }}
            <template #trigger-icon>
              <IconEdit />
            </template>
          </a-avatar>
          <a-button @click="handleUserAction" v-else>点击登录</a-button>
        </div>
      </div>
    </a-layout-header>
    <a-layout>
      <a-layout-sider>
        <div class="logo" />
        <a-menu
          :default-open-keys="['0_1']"
          :default-selected-keys="['0_1']"
          :style="{ width: '100%' }"
          @menu-item-click="onClickMenuItem"
        >
          <a-menu-item key="0_1">
            <IconHome></IconHome>
            主页
          </a-menu-item>
          <a-menu-item key="0_2">
            <IconCalendar></IconCalendar>
            我的网盘
          </a-menu-item>
          <a-sub-menu key="groupDrive">
            <template #title><IconCalendar></IconCalendar> 群组网盘 </template>
            <a-menu-item
              v-for="drive in groupDrives"
              :key="drive.id"
              @click="navigateToDrive(drive.id)"
            >
              {{ drive.name }}
            </a-menu-item>
          </a-sub-menu>
        </a-menu>
        <!-- trigger -->
        <template #trigger="{ collapsed }">
          <IconCaretRight v-if="collapsed"></IconCaretRight>
          <IconCaretLeft v-else></IconCaretLeft>
        </template>
      </a-layout-sider>
      <a-layout>
        <a-layout>
          <router-view></router-view>
          <!-- 这里是用于路由渲染的标签 -->
        </a-layout>
      </a-layout>
    </a-layout>
  </a-layout>
</template>
<script setup>
import { onMounted, computed, watch, ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import {
  IconCaretRight,
  IconCaretLeft,
  IconHome,
  IconCalendar,
  IconEdit,
} from "@arco-design/web-vue/es/icon";
import ACCESS_ENUM from "@/access/accessEnum";

const groupDrives = ref([]);
const router = useRouter();
const store = useStore();

// 使用 ref 替代原来的值，以便在 state 改变时更新
const isUserLoggedIn = ref(false);
const username = ref("");

// 取用户名的前部分作为简短显示
const usernameShort = computed(() => {
  if (username.value.includes("@")) {
    return username.value.split("@")[0];
  }
  return username.value;
});

// 处理用户点击事件
const handleUserAction = () => {
  if (isUserLoggedIn.value) {
    // 处理已登录用户的点击事件（例如，打开用户设置等）
  } else {
    router.push("/user/login");

    // 处理未登录用户的点击事件（例如，导航至登录页面等）
  }
};

// 模拟从 Vuex 获取用户状态和信息（这部分需要你根据实际情况编写）
isUserLoggedIn.value = store.state.isUserLoggedIn;
username.value = store.state.username;
// 获取群组网盘信息
const fetchGroupDrives = async () => {
  try {
    const response = await axios.get("/api/group-drives");
    groupDrives.value = response.data;
  } catch (error) {
    console.error("Failed to fetch group drives:", error);
  }
};

// 点击跳转
const navigateToDrive = (driveId) => {
  router.push(`/drive/${driveId}`);
};

const onClickMenuItem = (key) => {
  switch (key) {
    case "0_1":
      router.push("/main");
      break;
    case "0_2":
      router.push("/pan");
      break;
  }
};

const navigateToLogin = () => {
  if (!store.state.user?.loginUser) {
    router.push("/login");
  }
};

// 使用 Vuex action 获取登录用户信息
onMounted(async () => {
  await store.dispatch("user/getLoginUser");
  fetchGroupDrives();
});

// 监听 loginUser state 的变化
watch(
  () => store.state.user.loginUser,
  (loginUser) => {
    // 根据 loginUser 的 userRole 判断用户是否已登录
    isUserLoggedIn.value = loginUser.userRole !== ACCESS_ENUM.NOT_LOGIN;
    // 更新 username
    username.value = loginUser.userName;
  }
);
</script>
<style scoped>
.main-layout {
  height: 100vh; /* 设置高度为视口高度的100% */
  background: var(--color-fill-2);

  border: 1px solid var(--color-border);
}

.main-layout :deep(.arco-layout-sider) .logo {
  margin-top: 0;

  height: 32px;
  margin: 12px 8px;
  background: rgba(255, 255, 255, 0.2);
}
.main-layout :deep(.arco-layout-sider-light) .logo {
  background: var(--color-fill-2);
}
.main-layout :deep(.arco-layout-header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  line-height: 64px;
  background: var(--color-bg-3);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1); /* 调深阴影 */
  z-index: 1;
}

.main-layout :deep(.arco-layout-footer) {
  height: 48px;
  color: var(--color-text-2);
  font-weight: 400;
  font-size: 14px;
  line-height: 48px;
}
.main-layout :deep(.arco-layout-content) {
  color: var(--color-text-2);
  font-weight: 400;
  font-size: 14px;
  background: var(--color-bg-3);
}
.main-layout :deep(.arco-layout-footer),
.main-layout :deep(.arco-layout-content) {
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: var(--color-white);
  font-size: 16px;
  font-stretch: condensed;
  text-align: center;
}
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding-left: 20px;
  padding-right: 50px;
}

.logo {
  /* 你的Logo样式 */
}

.username {
  /* 你的用户名样式 */
}

.unlogged-box {
  display: inline-block;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer; /* 添加鼠标样式为手指，表示可点击 */
}
</style>
