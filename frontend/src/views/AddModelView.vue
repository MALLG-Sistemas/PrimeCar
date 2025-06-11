<template>
  <section class="add-model__section">
    <header class="add-model__header">
      <h1 class="add-model__title">Página em Codificação...</h1>
    </header>
  </section>
</template>

<script setup></script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

.add-model__section {
  padding: 44px 22px;

  &__title {
    font-family: $font-primary;
    font-size: 29px;
    color: $color-dark-text;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
  }
}
</style>
