import { StoreOptions } from "vuex";

export default {
  namespaced: true,
  state: () => ({
    //"personal" 或者是群盘的id
    currentPan: "personal",
  }),
  mutations: {
    setCurrentPan(state, payload) {
      state.currentPan = payload;
    },
  },
} as StoreOptions<any>;
