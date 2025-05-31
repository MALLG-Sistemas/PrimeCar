<template>
  <div class="not-found">
    <div class="not-found__container">
      <h1>404</h1>
      <h2>Página não encontrada</h2>
      <p>Desculpe, a página que você está procurando não existe.</p>
      <router-link
        to="/"
        class="not-found__button">
        Voltar para Home
      </router-link>
    </div>
  </div>
</template>

<style lang="scss">
@use "../styles/variables" as *;

.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  background-color: #6c757d;

  &__container {
    max-width: 500px;
    padding: 2rem;

    h1 {
      font-size: 6rem;
      color: #000;
      margin: 0;
      line-height: 1;
    }

    h2 {
      font-size: 2rem;
      color: #325615;
      margin: 1rem 0;
    }

    p {
      color: #6c757d;
      margin-bottom: 2rem;
    }
  }

  &__button {
    display: inline-block;
    padding: 0.8rem 1.6rem;
    background-color: #145452;
    color: #414562;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #151845;
    }
  }
}
</style>
