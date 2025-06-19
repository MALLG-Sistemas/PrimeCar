<template>
  <section class="section-edit">
    <!-- Dialog de confirmação para exclusão -->
    <DialogAlert
      :isVisible="showDeleteDialog"
      message="Tem certeza que deseja excluir este veículo?"
      @confirm="confirmDelete"
      @cancel="showDeleteDialog = false"
      @close="showDeleteDialog = false" />

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
          @click="showDeleteDialog = true">
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

    <!-- Detalhes do veículo e formulário de edição -->
    <div
      class="section-edit__content"
      v-else>
      <div
        class="vehicle-content"
        :class="{ 'edit-mode': editMode }">
        <!-- Card de visualização (reduzido quando em modo de edição) -->
        <div
          class="vehicle-card"
          :class="{ reduced: editMode }">
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

        <!-- Card de edição (exibido apenas quando em modo de edição) -->
        <div
          v-if="editMode"
          class="vehicle-edit-card">
          <h2 class="vehicle-edit-card__title">Editar Veículo</h2>
          <hr class="vehicle-edit-card__divider" />

          <form
            @submit.prevent="saveChanges"
            class="vehicle-edit-form">
            <div class="form-group">
              <label for="car-year">Ano de Fabricação:</label>
              <input
                id="car-year"
                type="number"
                v-model.number="editedCar.ano_fabricacao"
                class="form-control"
                required />
            </div>

            <div class="form-group">
              <label for="car-color">Cor:</label>
              <input
                id="car-color"
                type="text"
                v-model="editedCar.cor"
                class="form-control"
                required />
            </div>

            <div class="form-group">
              <label for="car-desc">Descrição:</label>
              <textarea
                id="car-desc"
                v-model="editedCar.descricao_carro"
                class="form-control form-textarea"
                rows="5"></textarea>
            </div>

            <div class="form-group">
              <label for="car-image">Imagem Principal:</label>
              <div class="image-upload-container">
                <input
                  id="car-image"
                  type="file"
                  @change="handleImageChange"
                  class="form-control"
                  accept="image/*" />
                <p class="image-help-text">
                  Selecione uma nova imagem para substituir a atual
                </p>
              </div>
            </div>

            <div class="form-buttons">
              <ButtonComponent
                class="save-button"
                size="large"
                bgColor="#3D5E73"
                textColor="#FFFFFF"
                fontSize="14px"
                type="submit">
                Salvar Alterações
              </ButtonComponent>

              <ButtonComponent
                class="cancel-button"
                size="large"
                bgColor="#878787"
                textColor="#FFFFFF"
                fontSize="14px"
                type="button"
                @click="cancelEdit">
                Cancelar
              </ButtonComponent>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from "vue";
import { useRoute, useRouter } from "vue-router";
import apiClient from "../services/api";
import ButtonComponent from "../components/ButtonComponent.vue";
import DialogAlert from "../components/DialogAlert.vue";

const route = useRoute();
const router = useRouter();
const car = ref({});
const cars = ref([]); // Lista para o select
const isLoading = ref(true);
const errorMessage = ref("");
const editMode = ref(false);
const searchTerm = ref("");
const selectedCarId = ref("");
const showDeleteDialog = ref(false); // Controla a visibilidade do diálogo de confirmação
const editedCar = reactive({
  ano_fabricacao: 0,
  cor: "",
  descricao_carro: "",
  modelo_id: null,
});
const newImage = ref(null);
const isSaving = ref(false);

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
    // Remove os zeros à esquerda do ID se necessário
    const cleanId = id.replace(/^0+/, "");
    const response = await apiClient.getCarro(cleanId);
    car.value = response.data;

    // Inicializa os dados para edição
    editedCar.ano_fabricacao = car.value.ano_fabricacao || 0;
    editedCar.cor = car.value.cor || "";
    editedCar.descricao_carro = car.value.descricao_carro || "";

    // Obtém o ID do modelo, convertendo de "CAR001" para 1 se necessário
    if (car.value.modelo?.id) {
      if (
        typeof car.value.modelo.id === "string" &&
        car.value.modelo.id.startsWith("CAR")
      ) {
        editedCar.modelo_id = parseInt(
          car.value.modelo.id.replace("CAR", ""),
          10
        );
      } else {
        editedCar.modelo_id = car.value.modelo?.id || null;
      }
    } else {
      editedCar.modelo_id = null;
    }
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

