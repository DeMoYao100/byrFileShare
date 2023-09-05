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
            <!--     todo 新建文件夹的前端         -->
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
              </a-modal>
            </div>
            <!--     todo 这个在未来实现         -->
            <a-button type="primary"> 批量删除 </a-button>
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
          :scroll="{ y: 200 }"
        >
          <template #columns>
            <!-- todo 行选择器-->
            <a-table-column
              title="文件名"
              data-index="fileName"
            ></a-table-column>
            <a-table-column
              title="修改时间"
              data-index="lastUpdateTime"
            ></a-table-column>
            <a-table-column title="大小" data-index="fileSize"></a-table-column>
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
//todo 路径管理问题
import { ref, onMounted } from "vue";
import api from "@/axios-config";
import { useStore } from "vuex";
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

const newFolder = () => {
  // 新建文件夹
  console.log("New folder button clicked");
};
//打开上传对话框
const openUploadDialog = (record) => {
  uploadDialogVisible.value = true;
};
// 这只是测试组件在前端能否正常显示的代码
const uploadFile = (option) => {
  const { onProgress, onError, onSuccess, fileItem, name } = option;

  console.log("Upload file: " + fileItem.name);
  console.log(fileItem);

  // 更新 tableData 的值
  tableData.value.push({
    fileName: fileItem.name,
    lastUpdateTime: new Date().toLocaleString(),
    fileSize: fileItem.size,
  });

  // 模拟文件上传成功，你可以在这里加入真实的上传代码
  onSuccess("Upload successful");
};

// 上传文件
// const uploadFile = async (option) => {
//   const { onProgress, onError, onSuccess, fileItem, name } = option;
//
//   console.log("Upload file: " + fileItem.name);
//   console.log(fileItem);
//   const store = useStore();
//   const userEmail = store.state.user?.loginUser?.userEmail ?? "未登录";
//   try {
//     // 验证路径是否可用
//     const response = await api.post("/user/uploadGetPath", {
//       userEmail: userEmail,
//       path: ".", // todo 这里应该是用户选择的路径
//     });
//
//     if (response.data.message === "path available") {
//       // 对需要上传的文件进行本地加密
//       const formData = new FormData();
//       formData.append("fileInput", fileItem);
//       const response = await api.post("/user/uplaodEncryptFile", formData, {
//         headers: {
//           "Content-Type": "multipart/form-data",
//         },
//       });
//
//       if (response.data.message === "file encrypted") {
//         // 上传文件
//         const response = await api.post("/user/confirmUpload");
//
//         if (response.data.message === "successfully uploaded") {
//           console.log("文件上传成功");
//
//           // 更新 tableData 的值
//           tableData.value.push({
//             fileName: fileItem.name,
//             lastUpdateTime: new Date().toLocaleString(),
//             fileSize: fileItem.size,
//           });
//
//           // 文件上传成功
//           onSuccess("Upload successful");
//         } else {
//           console.error("文件上传失败");
//           onError("Upload failed");
//         }
//       } else {
//         console.error("文件加密失败");
//         onError("Encryption failed");
//       }
//     } else {
//       console.error("路径不可用");
//       onError("Path not available");
//     }
//   } catch (error) {
//     console.error("上传文件失败：", error);
//     onError("Upload failed");
//   }
// };
const deleteFile = async (record) => {
  console.log("Delete file: " + record.fileName);

  const store = useStore();
  const userEmail = store.state.user?.loginUser?.userEmail ?? "未登录";

  try {
    // 发送删除文件的请求
    const response = await api.post("/user/delete", {
      userEmail: userEmail, // 这里是当前登录用户的邮箱
      path: record.fileName, // 这里应该是文件的路径，我假设它和文件名相同
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
  const store = useStore();
  const userEmail = store.state.user?.loginUser?.userEmail ?? "未登录";
  console.log("下载中:" + userEmail);

  try {
    // 发送下载文件的请求
    const response = await api.post("/user/download", {
      userEmail: userEmail, // 这里是当前登录用户的邮箱
      path: record.fileName, // 这里应该是文件的路径，我假设它和文件名相同
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

//获取文件列表函数
const getFileList = async () => {
  const store = useStore();
  const userEmail = store.state.user?.loginUser?.userEmail ?? "未登录";
  console.log(" 5 : " + userEmail);
  try {
    const response = await api.post("/user/filelist", {
      userEmail: userEmail, // 这里应该是当前登录用户的邮箱
      path: ".",
    });
    if (response.status === 200) {
      console.log(" 4 : " + response.data);
      tableData.value = response.data.map((item) => {
        return {
          fileName: item.name,
          lastUpdateTime: new Date(item.time * 1000).toLocaleString(),
          fileSize: item.size ?? 0,
        };
      });
    }
  } catch (error) {
    console.error("获取文件列表失败：", error);
  }
};
//todo 未来可能实现的功能：
// const search = () => {
//   console.log("Search button clicked, search value: " + fileNameFuzzy.value);
// };

//下面是前端逻辑js，与python层无关：
const openModal = () => {
  newFolderDialogVisible.value = true;
};

const handleClose = (done) => {
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
  flex: 1; /* 占据多余空间 */
}
</style>
