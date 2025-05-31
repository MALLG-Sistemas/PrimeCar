<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="logo-container">
        <img
          src="../../images/logo-primecar.jpg"
          alt="Logo PrimeCar"
          class="logo" />
      </div>
      <!-- Codificar o menu -->
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

.main-content {
  flex-grow: 1;
  padding: 20px;
}
</style>
