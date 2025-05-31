<template>
  <div class="dashboard-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <!-- Logo -->
      <div class="logo-container">
        <img
          src="/images/logo-primecar.jpg"
          alt="Logo PrimeCar"
          class="logo" />
      </div>

      <!-- Navegação da Sidebar -->
      <nav class="sidebar-nav">
        <!-- Link "Dashboard" (Home Page) -->
        <router-link
          to="/"
          custom
          v-slot="{ navigate, isActive }">
          <div
            class="nav-link"
            :class="{ 'router-link-active': isActive }"
            @click="navigate">
            <span class="nav-link-icon material-symbols-outlined">cottage</span>
            <span class="nav-text">Dashboard</span>
          </div>
        </router-link>

        <!-- Link "Modelos" -->
        <router-link
          to="/modelos"
          custom>
          <div
            class="nav-link"
            :class="{ 'router-link-active': openMenu === 'modelos' }"
            @click="() => toggleMenu('modelos')">
            <span class="nav-link-icon material-symbols-outlined"
              >traffic_jam</span
            >
            <span class="nav-text">Modelos</span>
            <span
              class="arrow-icon material-symbols-outlined"
              :class="{ open: openMenu === 'modelos' }">
              {{
                openMenu === "modelos"
                  ? "keyboard_arrow_up"
                  : "keyboard_arrow_down"
              }}
            </span>
          </div>
        </router-link>

        <!-- Submenu Modelos -->
        <div
          class="sub-nav-link"
          v-show="openMenu === 'modelos'">
          <router-link
            to="/modelos"
            class="nav-link sub-link"
            :class="{ 'router-link-active': route.path === '/modelos' }">
            <span class="nav-text">Dashboard Modelos</span>
          </router-link>

          <router-link
            to="/modelos/add"
            class="nav-link sub-link"
            :class="{ 'router-link-active': route.path === '/modelos/add' }">
            <span class="nav-text">Cadastro de Modelos</span>
          </router-link>
        </div>

        <!-- Menu Carros -->
        <router-link
          to="/"
          custom>
          <div
            class="nav-link"
            :class="{ 'router-link-active': openMenu === 'carros' }"
            @click="() => toggleMenu('carros')">
            <span class="nav-link-icon material-symbols-outlined"
              >directions_car</span
            >
            <span class="nav-text">Carros</span>
            <span
              class="arrow-icon material-symbols-outlined"
              :class="{ open: openMenu === 'carros' }">
              {{
                openMenu === "carros"
                  ? "keyboard_arrow_up"
                  : "keyboard_arrow_down"
              }}
            </span>
          </div>
        </router-link>

        <!-- Submenu Carros -->
        <div
          class="sub-nav-link"
          v-show="openMenu === 'carros'">
          <router-link
            to="/"
            class="nav-link sub-link"
            :class="{ 'router-link-active': route.path === '/' }"
            active-class="">
            <span class="nav-text">Lista de Veículos</span>
          </router-link>

          <router-link
            to="/add"
            class="nav-link sub-link"
            :class="{ 'router-link-active': route.path === '/add' }">
            <span class="nav-text">Adicionar Veículo</span>
          </router-link>

          <router-link
            to="/edit"
            class="nav-link sub-link"
            :class="{ 'router-link-active': route.path === '/edit' }">
            <span class="nav-text">Visualizar/Editar Veículo</span>
          </router-link>
        </div>
      </nav>

      <!-- Footer da Sidebar -->
      <div class="sidebar-footer">
        <img
          src="/images/logo-mallg-sistemas.jpg"
          alt="Logo MALLG Sistemas"
          class="mallg-logo" />
        <p class="footer-text">Copyright © 2025 PrimeCar</p>
      </div>
    </aside>

    <!-- Conteúdo Principal -->
    <main class="main-content">
      <HeaderComponent />
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import HeaderComponent from "../components/HeaderComponent.vue";

// Estado reativo para controlar qual menu está aberto
const openMenu = ref("");

// Hook para acessar a rota atual
const route = useRoute();

// Função para alternar abertura de menus
const toggleMenu = (menu) => {
  openMenu.value = openMenu.value === menu ? "" : menu;
};
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

/* Layout principal com sidebar e conteúdo */
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* Siderbar Styles */
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
    cursor: pointer;

    /* Styles para o link ativo */
    &.router-link-active {
      background-color: $color-primary;
    }

    .nav-link-icon {
      font-size: 24px;
      margin-right: 16px;
    }

    .arrow-icon {
      margin-left: auto;
      font-size: 24px;
      transition: transform 0.2s ease;

      &.open {
        transform: rotate(180deg);
      }
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

/* Footer da Sidebar Styles */
.sidebar-footer {
  text-align: center;
  margin-top: auto;

  p {
    font-size: 12px;
    margin-bottom: 32px;
  }

  .mallg-logo {
    max-width: 100%;
  }
}

/* Styles de main content */
.main-content {
  flex-grow: 1;
}
</style>
