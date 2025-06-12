<template>
  <div class="car-list">
    <header class="car-list__header">
      <h1 class="car-list__title">Veículos</h1>

      <div class="car-list__actions">
        <div class="car-list__search">
          <span class="material-symbols-outlined">search</span>
          <input
            v-model="searchTerm"
            type="text"
            id="search"
            name="search"
            placeholder="Pesquisar veículos..."
            class="car-list__search-input" />
        </div>

        <ButtonComponent
          class="car-list__add-button"
          size="medium"
          bgColor="#3D5E73"
          textColor="#FFFFFF"
          fontSize="14px"
          @click="navigateToAddCar">
          Add Veículo
        </ButtonComponent>
      </div>
    </header>

    <section
      v-if="isLoading"
      class="car-list__status">
      Carregando veículos...
    </section>
    <section
      v-else-if="errorMessage"
      class="car-list__status car-list__status--error">
      {{ errorMessage }}
    </section>
    <section
      v-else-if="filteredCars.length === 0"
      class="car-list__status car-list__status--empty">
      Nenhum veículo encontrado.
    </section>
    <table
      v-else
      class="car-list__table">
      <thead>
        <tr>
          <th>ID</th>
          <th>ID Modelo</th>
          <th>Data de Cadastro</th>
          <th>Ano Fabricação</th>
          <th>Cor</th>
          <th>Descrição</th>
          <th>Foto/Imagem</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="car in filteredCars"
          :key="car.id">
          <td>{{ car.id }}</td>
          <td>{{ car.modelo.id }}</td>
          <td>{{ formatDate(car.data_cadastro) }}</td>
          <td>{{ car.ano_fabricacao }}</td>
          <td>{{ car.cor }}</td>
          <td>{{ car.descricao_carro }}</td>
          <td>
            <img
              v-if="car.imagem_principal_url"
              :src="car.imagem_principal_url"
              :alt="`Imagem de ${car.modelo.nome_modelo}`"
              class="car-list__image" />
            <span v-else>Sem imagem</span>
          </td>
          <td>
            <ButtonComponent
              class="car-list__view-button"
              size="small"
              bgColor="#3D5E73"
              textColor="#FFFFFF"
              fontSize="14px"
              @click="navigateToDetails(car.id)">
              Visualizar
            </ButtonComponent>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import apiClient from "../services/api";
import ButtonComponent from "./ButtonComponent.vue";

// Estado reativos
const cars = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");
const searchTerm = ref("");

// Declaração de router
const router = useRouter();

// Fetch dos dados
const fetchCars = async () => {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await apiClient.getCarros();
    cars.value = Array.isArray(response.data.results)
      ? response.data.results
      : [];
  } catch (error) {
    handleError(error);
  } finally {
    isLoading.value = false;
  }
};

// Tratamento de erro dos dados recebidos da API
const handleError = (error) => {
  if (error.response) {
    errorMessage.value = `Erro ${error.response.status}: ${
      error.response.data?.detail || "Falha na API"
    }`;
  } else if (error.request) {
    errorMessage.value = "Sem resposta do servidor. Verifique sua conexão.";
  } else {
    errorMessage.value = `Erro: ${error.message}`;
  }
};

// Propriedade computada para a pesquisa
const filteredCars = computed(() => {
  const term = searchTerm.value.trim().toLowerCase();
  if (!term) return cars.value;

  return cars.value.filter((car) => {
    return (
      car.id.toString().includes(term) ||
      car.modelo.id.toString().includes(term) ||
      (car.modelo.nome_modelo || "").toLowerCase().includes(term) ||
      (car.cor || "").toLowerCase().includes(term) ||
      (car.descricao_carro || "").toLowerCase().includes(term) ||
      car.ano_fabricacao.toString().includes(term)
    );
  });
});

/* Lida com a navegação dos botões, direciona para a
 * página de adicionar veículo ou detalhes do veículo
 */
const navigateToAddCar = () => router.push({ name: "Add Veiculo" });
const navigateToDetails = (id) =>
  router.push({ name: "Editar Veiculo", params: { id } });

// Função para formatar a data no estilo brasileiro
const formatDate = (dateStr) => {
  if (!dateStr) return "";
  const date = new Date(dateStr);
  return date.toLocaleDateString("pt-BR");
};

// Lifecycle
onMounted(fetchCars);
</script>

<style scoped lang="scss">
@use "../styles/variables" as *;

.car-list {
  padding: 44px 22px;

  &__title {
    font-family: $font-primary;
    font-size: 29px;
    font-weight: 500;
    color: $color-text-secondary;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
  }

  &__actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  &__search {
    display: flex;
    align-items: center;
    width: 350px;
    padding: 12px 16px;
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
    }
  }

  &__status {
    margin-top: 20px;
    text-align: center;
    font-size: 1.2em;
    color: $color-dark-text;

    &--error {
      color: red;
    }

    &--empty {
      color: $color-text-tertiary;
    }
  }

  &__table {
    width: 100%;
    margin-top: 35px;
    border: 1px solid $color-border-table;
    border-radius: 8px;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;

    thead {
      tr {
        th {
          padding: 16px;
          text-align: left;
          color: $color-dark-text;
          font-family: $font-primary;
          font-size: 16px;
          font-weight: 700;
          line-height: 24px;
          text-transform: uppercase;
          border-bottom: 1px dashed $color-border-table;
        }
      }
    }

    tbody {
      tr {
        td {
          padding: 8px 16px;
          color: $color-dark-text;
          font-family: $font-primary;
          font-size: 13px;
          font-weight: 600;
          border-bottom: 1px dashed $color-border-table;
          text-transform: uppercase;
        }

        &:last-child {
          td {
            border-bottom: none;
          }
        }
      }
    }
  }

  &__image {
    max-width: 90px;
    max-height: 51px;
    width: 100%;
    height: auto;
    display: flex;
    justify-content: center;
    object-fit: cover;
    border-radius: 6px;
  }
}
</style>
