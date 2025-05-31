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
          :class="{ 'router-link-active': isHome }">
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
            to="/editar"
            class="nav-link sub-link"
            :class="{ 'router-link-active': isEdit }">
            <span class="nav-text">Visualizar/Editar Veículo</span>
          </router-link>
        </div>
      </nav>
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
const isHome = computed(() => route.path === "/");
const isAdd = computed(() => route.path === "/add");
const isEdit = computed(() => route.path === "/editar");
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
}

.sidebar-nav {
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
    margin-left: 24px;
    gap: 10px;

    .sub-link {
      padding: 8px 24px;
      font-size: 13px;
    }
  }
}

.main-content {
  flex-grow: 1;
  padding: 20px;
}
</style>
