<template>
  <a-layout class="main-layout">
    <a-layout-header style="padding-left: 20px">
      <div class="header-container">
        <div class="logo">
          <img
            :src="logoSrc"
            alt="Logo"
            style="width: 80px; height: auto; margin-top: 20px"
          />
        </div>
        <div class="seccloud-text">欢迎使用SeCloud</div>
        <a
          href="https://github.com/DeMoYao100/byrFileShare"
          class="github-icon"
        >
          <icon-github />
        </a>
        <div class="user-action">
          <a-avatar @click="handleUserAction" v-if="isUserLoggedIn.value">
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
          <a-menu-item key="createGroup">
            <IconHome></IconHome>
            创建群组
          </a-menu-item>
          <a-menu-item key="joinGroup">
            <IconHome></IconHome>
            加入群组
          </a-menu-item>
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
              v-for="drive in groupDrives.value"
              :key="drive.id"
              @click="handleGroupDriveClick(drive.id)"
            >
              {{ drive.id }}
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
          <router-view :key="store.state.pan.currentPan"></router-view>
          <!-- 这里是用于路由渲染的标签 -->
        </a-layout>
      </a-layout>
    </a-layout>
  </a-layout>
  <Modal
    v-model:visible="isModalVisible_create"
    title="创建群组确认"
    :onOk="handleOk_create"
    :onCancel="handleCancel_create"
  >
    <p>创建群组将向你提供群组密钥，请妥善保管，是否创建？</p>
  </Modal>

  <!-- 加入群组的模态窗口 -->
  <Modal
    v-model:visible="isModalVisible_join"
    title="加入群组"
    :onOk="handleOk_join"
    :onCancel="handleCancel_join"
  >
    <a-input
      :style="{ width: '320px' }"
      placeholder="请输入群组ID"
      :size="size"
      allow-clear
      v-model="groupInfo"
    />
  </Modal>
</template>
<script setup>
import { onMounted, computed, watch, ref, reactive } from "vue";
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
import { Modal } from "@arco-design/web-vue";
import api from "@/axios-config";
import logoSrc from "@/assets/logo.png";

const isModalVisible_create = ref(false);
const isModalVisible_join = ref(false);

const router = useRouter();
const store = useStore();
const groupInfo = ref("");
const groupDrives = reactive({ value: [] });

// 使用 ref 替代原来的值，以便在 state 改变时更新
const isUserLoggedIn = ref(false);

const userEmail = computed(
  () => store.state.user?.loginUser?.userEmail ?? "未登录"
);
const usernameShort = computed(() => {
  if (userEmail.value !== "未登录") {
    return userEmail.value.slice(0, 3); // 获取userEmail的前3位
  }
  return "未登录";
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

const fetchGroupList = async () => {
  console.log("执行");
  try {
    console.log("开始拿到群列表");
    const response = await api.post("/user/initlist");
    console.log("fetch结束", response);
    if (response.status === 200) {
      console.log("fetch到的目录data", response.data);

      // 将字符串数组转换为对象数组
      const transformedData = response.data.map((item) => ({ id: item }));
      groupDrives.value = transformedData;

      console.log("groupDrives.value", groupDrives.value);
    } else {
      console.log("Failed to fetch group list:", response.data);
    }
  } catch (error) {
    console.log("Failed to fetch group list:", error);
  }
};

const handleGroupDriveClick = (id) => {
  store.commit("pan/setCurrentPan", id);
  console.log("点击我的网盘后，当前的pan是：", store.state.pan.currentPan);
  router.push("/pan");
};

const pan = computed(() => store.state.pan.currentPan);

const onClickMenuItem = (key) => {
  switch (key) {
    case "createGroup":
      isModalVisible_create.value = true;
      break;
    case "joinGroup":
      isModalVisible_join.value = true;
      break;
    case "0_1":
      router.push("/");
      break;
    case "0_2":
      store.commit(
        "pan/setCurrentPan",
        store.state.user?.loginUser?.userEmail ?? "未登录"
      );
      console.log("点击我的网盘后，当前的pan是：", store.state.pan.currentPan);
      router.push("/pan");
      break;
  }
};

// 创建群组的函数
const handleOk_create = async () => {
  isModalVisible_create.value = false;
  try {
    const response = await api.post("/user/joinGroup", {
      id: "", // 创建群组时，群组ID应为空
    });
    if (response.data.message === "joined group") {
      await fetchGroupList();
    } else {
      console.error("Failed to create group:", response.data.error);
    }
  } catch (error) {
    console.error("Failed to create group:", error);
  }
};
// 加入群组的函数
const handleOk_join = async () => {
  isModalVisible_join.value = false;
  try {
    const response = await api.post("/user/joinGroup", {
      id: groupInfo.value, // 加入群组时，群组ID应为用户输入的值
    });
    if (response.data.message === "joined group") {
      console.error("成功加入群组");
      await fetchGroupList();
    } else {
      console.error("加入群组失败:", response.data.error);
    }
  } catch (error) {
    console.error("加入群组失败:", error);
  }
};
// 使用 Vuex action 获取登录用户信息
onMounted(async () => {
  await store.dispatch("user/getLoginUser");
  await fetchGroupList();
});

const handleCancel_create = () => {
  // 你的逻辑代码，比如关闭模态框
  isModalVisible_create.value = false;
};

const handleCancel_join = () => {
  // 你的逻辑代码，比如关闭模态框
  isModalVisible_create.value = false;
};
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

.unlogged-box {
  display: inline-block;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer; /* 添加鼠标样式为手指，表示可点击 */
}
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.seccloud-text {
  text-align: center;
  flex-grow: 1;
  font-size: 30px;
  color: skyblue;
}
.github-icon {
  margin-right: 40px;
  font-size: 24px;
}
</style>
