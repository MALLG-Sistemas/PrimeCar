<template>
  <section class="section-models-view">
    <div class="container">
      <h1 class="title">Modelos</h1>
      <p class="subtitle">Lista de modelos disponíveis</p>
      <p>Em breve, esta seção exibirá os modelos disponíveis.</p>
    </div>
  </section>
</template>

<script setup></script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

.section-models-view {
  .container {
    padding: 20px;
  }

  .title {
    font-size: 2rem;
    color: #333;
    text-align: center;
    margin-top: 20px;
  }

  .subtitle {
    font-size: 1.5rem;
    color: #666;
    text-align: center;
    margin-top: 10px;
  }
}
</style>
