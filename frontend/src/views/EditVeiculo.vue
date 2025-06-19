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

          <div class="section-edit__search-wrapper">
            <div class="section-edit__search">
              <span class="material-symbols-outlined">search</span>
              <input
                v-model="searchTerm"
                type="text"
                placeholder="Pesquisar veículos..."
                @focus="showSearchResults = true"
                @blur="handleSearchBlur"
                class="section-edit__search-input" />
            </div>

            <div
              v-if="showSearchResults && searchTerm.trim()"
              class="section-edit__search-results">
              <div
                v-if="filteredCars.length === 0"
                class="section-edit__search-no-results">
                Nenhum veículo encontrado
              </div>
              <div
                v-for="carOption in filteredCars"
                :key="carOption.id"
                class="section-edit__search-option"
                @mousedown="selectCarFromSearch(carOption.id)">
                {{ carOption.modelo?.nome_marca }}
                {{ carOption.modelo?.nome_modelo }} ({{ carOption.cor }})
              </div>
            </div>
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
          <hr class="vehicle-edit-card__divider__edit" />

          <!-- Seção de imagens do veículo -->
          <div class="vehicle-images">
            <!-- Imagem Principal -->
            <div class="main-image-container">
              <img
                :src="
                  previewImage ||
                  car.imagem_principal_url ||
                  '/images/no-image.jpg'
                "
                alt="Imagem principal do veículo"
                class="main-image" />
              <div
                class="edit-image-overlay"
                @click="$refs.fileInput.click()">
                <span class="material-symbols-outlined">edit</span>
                <span class="edit-text">Editar imagem</span>
              </div>
            </div>

            <!-- Miniaturas de imagens -->
            <div class="thumbnail-container">
              <!-- Miniatura principal -->
              <div class="thumbnail active">
                <img
                  :src="
                    previewImage ||
                    car.imagem_principal_url ||
                    '/images/no-image.jpg'
                  "
                  alt="Miniatura principal" />
                <div
                  class="thumbnail-edit-icon"
                  @click="$refs.fileInput.click()">
                  <span class="material-symbols-outlined">edit</span>
                </div>
              </div>

              <!-- Espaços para futuras imagens -->
              <div
                v-for="index in 3"
                :key="index"
                class="thumbnail empty">
                <span class="material-symbols-outlined add-icon"
                  >add_photo_alternate</span
                >
              </div>
            </div>
          </div>

          <form
            @submit.prevent="saveChanges"
            class="vehicle-edit-form">
            <!-- Campo de Modelo (apenas visualização) -->
            <div class="form-group">
              <label for="car-model">Modelo:</label>
              <input
                id="car-model"
                type="text"
                v-model="editedCar.modelo_nome"
                class="form-control"
                disabled
                title="Modelo não pode ser alterado diretamente" />
            </div>

            <!-- Campos de Ano e Cor lado a lado -->
            <div class="form-group form-row">
              <!-- Ano de Fabricação -->
              <div class="form-col">
                <label for="car-year">Ano de Fabricação:</label>
                <input
                  id="car-year"
                  type="number"
                  v-model.number="editedCar.ano_fabricacao"
                  class="form-control"
                  required />
              </div>

              <!-- Cor -->
              <div class="form-col">
                <label for="car-color">Cor:</label>
                <input
                  id="car-color"
                  type="text"
                  v-model="editedCar.cor"
                  class="form-control"
                  required />
              </div>
            </div>

            <!-- Campo de Descrição -->
            <div class="form-group">
              <label for="car-desc">Descrição:</label>
              <textarea
                id="car-desc"
                v-model="editedCar.descricao_carro"
                class="form-control form-textarea"
                rows="5"></textarea>
            </div>

            <!-- Input de arquivo oculto (acionado pelos botões de edição) -->
            <input
              ref="fileInput"
              id="car-image"
              type="file"
              @change="handleImageChange"
              class="hidden-input"
              accept="image/*" />

            <!-- Botões de ação do formulário -->
            <div class="form-buttons">
              <ButtonComponent
                class="save-button"
                size="large"
                bgColor="#3D5E73"
                textColor="#FFFFFF"
                fontSize="14px"
                type="submit"
                :disabled="isSaving">
                {{ isSaving ? "Salvando..." : "Salvar Alterações" }}
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
const fileInput = ref(null);
const previewImage = ref(null);
const showSearchResults = ref(false); // Controla a visibilidade do dropdown de resultados

