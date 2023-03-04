import { createRouter, createWebHistory } from "vue-router";
import DashboardView from "../views/DashboardView.vue";
import store from "../store/index";
import checkAuthToken from "@/helpers/checkAuthToken";
import PageNotFound from "@/components/PageNotFound.vue";

const routes = [
  {
    path: "/",
    name: "dashboard",
    meta: { requiresAuth: true },
    component: DashboardView,
  },
  {
    path: "/summary",
    name: "summary",
    meta: { requiresAuth: true },
    component: () => import("../views/SummaryView.vue"),
  },
  {
    path: "/list/add",
    name: "add_list",
    meta: { requiresAuth: true },
    component: () => import("../views/ListManagementView.vue"),
  },
  {
    path: "/list/edit/:id",
    name: "edit_list",
    meta: { requiresAuth: true },
    component: () => import("../views/ListManagementView.vue"),
  },
  {
    path: "/list/delete/:id",
    name: "delete_list",
    meta: { requiresAuth: true },
    component: () => import("../views/ListManagementView.vue"),
  },
  {
    path: "/card/:id/add",
    name: "add_card",
    meta: { requiresAuth: true },
    component: () => import("../views/CardManagementView.vue"),
  },
  {
    path: "/card/:list_id/edit/:card_id",
    name: "edit_card",
    meta: { requiresAuth: true },
    component: () => import("../views/CardManagementView.vue"),
  },
  {
    path: "/login",
    name: "login",
    meta: { requiresAuth: false },
    component: () => import("../views/LoginView.vue"),
  },
  {
    path: "/register",
    name: "register",
    meta: { requiresAuth: false },
    component: () => import("../views/RegisterView.vue"),
  },
  { path: "/:pathMatch(.*)*", name: "notFound", component: PageNotFound },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const isAuthenticated = checkAuthToken();

  store.dispatch("changeAuthState", {
    value: isAuthenticated,
  });

  if (to.meta.requiresAuth && !isAuthenticated) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    next({ name: "login" });
  } else if (
    !to.meta.requiresAuth &&
    isAuthenticated &&
    (to.name === "login" || to.name === "register")
  ) {
    next({ name: "dashboard" });
  } else next();
});

export default router;
