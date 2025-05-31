import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "../layouts/MainLayout.vue"; // Importação do layout principal (Contendo a Sidebar)

// Rotas da Aplicação
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
      {
        path: "add",
        name: "Add Veiculo",
        component: () => import("../views/AddVeiculo.vue"),
        meta: { title: "Add Veiculo" },
      },
      {
        path: "edit",
        name: "Editar Veiculo",
        component: () => import("../views/EditVeiculo.vue"),
        meta: { title: "Editar Veiculo" },
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
