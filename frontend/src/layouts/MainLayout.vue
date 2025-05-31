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
        <router-link
          to="/"
          class="nav-link">
          <span class="material-symbols-outlined icon-link-nav">cottage</span>
          <span class="nav-text">Dashboard</span>
        </router-link>
        <router-link
          to="/modelos"
          class="nav-link">
          <span class="material-symbols-outlined icon-link-nav"
            >traffic_jam</span
          >
          <span class="nav-text">Modelos</span>
        </router-link>
      </nav>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup></script>

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
}

.main-content {
  flex-grow: 1;
  padding: 20px;
}
</style>
