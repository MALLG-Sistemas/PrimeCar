import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "../layouts/MainLayout.vue"; // Importação do layout principal (Contendo a Sidebar)

// Rotas do app
const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      {
        path: "",
        name: "home",
        component: () => import("../views/HomeView.vue"),
        meta: { title: "Home" },
      },
      // Rota 404 - Page Not Found:
      {
        path: "/:catchAll(.*)*",
        name: "NotFound",
        component: () => import("../views/NotFound.vue"),
        meta: { title: "Page Not Found" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
