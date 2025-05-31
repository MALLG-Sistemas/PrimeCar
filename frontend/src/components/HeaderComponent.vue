<template>
  <header class="navbar">
    <div class="navbar-left">
      <!-- Aqui vai faltar codificar o parte que recebe o nome do usuário logado -->
      <h1 class="welcome">Bem-vindo, Mauricio!</h1>
      <p class="subtitle">
        Gerencie marcas, modelos, frota, locações e usuários cadastrados.
      </p>
    </div>
    <div class="navbar-right">
      <span class="material-symbols-outlined notification-icon">
        notifications
      </span>

      <!-- Aqui vai faltar codificar o parte que recebe as informações do usuário logado -->
      <div class="user-info">
        <img
          class="user-photo"
          src="/images/user-mauricio-perfil.jpg"
          alt="Foto do usuário" />
        <div class="user-text">
          <span class="user-name">Mauricio Pasetto</span>
          <span class="user-role">Admin</span>
        </div>
        <span class="material-symbols-outlined arrow-down-icon"
          >keyboard_arrow_down</span
        >
      </div>
    </div>
  </header>
</template>

<script setup>
// O usuário logado e suas informações virão da API.
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 79px;
  padding: 0 20px;

  /* Falar com o grupo referente ao box-shadow */
  /* box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); */

  .navbar-left {
    display: flex;
    flex-direction: column;
    justify-content: center;

    .welcome {
      margin: 0;
      font-size: 2rem; // 32px
      font-weight: 600;
      color: $color-text-secondary;
    }

    .subtitle {
      margin: 0;
      font-size: 0.875rem; // 14px
      color: $color-text-tertiary;
    }
  }

  .navbar-right {
    display: flex;
    align-items: center;

    .notification-icon {
      font-size: 26px;
      color: $color-text-secondary;
      margin-right: 15px;
      border-radius: 4px;
      border: 1px solid $color-text-tertiary;
      padding: 8px;
    }

    .user-info {
      display: flex;
      align-items: center;

      .user-photo {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 10px;
      }

      .user-text {
        display: flex;
        flex-direction: column;

        .user-name {
          font-size: 1rem;
          font-weight: 500;
          color: $color-text-secondary;
        }

        .user-role {
          font-size: 0.75rem;
          color: $color-text-tertiary;
        }
      }

      .arrow-down-icon {
        color: $color-text-secondary;
        font-size: 20px;
        margin-left: 10px;
      }
    }
  }
}
</style>
