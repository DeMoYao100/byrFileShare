// src/axios-config.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8081", // 你的 Flask 后端地址
});

export default api;
