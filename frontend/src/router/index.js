import { createRouter, createWebHistory } from "vue-router";
import MainLayout from "../layouts/MainLayout.vue"; // Importação do layout principal (Contendo a Sidebar)

// Rotas da Aplicação
const routes = [
  {
    path: "/",
    component: MainLayout,
    children: [
      // Rotas para Veículos:
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
        path: "edit/:id?",
        name: "Visualizar e Editar Veiculo",
        component: () => import("../views/EditViewVeiculo.vue"),
        meta: { title: "Editar/Visualizar Veiculo" },
        props: true, // Permite passar o parâmetro id como prop para o componente
      },

      // Rotas para Modelos:
      {
        path: "models",
        name: "Modelos",
        component: () => import("../views/AddModelView.vue"),
        meta: { title: "Gerenciamento de Modelos" },
      },
      {
        path: "models/add",
        name: "Add Modelo",
        component: () => import("../views/AddModelView.vue"),
        meta: { title: "Add Modelo" },
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
