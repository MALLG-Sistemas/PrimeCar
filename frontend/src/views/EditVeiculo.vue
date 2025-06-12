<template>
  <section class="section-edit">
    <div class="section-edit__container">
      <header class="section-edit__header">
        <h1 class="section-edit__title">Editar/Visualizar Veículo</h1>
      </header>

      <div class="section-edit__actions">
        <ButtonComponent
          class="section-edit__button"
          size="large"
          bgColor="#3D5E73"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="$router.push('/add')">
          Editar Veículo
        </ButtonComponent>
        <ButtonComponent
          class="section-edit__button"
          size="large"
          bgColor="#f00"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="$router.push('/veiculos')">
          Excluir Veículo
        </ButtonComponent>
      </div>
    </div>
  </section>
</template>

<script setup>
import ButtonComponent from "../components/ButtonComponent.vue";
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;
.section-edit {
  &__container {
    display: flex;
    justify-content: space-between;

    padding: 44px 22px;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
  }

  &__title {
    font-family: $font-primary;
    font-size: 29px;
    font-weight: 500;
    color: $color-text-secondary;
  }

  &__actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }
}
</style>