// Objeto reativo para armazenar os dados do veículo em edição
const editedCar = reactive({
  ano_fabricacao: 0,
  cor: "",
  descricao_carro: "",
  modelo_id: null,
  modelo_nome: "", // Adicionado para exibir o nome do modelo no campo de visualização
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

/**
 * Trata o evento blur do campo de pesquisa
 * Usa setTimeout para permitir o clique nas opções antes de fechar o dropdown
 */
const handleSearchBlur = () => {
  setTimeout(() => {
    showSearchResults.value = false;
  }, 200);
};

/**
 * Seleciona um carro a partir dos resultados da pesquisa
 * @param {string} id - ID do veículo selecionado
 */
const selectCarFromSearch = (id) => {
  selectedCarId.value = id;

  // Atualiza a URL para incluir o ID selecionado
  router.push({
    name: "Editar Veiculo",
    params: { id },
  });

  // Busca os detalhes do veículo selecionado
  fetchCarDetails(id);
};

/**
 * Busca os detalhes de um veículo pelo ID
 * @param {string} id - ID do veículo a ser buscado
 */
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

    // Adiciona o nome do modelo completo para exibição
    editedCar.modelo_nome = car.value.modelo
      ? `${car.value.modelo.nome_marca} ${car.value.modelo.nome_modelo}`
      : "";

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

    // Limpa o preview da imagem
    previewImage.value = null;
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

/**
 * Busca todos os veículos disponíveis para o select
 */
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

/**
 * Manipulador para quando um veículo é selecionado no dropdown
 */
const handleCarSelect = () => {
  if (selectedCarId.value) {
    // Atualiza a URL para incluir o ID selecionado
    router.push({
      name: "Editar Veiculo",
      params: { id: selectedCarId.value },
    });

    // Busca os detalhes do veículo selecionado
    fetchCarDetails(selectedCarId.value);
  }
};

/**
 * Exclui o veículo atual após confirmação
 */
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

/**
 * Manipulador para lidar com a seleção de uma nova imagem
 */
const handleImageChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    newImage.value = file;

    // Criar uma prévia da imagem
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

/**
 * Salva as alterações feitas no formulário
 */
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

/**
 * Cancela a edição e restaura valores originais
 */
const cancelEdit = () => {
  // Restaura os valores originais
  editedCar.ano_fabricacao = car.value.ano_fabricacao || 0;
  editedCar.cor = car.value.cor || "";
  editedCar.descricao_carro = car.value.descricao_carro || "";
  editedCar.modelo_id = car.value.modelo?.id || null;
  editedCar.modelo_nome = car.value.modelo
    ? `${car.value.modelo.nome_marca} ${car.value.modelo.nome_modelo}`
    : "";

  // Limpa a seleção de imagem
  newImage.value = null;
  previewImage.value = null;

  // Sai do modo de edição
  editMode.value = false;
};

/**
 * Formata uma data para o padrão brasileiro (DD/MM/AAAA)
 * @param {string} dateStr - String de data no formato ISO
 * @returns {string} Data formatada
 */
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

  &__search-wrapper {
    position: relative;
    flex: 1;
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

  &__search-results {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    max-height: 250px;
    overflow-y: auto;
    background-color: white;
    border: 1px solid $color-border-table;
    border-top: none;
    border-radius: 0 0 6px 6px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 10;
  }

  &__search-option {
    padding: 10px 16px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    color: $color-text-secondary;

    &:hover {
      background-color: #f5f5f5;
    }
  }

  &__search-no-results {
    padding: 10px 16px;
    color: $color-text-tertiary;
    font-style: italic;
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

  // Seção de imagens do veículo
  .vehicle-images {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .main-image-container {
      position: relative;
      width: 100%;
      height: 240px;
      border-radius: 8px;
      overflow: hidden;

      .main-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .edit-image-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        opacity: 0;
        transition: opacity 0.3s ease;
        cursor: pointer;

        &:hover {
          opacity: 1;
        }

        .material-symbols-outlined {
          font-size: 32px;
          margin-bottom: 10px;
        }

        .edit-text {
          font-size: 14px;
        }
      }
    }

    .thumbnail-container {
      display: flex;
      gap: 10px;

      .thumbnail {
        position: relative;
        width: 80px;
        height: 60px;
        border-radius: 4px;
        overflow: hidden;
        cursor: pointer;

        &.active {
          border: 2px solid $color-button-primary;
        }

        &.empty {
          background-color: #e0e0e0;
          display: flex;
          align-items: center;
          justify-content: center;

          .add-icon {
            color: #878787;
            font-size: 24px;
          }
        }

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .thumbnail-edit-icon {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          background-color: rgba(0, 0, 0, 0.5);
          color: white;
          opacity: 0;
          transition: opacity 0.3s ease;

          &:hover {
            opacity: 1;
          }
        }
      }
    }
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
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 60%;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    background-color: $color-bg-page-edit-view;

    &__title {
      text-align: center;
      font-family: $font-primary;
      font-size: 29px;
      font-weight: 500;
      color: $color-text-secondary;
      line-height: 121.168%;
    }

    &__divider {
      border: 0;
      border-top: 1px solid $color-border-table;
    }

    &__divider__edit {
      border: 0;
      border-top: 1px solid $color-light-bg;
    }
  }

  // Formulário de edição
  .vehicle-edit-form {
    .form-group {
      margin-bottom: 20px;

      // Layout para campos lado a lado
      &.form-row {
        display: flex;
        gap: 20px;

        .form-col {
          flex: 1;
        }
      }

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

        // Estilos específicos para campos desabilitados
        &:disabled {
          background-color: #f5f5f5;
          color: #666;
          cursor: not-allowed;
        }
      }

      .form-textarea {
        resize: vertical;
        min-height: 100px;
      }
    }

    .form-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 15px;
      margin-top: 30px;
    }
  }

  // Input de arquivo oculto
  .hidden-input {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
  }
}

// Responsividade para telas menores
@media (max-width: 768px) {
  .section-edit {
    .vehicle-content {
      flex-direction: column;

      .vehicle-card.reduced {
        width: 100%;
        margin-bottom: 20px;
      }

      .vehicle-edit-card {
        width: 100%;
      }
    }
  }
}
</style>
