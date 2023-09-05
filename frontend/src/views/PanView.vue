<template>
  <div class="common-layout">
    <a-layout>
      <div class="top">
        <div class="top-op">
          <a-space class="a-space-container">
            <div class="btn">
              <a-upload :show-file-list="false" :custom-request="uploadFile">
              </a-upload>
            </div>
            <div>
              <a-button type="primary" @click="openModal">新建文件夹</a-button>
              <a-modal
                title="新建文件夹"
                v-model:visible="newFolderDialogVisible"
                :before-close="handleClose"
              >
                <a-input
                  v-model="newFolderName"
                  placeholder="请输入文件夹名称"
                ></a-input>
                <template #footer>
                  <a-button type="primary" @click="newFolder">提交</a-button>
                </template>
              </a-modal>
            </div>

            <!--     todo 这个在未来实现         -->
            <a-button type="primary"> 批量删除 </a-button>
            <a-button
              type="primary"
              :disabled="!router.currentRoute.value.params.folderName"
              @click="navigateBack"
            >
              返回
            </a-button>
            <a-input
              clearable
              placeholder="输入文件名搜索"
              v-model="fileNameFuzzy"
              @keyup.enter="search"
            >
            </a-input>
          </a-space>
        </div>
      </div>
      <a-layout-content class="a-layout-content">
        <a-table
          :data="tableData"
          :hoverable="true"
          :showHeader="true"
          class="table-content"
          :scrollbar="true"
          :scroll="{ y: 20000 }"
          :virtual-list-props="{ height: 400 }"
          :pagination="false"
        >
          <template #columns>
            <!-- todo 行选择器-->
            <a-table-column title="文件名">
              <template #cell="{ record }">
                <a
                  v-if="record.fileType === 'dir'"
                  @click="navigateToFolder(record.fileName)"
                >
                  {{ record.fileName }}
                </a>
                <span v-else>{{ record.fileName }}</span>
              </template>
            </a-table-column>
            <a-table-column
              title="修改时间"
              data-index="lastUpdateTime"
            ></a-table-column>
            <a-table-column title="大小" data-index="fileSize"></a-table-column>
            <a-table-column title="类型" data-index="fileType"></a-table-column>
            <a-table-column title="操作">
              <template #cell="{ record }">
                <!-- 使用 Arco Design 的图标组件，直接绑定下载函数 -->
                <icon-download
                  :style="{
                    color: hoverDownload ? 'darkgray' : '',
                    'font-size': '24px',
                  }"
                  @mouseover="hoverDownload = true"
                  @mouseout="hoverDownload = false"
                  @click="downloadFile(record)"
                />
                <!-- 使用 Arco Design 的图标组件，直接绑定删除函数 -->
                <icon-delete
                  :style="{
                    color: hoverDownload ? 'darkgray' : '',
                    'font-size': '24px',
                  }"
                  @mouseover="hoverDelete = true"
                  @mouseout="hoverDelete = false"
                  @click="deleteFile(record)"
                />
              </template>
            </a-table-column>
          </template>
        </a-table>
        <!--   todo 显示太多怎么办？-->
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script setup>
//todo 三级目录实现
import { ref, onMounted, watch } from "vue";
import api from "@/axios-config";
import { useStore } from "vuex";
import router from "@/router";
import { join, dirname } from "path-browserify";
import { useRoute } from "vue-router";

//这里是使得界面一家在就开始获取一次文件列表，后面每一次操作都需要向python获取一次文件列表
onMounted(async () => {
  await getFileList();
});
const fileAccept = ref("*");
const fileNameFuzzy = ref("");
const currentPage = ref(1);
const pageSize = ref(15);
const newFolderDialogVisible = ref(false);
const newFolderName = ref("");
const tableData = ref([]);

//上传对话框相关变量
const uploadDialogVisible = ref(false);
const uploadFilePath = ref("");
const store = useStore(); // 在这里调用useStore
const route = useRoute();
const currentFolder = ref(""); // 创建一个本地状态来存储当前文件夹路径

