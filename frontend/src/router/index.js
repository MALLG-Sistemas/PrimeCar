import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue"; // Importação do de HomeView (página inicial)

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  // Rotas a serem adicionadas
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
