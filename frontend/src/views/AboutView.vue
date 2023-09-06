<script setup>
import { reactive } from "vue";

const groupDrives = reactive({
  value: [{ id: "test1" }, { id: "test2" }, { id: "test3" }],
});
console.log("定义的value是", groupDrives.value);
</script>

<template>
  <div>
    <ul>
      <li v-for="drive in groupDrives.value" :key="drive.id">
        {{ drive.id }}
      </li>
    </ul>
  </div>
</template>
