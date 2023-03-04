import { createStore } from "vuex";

export default createStore({
  state() {
    return {
      dragStarted: false,
      isAuthenticated: false,
      showExportAlert: false,
      userDetail: null,
    };
  },
  mutations: {
    changeDragStarted(state, value) {
      state.dragStarted = value;
    },
    changeAuthState(state, value) {
      state.isAuthenticated = value;
    },
    changeExportAlertState(state, value) {
      state.showExportAlert = value;
    },
    changeUserDetailState(state, value) {
      state.userDetail = value;
    },
  },
  actions: {
    changeDragStarted(context, payload) {
      context.commit("changeDragStarted", payload.value);
    },
    changeAuthState(context, payload) {
      context.commit("changeAuthState", payload.value);
    },
    changeExportAlertState(context, payload) {
      context.commit("changeExportAlertState", payload.value);
    },
    changeUserDetailState(context, payload) {
      context.commit("changeUserDetailState", payload.value);
    },
  },
  modules: {},
});
