<template>
  <section class="section-edit">
    <div class="section-edit__container">
      <header class="section-edit__header">
        <h1 class="section-edit__title">Editar/Visualizar Veículo</h1>
      </header>

      <div class="section-edit__actions">
        <!-- Verificar -->
        <ButtonComponent
          class="section-edit__button"
          size="large"
          bgColor="#3D5E73"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="$router.push('')">
          Editar Veículo
        </ButtonComponent>
        <!-- Verificar -->
        <ButtonComponent
          class="section-delete__button"
          size="large"
          bgColor="#f00"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="$router.push('/veiculos')">
          Excluir Veículo
        </ButtonComponent>
      </div>
    </div>

    <div
      class="section-edit__content"
      v-if="isLoading">
      <p class="loading">Carregando detalhes do veículo...</p>
    </div>

    <div
      class="section-edit__content"
      v-else-if="errorMessage">
      <p class="error-message">{{ errorMessage }}</p>
    </div>

    <div
      class="section-edit__content"
      v-else>
      <div class="vehicle-card">
        <img
          :src="car.imagem_principal_url || '/images/no-image.jpg'"
          alt="Imagem do veículo"
          class="vehicle-card__image" />

        <div class="vehicle-card__thumbs">
          <div
            v-for="(thumb, index) in 4"
            :key="index"
            class="vehicle-card__thumb" />
        </div>

        <h2 class="vehicle-card__title">
          {{ car.modelo?.nome_marca }} {{ car.modelo?.nome_modelo }}
        </h2>
        <hr class="vehicle-card__divider" />

        <div class="vehicle-card__info">
          <p><strong>Código:</strong> {{ car.id }}</p>
          <p><strong>ID Modelo:</strong> {{ car.modelo?.id }}</p>
          <p><strong>Ano:</strong> {{ car.ano_fabricacao }}</p>
          <p><strong>Cor:</strong> {{ car.cor }}</p>
          <p>
            <strong>Data de Cadastro:</strong>
            {{ formatDate(car.data_cadastro) }}
          </p>
          <p><strong>Descrição:</strong> {{ car.descricao_carro }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import apiClient from "../services/api";
import ButtonComponent from "../components/ButtonComponent.vue";

const route = useRoute();
const router = useRouter();
const car = ref({});
const isLoading = ref(true);
const errorMessage = ref("");

// Buscar dados do carro pelo ID na URL
const fetchCarDetails = async () => {
  const id = route.params.id;
  if (!id) {
    errorMessage.value = "ID do veículo não especificado";
    isLoading.value = false;
    return;
  }

  try {
    isLoading.value = true;
    const response = await apiClient.getCarro(id);
    car.value = response.data;
  } catch (error) {
    if (error.response) {
      errorMessage.value = `Erro ${error.response.status}: ${
        error.response.data?.detail || "Erro ao carregar dados do veículo"
      }`;
    } else if (error.request) {
      errorMessage.value = "Sem resposta do servidor. Verifique sua conexão.";
    } else {
      errorMessage.value = `Erro: ${error.message}`;
    }
  } finally {
    isLoading.value = false;
  }
};

// Função para excluir o veículo
const deleteCar = async () => {
  if (!confirm("Tem certeza que deseja excluir este veículo?")) {
    return;
  }

  try {
    await apiClient.deleteCarro(route.params.id);
    alert("Veículo excluído com sucesso!");
    router.push("/");
  } catch (error) {
    alert(`Erro ao excluir veículo: ${error.message}`);
  }
};

// Formata data para o padrão brasileiro
const formatDate = (dateStr) => {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  return date.toLocaleDateString("pt-BR");
};

// Carregar dados ao montar o componente
onMounted(fetchCarDetails);
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

  &__content {
    padding: 0 22px;
  }

  .loading,
  .error-message {
    text-align: center;
    padding: 20px;
    font-size: 18px;
  }

  .error-message {
    color: red;
  }

  .vehicle-card {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);

    &__image {
      width: 100%;
      max-height: 400px;
      object-fit: cover;
      border-radius: 8px;
    }

    &__thumbs {
      display: flex;
      gap: 10px;
      margin-top: 10px;
    }

    &__thumb {
      width: 60px;
      height: 60px;
      background-color: #e0e0e0;
      border-radius: 4px;
    }

    &__title {
      font-size: 24px;
      margin-top: 20px;
      color: $color-text-secondary;
    }

    &__divider {
      margin: 10px 0;
      border: 0;
      border-top: 1px solid $color-border-table;
    }

    &__info {
      p {
        margin: 10px 0;
        color: $color-text-secondary;
      }
    }
  }
}
</style>
