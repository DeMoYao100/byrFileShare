<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <div class="top">
          <div class="top-op">
            <div class="btn">
              <el-upload
                :show-file-list="false"
                :with-credentials="true"
                :multiple="true"
                :http-request="uploadFile"
                :accept="fileAccept"
              >
                <el-button type="primary">
                  <span class="iconfont icon-upload"></span>
                  上传
                </el-button>
              </el-upload>
            </div>
            <el-button
              class="mr-3"
              type="success"
              @click="newFolderDialogVisible = true"
            >
              <span class="iconfont icon-folder-add"></span>
              新建文件夹
            </el-button>
            <el-dialog
              title="新建文件夹"
              v-model:visible="newFolderDialogVisible"
              width="30%"
              :before-close="handleClose"
            >
              <el-input
                v-model="newFolderName"
                placeholder="请输入文件夹名称"
              ></el-input>
              <span class="dialog-footer">
                <el-button @click="newFolderDialogVisible = false"
                  >取 消</el-button
                >
                <el-button type="primary" @click="createFolder"
                  >确 定</el-button
                >
              </span>
            </el-dialog>
            <el-button type="danger">
              <span class="iconfont icon-del"></span>
              批量删除
            </el-button>
            <el-input
              clearable
              placeholder="输入文件名搜索"
              v-model="fileNameFuzzy"
              @keyup.enter="search"
            >
              <template #suffix>
                <i class="iconfont icon-search" @click="search"></i>
              </template>
            </el-input>
          </div>
        </div>
      </el-header>
      <el-main class="content">
        <div>
          <div v-if="tableData && tableData.length > 0">
            <el-table
              :data="tableData"
              header-row-class-name="table-header-row"
              highlight-current-row
            >
              <el-table-column
                type="index"
                width="50"
                align="center"
              ></el-table-column>
              <el-table-column
                type="selection"
                width="50"
                align="center"
              ></el-table-column>
              <el-table-column label="文件名" prop="fileName"></el-table-column>
              <el-table-column
                label="修改时间"
                prop="lastUpdateTime"
              ></el-table-column>
              <el-table-column label="大小" prop="fileSize"></el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button
                    size="mini"
                    type="danger"
                    @click="deleteFile(scope.$index)"
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
            <el-pagination
              background
              :page-sizes="[15, 30, 50, 100]"
              :page-size="pageSize"
              v-model:current-page="currentPage"
              layout="total, sizes, prev, pager, next, jumper"
              style="text-align: right"
            >
            </el-pagination>
          </div>
          <div v-else>
            <h3>网盘空空如也</h3>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "@/axios-config";
import { ElMessage } from "element-plus";

import {
  ElUpload,
  ElTable,
  ElTableColumn,
  ElPagination,
  ElDialog,
  ElInput,
  ElButton,
} from "element-plus";

onMounted(async () => {
  await getFileList();
});

const fileAccept = ref("*");
const fileNameFuzzy = ref("");
const currentPage = ref(1);
const pageSize = ref(15);
const newFolderDialogVisible = ref(false);
const newFolderName = ref("");

interface FileData {
  fileName: string;
  lastUpdateTime: string;
  fileSize: number;
}

const tableData = ref<FileData[]>([]); // 假设 FileData 是你定义的接口

// 获取文件列表函数
const getFileList = async () => {
  try {
    const response = await api.post("/user/filelist", {
      path: ".",
    });
    if (response.status === 200) {
      tableData.value = response.data.map((item: any) => {
        return {
          fileName: item.name,
          lastUpdateTime: new Date(item.time * 1000).toLocaleString(), // 假设时间戳是秒级
          fileSize: item.size ?? 0, // 对于文件夹，可能没有 size
        };
      });
    }
  } catch (error) {
    console.error("获取文件列表失败：", error);
  }
};

const addFile = async (fileData: any) => {
  console.log(fileData.file);
};

const newFolder = () => {
  console.log("New folder button clicked");
};

const search = () => {
  console.log("Search button clicked, search value: " + fileNameFuzzy.value);
};

const loadDataList = () => {
  console.log("Load data list");
};
// 这是测试，只是显示到前端，不需要使用
// const uploadFile = async (fileData: any) => {
//   console.log("Upload file: " + fileData.file.name);
//   tableData.value.push({
//     fileName: fileData.file.name,
//     lastUpdateTime: new Date().toLocaleString(),
//     fileSize: fileData.file.size,
//   });
//   await getFileList(); // 重新获取文件列表
// };
const uploadFile = async (uploadRequest: any) => {
  const { file, onSuccess, onError } = uploadRequest;
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await api.post("/user/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    if (response.status === 200) {
      ElMessage.success("文件上传成功");
      onSuccess(response.data);
    } else {
      ElMessage.error("文件上传失败");
      onError(new Error("File upload failed"));
    }
  } catch (error) {
    ElMessage.error("文件上传失败");
    onError(error);
  }
};
const createFolder = async () => {
  console.log("Create folder: " + newFolderName.value);
  tableData.value.push({
    fileName: newFolderName.value,
    lastUpdateTime: new Date().toLocaleString(),
    fileSize: 0,
  });
  newFolderDialogVisible.value = false;
  await getFileList(); // 重新获取文件列表
};

const handleClose = (done: any) => {
  done();
};

const deleteFile = (index: number) => {
  console.log("Delete file: " + tableData.value[index].fileName);
  tableData.value.splice(index, 1);PanView.vuePanView.vue
};
</script>

<style scoped>
.common-layout {
  padding: 0 20px;
  height: calc(100vh - 300px);
  overflow-y: auto;
}

.top {
  margin-top: 20px;
}

.top .top-op {
  display: flex;
  align-items: center;
}

.top .top-op .btn {
  margin-right: 10px;
}

.top .top-op .el-button {
  margin-right: 10px;
}

.content {
  padding: 10px;
}
</style>
