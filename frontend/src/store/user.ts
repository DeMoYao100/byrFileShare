import axios from "axios";
import ACCESS_ENUM from "@/access/accessEnum";
import { StoreOptions } from "vuex";
import api from "@/axios-config"; //

export default {
  namespaced: true,
  state: () => ({
    loginUser: {
      userEmail: "未登录",
      userRole: ACCESS_ENUM.NOT_LOGIN,
    },
  }),
  actions: {
    async getLoginUser({ commit, state }) {
      try {
        const response = await api.post("/user/getLoginUser");
        const res = response.data;
        if (res.code === 200) {
          commit("updateUser", {
            ...state.loginUser,
            userEmail: res.email, // 添加这一行
            userRole: ACCESS_ENUM.USER,
          });
        } else {
          commit("updateUser", {
            ...state.loginUser,
            userRole: ACCESS_ENUM.NOT_LOGIN,
          });
        }
      } catch (error) {
        console.error("Error fetching login user:", error);
        commit("updateUser", {
          ...state.loginUser,
          userRole: ACCESS_ENUM.NOT_LOGIN,
        });
      }
    },
  },
  mutations: {
    updateUser(state, payload) {
      state.loginUser = payload;
    },
  },
} as StoreOptions<any>;
