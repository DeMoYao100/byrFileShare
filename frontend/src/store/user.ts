import axios from "axios";
import ACCESS_ENUM from "@/access/accessEnum";
import { StoreOptions } from "vuex";

export default {
  namespaced: true,
  state: () => ({
    loginUser: {
      userName: "未登录",
      userRole: ACCESS_ENUM.NOT_LOGIN,
    },
  }),
  actions: {
    async getLoginUser({ commit, state }) {
      try {
        const response = await axios.get(
          "http://localhost:????/api/user/get/login"
        );
        const res = response.data;
        if (res.code === 0) {
          commit("updateUser", {
            ...state.loginUser,
            userRole: ACCESS_ENUM.USER,
            // 其他你需要更新的字段
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