const newFolder = async () => {
  console.log("New folder button clicked");

  // 获取当前的文件夹路径和新文件夹的名称
  const folder = currentFolder.value;
  const folderName = newFolderName.value;
  const newFolderPath = join(folder, folderName);

  console.log(
    "newFolder中，folder是：",
    folder,
    "newFolderName是：",
    folderName
  );
  console.log("我们要传这个给后端创建新文件夹：", newFolderPath);

  try {
    // 发送创建新文件夹的请求
    const response = await api.post("/user/makedir", {
      userEmail: store.state.pan.currentPan, // 这里是当前登录用户的邮箱
      path: newFolderPath, // 这里是新文件夹的路径
    });

    if (response.data.message === "successfully made new dir") {
      console.log("文件夹创建成功");

      // 在 tableData 中添加新文件夹
      tableData.value.push({
        fileName: folderName,
        lastUpdateTime: new Date().toLocaleString(),
        fileSize: 0,
        fileType: "dir",
      });

      // 关闭新建文件夹的对话框
      newFolderDialogVisible.value = false;
    } else {
      console.error("文件夹创建失败");
    }
  } catch (error) {
    console.error("创建文件夹失败：", error);
  }
};
//打开上传对话框
const openUploadDialog = (record) => {
  uploadDialogVisible.value = true;
};
// 这只是测试组件在前端能否正常显示的代码
// const uploadFile = (option) => {
//   const { onProgress, onError, onSuccess, fileItem, name } = option;
//
//   console.log("Upload file: " + fileItem.name);
//   console.log(fileItem);
//
//   // 更新 tableData 的值
//   tableData.value.push({
//     fileName: fileItem.name,
//     lastUpdateTime: new Date().toLocaleString(),
//     fileSize: fileItem.size,
//   });
//
//   // 模拟文件上传成功，你可以在这里加入真实的上传代码
//   onSuccess("Upload successful");
// };

