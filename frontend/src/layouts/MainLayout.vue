<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <!-- Codificar o menu -->
    </aside>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 248px;
  background-color: $color-bg-sidebar;
  padding: 20px;
  color: $color-light-text;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
}
</style>
