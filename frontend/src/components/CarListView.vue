<template>
  <div class="car-list-view">
    <div class="container-header">
      <h1 class="title-veiculos">Veículos</h1>

      <!-- Search Input ***** NÃO ESQUECER DE IMPLEMENTAR A LÓGICA DE PESQUISA NA LISTA DE CARROS -->
      <div class="search-wrapper">
        <span class="material-symbols-outlined search-icon">search</span>
        <input
          type="text"
          placeholder="Pesquisar veículos..."
          class="search-input" />
      </div>

      <!-- Falta o button de Adicionar Veículo -->
    </div>
    <div
      v-if="loading"
      class="loading">
      Carregando veículos...
    </div>
    <div
      v-if="error"
      class="error">
      {{ error }}
    </div>

    <div
      v-if="!loading && !error && carros.length === 0"
      class="no-cars">
      Nenhum veículo encontrado.
    </div>

    <table
      v-if="!loading && !error && carros.length > 0"
      class="car-table">
      <thead>
        <tr>
          <th>ID/Código</th>
          <!-- <th>Marca</th> -->
          <th>ID Modelo</th>
          <th>Data de Cadastro</th>
          <th>Ano Fabricação</th>
          <th>Cor</th>
          <th>Descrição</th>
          <th>Imagem</th>

          <!-- Usar qual titulo para essa coluna? Aqui terá o button "Visualizar" -->
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="carro in carros"
          :key="carro.id">
          <td>{{ carro.id }}</td>

          <!-- Ajusta para ID do modelo -->
          <td>{{ carro.modelo.id }}</td>
          <td>{{ formatDate(carro.data_cadastro) }}</td>
          <td>{{ carro.ano_fabricacao }}</td>
          <td>{{ carro.cor }}</td>
          <td>{{ carro.descricao_carro }}</td>
          <td class="td-car-image">
            <img
              v-if="carro.imagem_principal_url"
              :src="carro.imagem_principal_url"
              :alt="'Imagem de ' + carro.modelo.nome_modelo"
              class="car-thumbnail" />
            <span v-else>(Sem imagem)</span>
          </td>
          <td>
            <!-- ButtonComponent -->
            <ButtonComponent
              class="btn-table"
              size="medium"
              bgColor="#3D5E73"
              textColor="#FFFFFF"
              @click="() => verDetalhes(carro.id)">
              Visualizar
            </ButtonComponent>

            <!-- Adicionar botões para editar/deletar futuramente -->
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import apiClient from "../services/api"; // Importação do cliente API
import ButtonComponent from "./ButtonComponent.vue";

const carros = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchCarros = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await apiClient.getCarros();
    carros.value = response.data.results; // Ajuste se sua API DRF usar paginação (results)

    // Log para verificar os dados recebidos
    console.log("Carros recebidos:", carros.value);
  } catch (err) {
    console.error("Erro ao buscar carros:", err);
    error.value = "Falha ao carregar os veículos. Tente novamente mais tarde.";
    if (err.response) {
      // O servidor respondeu com um status de erro (4xx, 5xx)
      console.error("Dados do erro:", err.response.data);
      console.error("Status do erro:", err.response.status);
      error.value += ` (Status: ${err.response.status})`;
    } else if (err.request) {
      // A requisição foi feita mas não houve resposta
      console.error("Requisição do erro:", err.request);
      error.value =
        "Não foi possível conectar ao servidor. Verifique sua conexão e se o backend está rodando.";
    } else {
      // Algo aconteceu ao configurar a requisição que acionou um erro
      console.error("Mensagem de erro:", err.message);
    }
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchCarros();
});

const verDetalhes = (carroId) => {
  console.log("Visualizar detalhes do carro ID:", carroId);
  // Aqui você usaria o router para navegar para a página de detalhes
  // router.push({ name: 'CarDetail', params: { id: carroId } });
};

// Falta Codificar a lógico do search input, para pesquisar na lista de carros

// Função para formatação de data
const formatDate = (isoDate) => {
  if (!isoDate) return "";
  const date = new Date(isoDate);
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();
  return `${day}/${month}/${year}`;
};
</script>

<style scoped lang="scss">
@use "../styles/variables" as *;

.car-list-view {
  padding: 44px 22px 18px 22px;

  .title-veiculos {
    font-family: $font-primary;
    font-size: 29px;
    font-weight: 500;
    color: $color-text-secondary;
  }
}

.container-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;

  .search-wrapper {
    display: flex;
    align-items: center;
    width: 350px;
    padding: 12px 16px;
    gap: 8px;
    color: $color-text-tertiary;
    border-radius: 6px;
    border: 1px solid $color-border-table;
  }

  .search-input {
    border: none;
    outline: none;
    flex: 1;
  }
}

.loading,
.error,
.no-cars {
  margin-top: 20px;
  text-align: center;
  font-size: 1.2em;
}

.error {
  color: red;
}

.car-table {
  width: 100%;
  margin-top: 35px;
  overflow: hidden;
  border: 1px solid $color-border-table;
  border-radius: 8px;
  border-collapse: separate;
  border-spacing: 0;

  thead {
    th {
      padding: 16px;
      text-align: left;
      color: $color-dark-text;
      font-family: $font-primary;
      font-size: 16px;
      font-weight: 600;
      background-color: $color-light-bg;
      text-transform: uppercase;
      border-bottom: 1px dashed $color-border-table;
    }
  }

  tbody {
    tr {
      td {
        padding: 16px;
        text-align: left;
        color: $color-dark-text;
        font-family: $font-primary;
        font-size: 16px;
        font-weight: 600;
        border-bottom: 1px dashed $color-border-table;
      }
      &:last-child {
        td {
          border-bottom: none;
        }
      }
    }

    .td-car-image {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 8px 16px;
    }
  }
}

.car-thumbnail {
  max-width: 192px;
  max-height: 61px;
  object-fit: cover;
  width: 100%;
  height: auto;
  border-radius: 6px;
}
</style>