// 上传文件
const uploadFile = async (option) => {
  console.log("begin upload");
  const { onProgress, onError, onSuccess, fileItem, name } = option;

  console.log("Upload file: " + fileItem.name);
  console.log(fileItem);
  const folder = currentFolder.value; // 获取本地状态
  console.log("uploadFile中，folder是：", folder, "name是：", fileItem.name);
  console.log("他们的类型是：", typeof folder, typeof fileItem.name);
  const newFilePath = join(folder, fileItem.name);
  try {
    console.log(
      "uploadFile中，userEmail是：",
      store.state.pan.currentPan,
      "newFilePath是：",
      newFilePath
    );
    // 验证路径是否可用
    const response = await api.post("/user/uploadGetPath", {
      userEmail: store.state.pan.currentPan,
      path: newFilePath, // FIXME 这里应该是文件的路径，目前只传文件名
    });

    if (response.data.message === "path available") {
      // 对需要上传的文件进行本地加密
      const formData = new FormData();
      formData.append("fileInput", fileItem.file);
      console.log("fileItem", fileItem);
      const response = await api.post("/user/uploadEncryptFile", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      if (response.data.message === "file encrypted") {
        // 上传文件
        const response = await api.post("/user/confirmUpload");

        if (response.data.message === "successfully uploaded") {
          console.log("文件上传成功");

          // 更新 tableData 的值
          tableData.value.push({
            fileName: fileItem.name,
            lastUpdateTime: new Date().toLocaleString(),
            fileSize: fileItem.size,
            fileType: fileItem.type,
          });

          // 文件上传成功
          onSuccess("Upload successful");
        } else {
          console.error("文件上传失败");
          onError("Upload failed");
        }
      } else {
        console.error("文件加密失败");
        onError("Encryption failed");
      }
    } else {
      console.error("路径不可用");
      onError("Path not available");
    }
  } catch (error) {
    console.error("上传文件失败：", error);
    onError("Upload failed");
  }
  console.log("end upload");
};
const deleteFile = async (record) => {
  console.log("Delete file: " + record.fileName);

  const pan = store.state.pan.currentPan;
  const folder = currentFolder.value; // 获取本地状态
  console.log("deleteFile中，folder是：", folder, "name是：", record.fileName);
  const newFilePath = join(folder, record.fileName);
  console.log("我们要传这个给后端删除：", newFilePath);
  try {
    // 发送删除文件的请求
    const response = await api.post("/user/delete", {
      userEmail: pan, // 这里是当前登录用户的邮箱
      path: newFilePath, // 这里应该是文件的路径，我假设它和文件名相同
    });

    if (response.data.message === "successfully deleted") {
      console.log("文件删除成功");

      // 从 tableData 中删除该文件
      const index = tableData.value.findIndex(
        (item) => item.fileName === record.fileName
      );
      if (index !== -1) {
        tableData.value.splice(index, 1);
      }
    } else {
      console.error("文件删除失败");
    }
  } catch (error) {
    console.error("删除文件失败：", error);
  }
};

const downloadFile = async (record) => {
  console.log("下载: " + record.fileName);
  const pan = store.state.pan.currentPan;
  console.log("下载中，当前的pan是:" + pan);
  const folder = currentFolder.value; // 获取本地状态
  const deleteFilePath = join(folder, record.fileName);
  try {
    // 发送下载文件的请求
    const response = await api.post("/user/download", {
      userEmail: pan, // 这里是当前登录用户的邮箱
      path: deleteFilePath,
    });

    if (response.data.status === "success") {
      console.log("文件下载成功");
      // 这里可以添加一些其他的前端操作，例如显示一个通知或者其他的反馈给用户
    } else {
      console.error("文件下载失败");
    }
  } catch (error) {
    console.error("下载文件失败：", error);
  }
};

//获取文件列表函数,给后端的userEmail 传入当前的pan来决定
//如果要访问个人网盘就是邮箱，否则是群组id
const getFileList = async (folderName = "") => {
  try {
    console.log("getFileList中：", store.state.pan.currentPan);
    console.log("getFileList中：", folderName);
    const response = await api.post("/user/filelist", {
      userEmail: store.state.pan.currentPan,
      path: folderName, // 使用传入的文件夹名称
    });
    if (response.status === 200) {
      tableData.value = response.data.map((item) => {
        return {
          fileName: item.name,
          lastUpdateTime: new Date(item.time * 1000).toLocaleString(),
          fileSize: item.size ?? 0,
          fileType: item.type ?? "file",
        };
      });
    }
  } catch (error) {
    console.error("获取文件列表失败：", error);
  }
};
const navigateToFolder = (folderName) => {
  const newPath = join(currentFolder.value, folderName);
  currentFolder.value = newPath; // 更新本地状态
  router.push(`/pan/${newPath}`);
};

const navigateBack = () => {
  const parentFolder = dirname(currentFolder.value); // 使用 `dirname` 来获取父目录
  currentFolder.value = parentFolder; // 更新本地状态
  router.push(`/pan/${parentFolder}`);
};

watch(
  () => route.params.folderName,
  (newFolderName, oldFolderName) => {
    // 只有当路由到不同的 "folderName" 时才获取新的文件列表
    if (newFolderName !== oldFolderName) {
      currentFolder.value = newFolderName; // 更新本地状态
      getFileList(newFolderName);
    }
  }
);
//todo 未来可能实现的功能：
// const search = () => {
//   console.log("Search button clicked, search value: " + fileNameFuzzy.value);
// };

//下面是前端逻辑js，与python层无关：
const openModal = () => {
  newFolderDialogVisible.value = true;
};

const handleClose = (done) => {
  // 清除输入框的内容
  newFolderName.value = "";
  done();
};
const hoverDownload = ref(false);
const hoverDelete = ref(false);
</script>
<style scoped>
.a-space-container {
  margin-left: 20px; /* 左侧空白 */
  margin-top: 20px; /* 上侧空白 */
}
.common-layout,
a-layout {
  display: flex;
  flex-direction: column; /* 垂直布局 */
  height: 100vh; /* 占据全屏 */
}
.a-layout-content {
  flex: 1; /* 占据多余空间 */
  display: flex;
  flex-direction: column; /* 垂直布局 */
}

.table-content {
  height: calc(100vh - 80px); /* 80px = 60px (top height) + 20px (top margin) */
  flex: 1; /* 占据多余空间 */
}
</style>
