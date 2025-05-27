<template>
  <div class="car-list-view">
    <h1>Lista de Veículos</h1>
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
          <th>ID Carro</th>
          <th>Marca</th>
          <th>Modelo</th>
          <th>Ano Modelo</th>
          <th>Ano Fabricação</th>
          <th>Cor</th>
          <th>Descrição</th>
          <th>Imagem</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="carro in carros"
          :key="carro.id">
          <td>{{ carro.id }}</td>
          <td>{{ carro.modelo.nome_marca }}</td>
          <td>{{ carro.modelo.nome_modelo }}</td>
          <td>{{ carro.modelo.ano_modelo }}</td>
          <td>{{ carro.ano_fabricacao }}</td>
          <td>{{ carro.cor }}</td>
          <td>{{ carro.descricao_carro }}</td>
          <td>
            <img
              v-if="carro.imagem_principal_url"
              :src="carro.imagem_principal_url"
              :alt="'Imagem de ' + carro.modelo.nome_modelo"
              class="car-thumbnail" />
            <span v-else>(Sem imagem)</span>
          </td>
          <td>
            <button @click="verDetalhes(carro.id)">Visualizar</button>
            <!-- Adicionar botões para editar/deletar futuramente -->
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import apiClient from "../services/api"; // Importe seu serviço de API
// import { useRouter } from 'vue-router'; // Se for usar o router para navegação

// const router = useRouter(); // Se for usar o router
const carros = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchCarros = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await apiClient.getCarros();
    carros.value = response.data.results; // Ajuste se sua API DRF usar paginação (results)
    // Se não usar paginação, pode ser apenas response.data
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
</script>

<style scoped lang="scss">
.car-list-view {
  padding: 20px;
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
  border-collapse: collapse;
  margin-top: 20px;

  th,
  td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }

  th {
    background-color: #f2f2f2;
  }
}

.car-thumbnail {
  max-width: 100px;
  max-height: 70px;
  object-fit: cover;
}
</style>
