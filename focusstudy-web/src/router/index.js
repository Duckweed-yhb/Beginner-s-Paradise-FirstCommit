import { createRouter, createWebHistory } from "vue-router";
import TasksView from "../views/TasksView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/tasks" },
    { path: "/tasks", component: TasksView },
    { path: "/timer", component: () => import("../views/TimerView.vue") },
    { path: "/stats", component: () => import("../views/StatsView.vue") },
  ],
});

export default router;
