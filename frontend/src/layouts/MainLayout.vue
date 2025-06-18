<template>
  <div class="dashboard-layout">
    <!-- Sidebar: Menu lateral de naveção -->
    <aside class="sidebar">
      <!-- Container com a Logo do sistema "PrimeCar" -->
      <div class="logo-container">
        <!-- Logo PrimeCar -->
        <img
          src="/images/logo-primecar.jpg"
          alt="Logo PrimeCar"
          class="logo" />
      </div>

      <!-- Navegação da Sidebar -->
      <nav class="sidebar-nav">
        <!-- 
          Link "Dashboard" (Home Page)
          Usando router-link com slot customizado para maior controle sobre o elemento renderizado
        -->
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

        <!-- 
          Link "Modelos" - Menu expansível
          Controla a abertura/fechamento do submenu correspondente  
        -->
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
              keyboard_arrow_down
            </span>
          </div>
        </router-link>

        <!-- 
          Submenu Modelos - Aparece apenas quando o menu 'modelos' está aberto
        -->
        <div
          class="sub-nav-link"
          v-show="openMenu === 'modelos'">
          <router-link
            to="/models"
            class="nav-link sub-link"
            :class="{ 'router-link-active': route.path === '/modelos' }">
            <span class="nav-text">Dashboard Modelos</span>
          </router-link>

          <router-link
            to="/models/add"
            class="nav-link sub-link"
            :class="{ 'router-link-active': route.path === '/modelos/add' }">
            <span class="nav-text">Cadastro de Modelos</span>
          </router-link>
        </div>

        <!-- 
          Menu Carros - Outro menu expansível
          Similar ao menu "Modelos" em estrutura
        -->
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
              keyboard_arrow_down
            </span>
          </div>
        </router-link>

        <!-- 
          Submenu Carros - Opções específicas para gestão de veículos
          Visível apenas quando o menu 'carros' está aberto
        -->
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

      <!-- 
        Footer da Sidebar - Informações de copyright e logo secundário
        Posicionado na parte inferior usando margin-top: auto
      -->
      <div class="sidebar-footer">
        <p class="footer-text">PrimeCar - Copyright © 2025</p>
        <img
          src="/images/logo-mallg-sistemas.jpg"
          alt="Logo MALLG Sistemas"
          class="mallg-logo" />
      </div>
    </aside>

    <!-- 
      Conteúdo Principal - Área onde o conteúdo da página será renderizado
      Formado pelo Header fixo e a view de rota dinâmica
    -->
    <main class="main-content">
      <HeaderComponent />
      <!-- Router-view renderiza o componente correspondente à rota atual -->
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
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

// Verificar a rota atual e abrir o menu apropriado
const setInitialMenuState = () => {
  // Se estiver na raiz ou em páginas relacionadas a carros, abra o menu de carros
  if (
    route.path === "/" ||
    route.path.startsWith("/add") ||
    route.path.startsWith("/edit")
  ) {
    openMenu.value = "carros";
  }
  // Se estiver em páginas de modelos, abra o menu de modelos
  else if (route.path.startsWith("/models") || route.path === "/modelos") {
    openMenu.value = "modelos";
  }
};

// Executar ao montar o componente
onMounted(() => {
  setInitialMenuState();
});

// Observar mudanças na rota para atualizar o estado do menu
watch(
  () => route.path,
  () => setInitialMenuState()
);
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

/* Layout principal com sidebar e conteúdo */
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

/* Siderbar Styles */
.sidebar {
  width: 248px;
  min-width: 248px;
  background-color: $color-bg-sidebar;
  padding-top: 20px;
  color: $color-light-text;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
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
      transition: transform 0.3s ease;
      transform: rotate(0);

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

  .footer-text {
    font-size: 12px;
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
