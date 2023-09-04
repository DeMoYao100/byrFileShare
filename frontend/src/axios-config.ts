// src/axios-config.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5001", // 你的 Flask 后端地址
  withCredentials: true, // 添加这一行
});

export default api;
