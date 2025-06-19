<template>
  <section class="section-edit">
    <!-- Interface diferente baseada na forma de acesso -->
    <div class="section-edit__container">
      <header class="section-edit__header">
        <h1 class="section-edit__title">
          {{
            isDirectAccess ? "Selecionar Veículo" : "Editar/Visualizar Veículo"
          }}
        </h1>
      </header>

      <!-- Interface de acesso direto pelo menu -->
      <div
        v-if="isDirectAccess"
        class="section-edit__direct-access">
        <div class="section-edit__search-container">
          <ButtonComponent
            class="section-edit__button"
            size="small"
            bgColor="#3D5E73"
            textColor="#FFFFFF"
            fontSize="14px"
            @click="$router.push('/')">
            Voltar
          </ButtonComponent>

          <div class="section-edit__search">
            <span class="material-symbols-outlined">search</span>
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Pesquisar veículos..."
              class="section-edit__search-input" />
          </div>

          <select
            v-model="selectedCarId"
            class="section-edit__select"
            @change="handleCarSelect">
            <option
              disabled
              value="">
              Selecione um veículo
            </option>
            <option
              v-for="carOption in filteredCars"
              :key="carOption.id"
              :value="carOption.id">
              {{ carOption.modelo?.nome_marca }}
              {{ carOption.modelo?.nome_modelo }} ({{ carOption.cor }})
            </option>
          </select>
        </div>
      </div>

      <!-- Botões de ação para acesso pelo botão Visualizar -->
      <div
        v-else
        class="section-edit__actions">
        <ButtonComponent
          class="section-edit__button"
          size="large"
          bgColor="#3D5E73"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="editMode = !editMode">
          {{ editMode ? "Cancelar" : "Editar Veículo" }}
        </ButtonComponent>

        <ButtonComponent
          class="section-delete__button"
          size="large"
          bgColor="#f00"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="deleteCar">
          Excluir Veículo
        </ButtonComponent>
      </div>
    </div>

    <!-- Estado de carregamento -->
    <div
      class="section-edit__content"
      v-if="isLoading">
      <p class="loading">Carregando detalhes do veículo...</p>
    </div>

    <!-- Estado de erro -->
    <div
      class="section-edit__content"
      v-else-if="errorMessage">
      <p class="error-message">{{ errorMessage }}</p>
    </div>

    <!-- Estado de seleção vazia (para acesso direto) -->
    <div
      class="section-edit__content"
      v-else-if="isDirectAccess && !selectedCarId">
      <p class="instruction-message">
        Utilize a pesquisa ou selecione um veículo na lista acima para
        visualizar seus detalhes.
      </p>
    </div>

    <!-- Detalhes do veículo -->
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
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import apiClient from "../services/api";
import ButtonComponent from "../components/ButtonComponent.vue";

const route = useRoute();
const router = useRouter();
const car = ref({});
const cars = ref([]); // Lista para o select
const isLoading = ref(true);
const errorMessage = ref("");
const editMode = ref(false);
const searchTerm = ref("");
const selectedCarId = ref("");

// Verifica se o acesso foi direto pelo menu ou via botão Visualizar
const isDirectAccess = computed(() => !route.params.id);

// Lista filtrada de carros para o select
const filteredCars = computed(() => {
  const term = searchTerm.value.trim().toLowerCase();
  if (!term) return cars.value;

  return cars.value.filter((carItem) => {
    const marcaModelo =
      `${carItem.modelo?.nome_marca} ${carItem.modelo?.nome_modelo}`.toLowerCase();
    const cor = (carItem.cor || "").toLowerCase();
    const ano = carItem.ano_fabricacao?.toString() || "";

    return (
      marcaModelo.includes(term) || cor.includes(term) || ano.includes(term)
    );
  });
});

// Buscar dados do carro pelo ID na URL ou pelo ID selecionado
const fetchCarDetails = async (id) => {
  if (!id) {
    if (isDirectAccess.value) {
      isLoading.value = false;
      return;
    }

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

// Buscar lista de todos os carros para o select
const fetchAllCars = async () => {
  try {
    const response = await apiClient.getCarros();
    cars.value = Array.isArray(response.data.results)
      ? response.data.results
      : [];
  } catch (error) {
    console.error("Erro ao buscar lista de veículos:", error);
  }
};

// Manipulador para quando um carro é selecionado no dropdown
const handleCarSelect = () => {
  if (selectedCarId.value) {
    // Atualiza a URL para incluir o ID selecionado (opcional)
    router.push({
      name: "Editar Veiculo",
      params: { id: selectedCarId.value },
    });

    // Busca os detalhes do veículo selecionado
    fetchCarDetails(selectedCarId.value);
  }
};

// Função para excluir o veículo
const deleteCar = async () => {
  if (!confirm("Tem certeza que deseja excluir este veículo?")) {
    return;
  }

  try {
    await apiClient.deleteCarro(route.params.id || selectedCarId.value);
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
onMounted(async () => {
  if (isDirectAccess.value) {
    // Se for acesso direto pelo menu, busca todos os carros para o select
    await fetchAllCars();
    isLoading.value = false;
  } else {
    // Se for acesso via botão Visualizar, busca apenas o carro específico
    fetchCarDetails(route.params.id);
  }
});
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

  &__direct-access {
    width: 100%;
    margin-top: 20px;
  }

  &__search-container {
    display: flex;
    align-items: center;
    gap: 15px;
    width: 100%;
  }

  &__search {
    display: flex;
    align-items: center;
    flex: 1;
    padding: 10px 16px;
    gap: 8px;
    border: 1px solid $color-border-table;
    border-radius: 6px;
    color: $color-text-tertiary;
    background-color: white;

    &-input {
      border: none;
      outline: none;
      flex: 1;
      background-color: transparent;
      font-size: 14px;
    }
  }

  &__select {
    min-width: 250px;
    padding: 10px;
    border: 1px solid $color-border-table;
    border-radius: 6px;
    background-color: white;
    font-size: 14px;
    color: $color-text-secondary;
    cursor: pointer;
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
  .error-message,
  .instruction-message {
    text-align: center;
    padding: 20px;
    font-size: 18px;
  }

  .error-message {
    color: red;
  }

  .instruction-message {
    color: $color-text-tertiary;
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
