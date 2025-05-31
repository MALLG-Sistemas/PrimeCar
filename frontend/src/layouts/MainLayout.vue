<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <!-- Logo do Sistema PrimeCar -->
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
          class="nav-link router-link-active">
          <span class="material-symbols-outlined icon-link-nav">cottage</span>
          <span class="nav-text">Dashboard</span>
        </router-link>

        <!-- Link "Modelos" -->
        <router-link
          to="/modelos"
          class="nav-link"
          :class="{ 'router-link-active': isModelsActive }"
          @click.prevent="toggleModelos">
          <span class="material-symbols-outlined icon-link-nav"
            >traffic_jam</span
          >
          <span class="nav-text">Modelos</span>
          <span class="material-symbols-outlined arrow-icon">
            {{ isModelosOpen ? "keyboard_arrow_up" : "keyboard_arrow_down" }}
          </span>
        </router-link>

        <!-- Submenu de Modelos -->
        <div
          class="sub-nav-link"
          v-show="isModelosOpen">
          <router-link
            to="/modelos"
            class="nav-link sub-link"
            :class="{ 'router-link-active': isModelsDashboardActive }">
            <span class="nav-text">Dashboard Modelos</span>
          </router-link>
          <router-link
            to="/modelos/add"
            class="nav-link sub-link"
            :class="{ 'router-link-active': isModelsAddActive }">
            <span class="nav-text">Cadastro de Modelos</span>
          </router-link>
        </div>

        <!-- Link "Carros" -->
        <router-link
          to="/"
          class="nav-link"
          :class="{ 'router-link-active': isCarrosActive }"
          active-class=""
          @click.prevent="toggleCarros">
          <span class="material-symbols-outlined icon-link-nav"
            >directions_car</span
          >
          <span class="nav-text">Carros</span>
          <span class="material-symbols-outlined arrow-icon">
            {{ isCarrosOpen ? "keyboard_arrow_up" : "keyboard_arrow_down" }}
          </span>
        </router-link>

        <!-- Submenu de Carros -->
        <div
          class="sub-nav-link"
          v-show="isCarrosOpen">
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
          src="/images/logo-mallg-sistemas.jpg"
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
import { ref, computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

// Propriedades computadas para verificar a rota ativa atual
const isHome = computed(() => route.path === "/");
const isAdd = computed(() => route.path === "/add");
const isEdit = computed(() => route.path === "/edit");

// Ativa o menu "Carros" quando a rota for uma das definidas
const isCarrosActive = computed(() => {
  return ["/", "/add", "/edit"].includes(route.path);
});

// Ativa o menu "Modelos" se o caminho iniciar com "/modelos"
const isModelsActive = computed(() => route.path.startsWith("/modelos"));
const isModelsDashboardActive = computed(() => route.path === "/modelos");
const isModelsAddActive = computed(() => route.path === "/modelos/add");

// Estados reativos para controle de exibição dos submenus
const isCarrosOpen = ref(false);
const isModelosOpen = ref(false);

// Função genérica para alternar a abertura de um menu e fechar o outro
function toggleMenu(currentMenu, otherMenu) {
  currentMenu.value = !currentMenu.value;
  if (currentMenu.value) {
    otherMenu.value = false;
  }
}

// Funções de alternância específicas para cada submenu
function toggleCarros() {
  toggleMenu(isCarrosOpen, isModelosOpen);
}

function toggleModelos() {
  toggleMenu(isModelosOpen, isCarrosOpen);
}
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

    /* Styles para o link ativo */
    &.router-link-active {
      background-color: $color-primary;
    }

    .icon-link-nav {
      font-size: 24px;
      margin-right: 16px;
    }

    .arrow-icon {
      margin-left: auto;
      font-size: 24px;
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
  margin-top: 50px;

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
  padding: 20px;
}
</style>