// Função para excluir o veículo (após confirmação no DialogAlert)
const confirmDelete = async () => {
  try {
    const carId = route.params.id || selectedCarId.value;
    // Remove os zeros à esquerda do ID se necessário
    const cleanCarId = carId.replace(/^0+/, "");
    await apiClient.deleteCarro(cleanCarId);
    alert("Veículo excluído com sucesso!");
    router.push("/");
  } catch (error) {
    alert(`Erro ao excluir veículo: ${error.message}`);
  }
};

// Manipulador para lidar com a seleção de imagem
const handleImageChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    newImage.value = file;
  }
};

// Função para salvar as alterações
const saveChanges = async () => {
  try {
    isSaving.value = true;

    // Cria um FormData para envio multipart/form-data (necessário para upload de arquivos)
    const formData = new FormData();
    formData.append("ano_fabricacao", editedCar.ano_fabricacao);
    formData.append("cor", editedCar.cor);
    formData.append("descricao_carro", editedCar.descricao_carro);

    // Verifica se o modelo_id existe e se está no formato CAR001
    // Se sim, extrai apenas o número (convertendo de CAR001 para 1)
    if (editedCar.modelo_id) {
      // Se o ID do modelo estiver no formato "CARxxx", extraímos o número
      if (
        typeof editedCar.modelo_id === "string" &&
        editedCar.modelo_id.startsWith("CAR")
      ) {
        const numericId = parseInt(editedCar.modelo_id.replace("CAR", ""), 10);
        formData.append("modelo_id", numericId);
      } else {
        // Caso contrário, usamos o valor como está
        formData.append("modelo_id", editedCar.modelo_id);
      }
    }

    // Adiciona a nova imagem se houver
    if (newImage.value) {
      formData.append("imagem_principal", newImage.value);
    }

    // Enviar para API
    const carId = route.params.id || selectedCarId.value;
    // Remove os zeros à esquerda do ID se necessário (converter 0003 para 3)
    const cleanCarId = carId.replace(/^0+/, "");
    await apiClient.updateCarro(cleanCarId, formData);

    // Recarrega os detalhes atualizados
    await fetchCarDetails(carId);

    // Sai do modo de edição
    editMode.value = false;
    alert("Veículo atualizado com sucesso!");
  } catch (error) {
    alert(`Erro ao atualizar veículo: ${error.message}`);
    console.error("Erro ao atualizar:", error);
  } finally {
    isSaving.value = false;
  }
};

// Função para cancelar a edição
const cancelEdit = () => {
  // Restaura os valores originais
  editedCar.ano_fabricacao = car.value.ano_fabricacao || 0;
  editedCar.cor = car.value.cor || "";
  editedCar.descricao_carro = car.value.descricao_carro || "";
  editedCar.modelo_id = car.value.modelo?.id || null;

  // Limpa a seleção de imagem
  newImage.value = null;

  // Sai do modo de edição
  editMode.value = false;
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
/* Estilos existentes mantidos */
</style>

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

  // Layout para modo de edição
  .vehicle-content {
    display: flex;
    gap: 20px;

    &.edit-mode {
      justify-content: space-between;
    }
  }

  .vehicle-card {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    background-color: $color-bg-page-edit-view;
    transition: width 0.3s ease;

    &.reduced {
      width: 38%; // Quando em modo de edição, card de visualização fica com 38%
      margin: 0;
    }

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
      border-radius: 4px;
      background-color: #e0e0e0;
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

  // Card de edição
  .vehicle-edit-card {
    width: 60%;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    background-color: white;

    &__title {
      font-size: 24px;
      margin-top: 0;
      color: $color-text-secondary;
    }

    &__divider {
      margin: 10px 0 20px;
      border: 0;
      border-top: 1px solid $color-border-table;
    }
  }

  // Formulário de edição
  .vehicle-edit-form {
    .form-group {
      margin-bottom: 20px;

      label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: $color-text-secondary;
      }

      .form-control {
        width: 100%;
        padding: 10px;
        border: 1px solid $color-border-table;
        border-radius: 6px;
        font-size: 14px;

        &:focus {
          outline: none;
          border-color: $color-button-primary;
        }
      }

      .form-textarea {
        resize: vertical;
        min-height: 100px;
      }

      .image-upload-container {
        .image-help-text {
          margin-top: 5px;
          font-size: 12px;
          color: $color-text-tertiary;
        }
      }
    }

    .form-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 15px;
      margin-top: 30px;
    }
  }
}
</style>
