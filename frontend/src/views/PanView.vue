<template>
  <div class="common-layout">
    <a-layout>
      <a-layout-header>
        <div class="top">
          <div class="top-op">
            <a-space>
              <div class="btn">
                <a-upload :custom-request="uploadFile"> </a-upload>
              </div>
              <!--     todo 新建文件夹的前端         -->
              <div>
                <a-button type="primary" @click="openModal"
                  >新建文件夹</a-button
                >
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
      </a-layout-header>
      <a-layout-content>
        <div>
          <div v-if="tableData && tableData.length > 0">
            <a-table :data="tableData" :hoverable="true">
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
                <a-table-column
                  title="大小"
                  data-index="fileSize"
                ></a-table-column>
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
          </div>
          <div v-else>
            <h3>网盘空空如也</h3>
          </div>
        </div>
      </a-layout-content>
    </a-layout>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/axios-config";

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

const newFolder = () => {
  // 新建文件夹
  console.log("New folder button clicked");
};

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

const deleteFile = (record) => {
  console.log("Delete file: " + record.fileName);
};

const downloadFile = (record) => {
  console.log("Download file: " + record.fileName);
};

//获取文件列表函数
const getFileList = async () => {
  try {
    const response = await api.post("/user/filelist", {
      path: ".",
    });
    if (response.status === 200) {
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
