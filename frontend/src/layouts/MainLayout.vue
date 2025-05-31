<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <!-- Logo do Sistema PrimeCar -->
      <div class="logo-container">
        <img
          src="../../images/logo-primecar.jpg"
          alt="Logo PrimeCar"
          class="logo" />
      </div>

      <!-- Menu de Navegação da Sidebar -->
      <nav class="sidebar-nav">
        <!-- Dashboard -->
        <router-link
          to="/"
          class="nav-link router-link-active">
          <span class="material-symbols-outlined icon-link-nav">cottage</span>
          <span class="nav-text">Dashboard</span>
        </router-link>

        <!-- Modelos -->
        <router-link
          to="/modelos"
          class="nav-link">
          <span class="material-symbols-outlined icon-link-nav"
            >traffic_jam</span
          >
          <span class="nav-text">Modelos</span>
        </router-link>

        <!-- Carros -->
        <router-link
          to="/"
          class="nav-link"
          :class="{ 'router-link-active': isCarrosActive }"
          active-class="">
          <span class="material-symbols-outlined icon-link-nav"
            >directions_car</span
          >
          <span class="nav-text">Carros</span>
        </router-link>

        <!-- Submenu de Carros -->
        <div class="sub-nav-link">
          <router-link
            to="/"
            class="nav-link sub-link"
            :class="{ 'router-link-active': isHome }"
            active-class="">
            <span class="nav-text">Lista de Veículos</span>
          </router-link>
          <router-link
            to="/add"
            class="nav-link sub-link"
            :class="{ 'router-link-active': isAdd }">
            <span class="nav-text">Adicionar Veículo</span>
          </router-link>
          <router-link
            to="/edit"
            class="nav-link sub-link"
            :class="{ 'router-link-active': isEdit }">
            <span class="nav-text">Visualizar/Editar Veículo</span>
          </router-link>
        </div>
      </nav>

      <!-- Footer da Sidebar -->
      <div class="sidebar-footer">
        <img
          src="../../public/images/logo-mallg-sistemas.jpg"
          alt="Logo MALLG Sistemas"
          class="mallg-logo" />
        <p class="footer-text">Copyright © 2025 PrimeCar</p>
      </div>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

/**
 * isHome:
 * Uma propriedade computada que retorna verdadeiro se o caminho da rota atual for a página inicial ("/").
 *
 * isAdd:
 * Uma propriedade computada que retorna verdadeiro se o caminho da rota atual corresponder à página "adicionar" ("/add").
 *
 * isEdit:
 * Uma propriedade computada que retorna verdadeiro se o caminho da rota atual corresponder à página "editar" ("/edit").
 */
const isHome = computed(() => route.path === "/");
const isAdd = computed(() => route.path === "/add");
const isEdit = computed(() => route.path === "/edit");

const isCarrosActive = computed(() => {
  return ["/", "/add", "/edit"].includes(route.path);
});
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 248px;
  background-color: $color-bg-sidebar;
  padding-top: 20px;
  color: $color-light-text;
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-top: 24px;
  gap: 15px;

  .nav-link {
    display: flex;
    align-items: center;
    padding: 12px 24px;
    text-decoration: none;
    color: inherit;
    font-size: 14px;

    &.router-link-active {
      background-color: $color-primary;
    }

    .icon-link-nav {
      font-size: 24px;
      margin-right: 16px;
    }
  }

  .sub-nav-link {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .sub-link {
      padding: 8px 36px;
      font-size: 13px;
    }
  }
}

/* Footer da Sidebar */
.sidebar-footer {
  text-align: center;
  margin-top: 50px;

  p {
    font-size: 12px;
    margin-bottom: 32px;
  }

  .mallg-logo {
    max-width: 100%;
  }
}

.main-content {
  flex-grow: 1;
  padding: 20px;
}
</style>
