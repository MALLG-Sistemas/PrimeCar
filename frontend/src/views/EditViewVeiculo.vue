<!-- 
  Este componente implementa uma interface de visualização e edição de veículos
  com duas formas de acesso possíveis:
  1. Acesso direto pelo menu (com seleção de veículo)
  2. Acesso via botão "Visualizar" de um veículo específico
-->
<template>
  <section class="section-edit">
    <!-- 
      Dialog de confirmação para exclusão - Componente reutilizável que exibe
      uma mensagem de confirmação antes de excluir um veículo 
    -->
    <DialogAlert
      :isVisible="showDeleteDialog"
      message="Tem certeza que deseja excluir este veículo?"
      @confirm="confirmDelete"
      @cancel="showDeleteDialog = false"
      @close="showDeleteDialog = false" />

    <!-- 
      Container principal com título dinâmico baseado na forma de acesso 
    -->
    <div class="section-edit__container">
      <header class="section-edit__header">
        <h1 class="section-edit__title">
          {{
            isDirectAccess ? "Selecionar Veículo" : "Visualizar/Editar Veículo"
          }}
        </h1>
      </header>

      <!-- 
        Interface de acesso direto pelo menu - Exibe um campo de pesquisa e
        um select para escolher veículos da lista 
      -->
      <div
        v-if="isDirectAccess"
        class="section-edit__direct-access">
        <div class="section-edit__search-container">
          <!-- Botão para voltar à página principal -->
          <ButtonComponent
            class="section-edit__button"
            size="small"
            bgColor="#3D5E73"
            textColor="#FFFFFF"
            fontSize="14px"
            @click="$router.push('/')">
            Voltar
          </ButtonComponent>

          <!-- 
            Campo de pesquisa com dropdown de resultados em tempo real 
          -->
          <div class="section-edit__search-wrapper">
            <div class="section-edit__search">
              <span class="material-symbols-outlined">search</span>
              <input
                v-model="searchTerm"
                type="text"
                id="car-search"
                name="car-search"
                placeholder="Pesquisar veículos..."
                @focus="showSearchResults = true"
                @blur="handleSearchBlur"
                class="section-edit__search-input" />
            </div>

            <!-- 
              Dropdown com resultados da pesquisa - Aparece apenas quando há texto
              no campo de pesquisa e o campo está em foco 
            -->
            <div
              v-if="showSearchResults && searchTerm.trim()"
              class="section-edit__search-results">
              <!-- Mensagem quando nenhum resultado é encontrado -->
              <div
                v-if="filteredCars.length === 0"
                class="section-edit__search-no-results">
                Nenhum veículo encontrado
              </div>
              <!-- Lista de veículos que correspondem à pesquisa -->
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

          <!-- 
            Select tradicional como alternativa à pesquisa 
          -->
          <select
            v-model="selectedCarId"
            id="car-select"
            name="car-select"
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

      <!-- 
        Botões de ação para acesso pelo botão Visualizar - Aparecem apenas
        quando o veículo foi selecionado previamente 
      -->
      <div
        v-else
        class="section-edit__actions">
        <!-- Botão que alterna entre modo de visualização e edição -->
        <ButtonComponent
          class="section-edit__button"
          size="large"
          bgColor="#3D5E73"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="editMode = !editMode">
          {{ editMode ? "Cancelar" : "Editar Veículo" }}
        </ButtonComponent>

        <!-- Botão de exclusão que abre o dialog de confirmação -->
        <ButtonComponent
          class="section-delete__button"
          size="large"
          bgColor="#f00"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="showDeleteDialog = true">
          Excluir Veículo
        </ButtonComponent>

        <!-- Botão para trocar o veículo selecionado -->
        <ButtonComponent
          class="section-back__button"
          size="large"
          bgColor="#878787"
          textColor="#FFFFFF"
          fontSize="11px"
          @click="backToSelection">
          Trocar Veículo
        </ButtonComponent>
      </div>
    </div>

    <!-- 
      Estados de interface condicionais: carregando, erro, sem seleção
      ou visualização normal 
    -->

    <!-- Estado de carregamento - Exibido durante operações assíncronas -->
    <div
      class="section-edit__content"
      v-if="isLoading">
      <p class="loading">Carregando detalhes do veículo...</p>
    </div>

    <!-- Estado de erro - Exibido quando ocorre uma falha na API -->
    <div
      class="section-edit__content"
      v-else-if="errorMessage">
      <p class="error-message">{{ errorMessage }}</p>
    </div>

    <!-- 
      Instrução para selecionar um veículo - Exibida apenas no acesso direto
      quando nenhum veículo foi selecionado 
    -->
    <div
      class="section-edit__content"
      v-else-if="isDirectAccess && !selectedCarId">
      <p class="instruction-message">
        Utilize a pesquisa ou selecione um veículo na lista acima para
        visualizar seus detalhes.
      </p>
    </div>

    <!-- 
      Conteúdo principal: detalhes do veículo e formulário de edição 
    -->
    <div
      class="section-edit__content"
      v-else>
      <div
        class="vehicle-content"
        :class="{ 'edit-mode': editMode }">
        <!-- 
          Card de visualização - Mostra os detalhes do veículo
          Quando no modo de edição, este card é reduzido para dar espaço ao formulário 
        -->
        <div
          class="vehicle-card"
          :class="{ reduced: editMode }">
          <!-- Imagem principal do veículo -->
          <img
            :src="car.imagem_principal_url || '/images/no-image.jpg'"
            alt="Imagem do veículo"
            class="vehicle-card__image" />

          <!-- Espaços para miniaturas (implementação futura) -->
          <div class="vehicle-card__thumbs">
            <div
              v-for="(thumb, index) in 4"
              :key="index"
              class="vehicle-card__thumb" />
          </div>

          <!-- Título e informações do veículo -->
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

        <!-- 
          Card de edição - Aparece apenas quando o usuário ativa o modo de edição
          Contém o formulário para modificar as propriedades do veículo 
        -->
        <div
          v-if="editMode"
          class="vehicle-edit-card">
          <h2 class="vehicle-edit-card__title">Editar Veículo</h2>
          <hr class="vehicle-edit-card__divider__edit" />

          <!-- 
            Seção de gerenciamento de imagens do veículo
            Permite visualizar e alterar imagens existentes 
          -->
          <div class="vehicle-images">
            <!-- 
              Imagem Principal com overlay de edição - Ao clicar, abre o seletor de arquivos 
            -->
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

            <!-- 
              Miniaturas de imagens - Uma ativa (a principal) e espaços para futuras imagens
              que podem ser adicionadas clicando nos ícones "+" 
            -->
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

              <!-- Espaços para futuras imagens adicionais -->
              <div
                v-for="index in 3"
                :key="index"
                class="thumbnail empty"
                @click="$refs.fileInput.click()">
                <span class="material-symbols-outlined add-icon"
                  >add_photo_alternate</span
                >
              </div>
            </div>
          </div>

          <!-- 
            Formulário de edição - Contém os campos para modificar as propriedades do veículo
            Ao enviar, chama o método saveChanges que atualiza o veículo na API 
          -->
          <form
            @submit.prevent="saveChanges"
            class="vehicle-edit-form">
            <!-- Campo de Modelo (apenas visualização - não editável) -->
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

            <!-- 
              Layout de dois campos lado a lado para melhor utilização do espaço
            -->
            <div class="form-group form-row">
              <!-- Campo de Ano de Fabricação -->
              <div class="form-col">
                <label for="car-year">Ano de Fabricação:</label>
                <input
                  id="car-year"
                  type="number"
                  v-model.number="editedCar.ano_fabricacao"
                  class="form-control"
                  required />
              </div>

              <!-- Campo de Cor -->
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

            <!-- Campo de Descrição - Área de texto multilinha -->
            <div class="form-group">
              <label for="car-desc">Descrição:</label>
              <textarea
                id="car-desc"
                v-model="editedCar.descricao_carro"
                class="form-control form-textarea"
                rows="5"></textarea>
            </div>

            <!-- 
              Input de arquivo oculto - Acionado pelos botões de edição de imagem
              Quando uma imagem é selecionada, o handleImageChange é disparado 
            -->
            <input
              ref="fileInput"
              id="car-image"
              type="file"
              @change="handleImageChange"
              class="hidden-input"
              accept="image/*" />

            <!-- Botões de ação do formulário -->
            <div class="form-buttons">
              <!-- Botão de salvar com feedback visual durante o salvamento -->
              <ButtonComponent
                class="save-button"
                size="large"
                bgColor="#3D5E73"
                textColor="#FFFFFF"
                fontSize="14px"
                type="submit"
                :disabled="isSaving">
                {{ isSaving ? "Salvando..." : "Salvar" }}
              </ButtonComponent>

              <!-- Botão de cancelar edição -->
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

// Hooks do Vue Router para trabalhar com navegação e parâmetros
const route = useRoute();
const router = useRouter();

// Estado principal dos dados do veículo e lista completa
const car = ref({}); // Dados do veículo atual
const cars = ref([]); // Lista completa de veículos para o select

// Estados de UI
const isLoading = ref(true); // Controla a exibição do loader
const errorMessage = ref(""); // Armazena mensagens de erro para exibição
const editMode = ref(false); // Controla se o formulário de edição está visível
const searchTerm = ref(""); // Texto digitado no campo de pesquisa
const selectedCarId = ref(""); // ID do veículo selecionado no dropdown
const showDeleteDialog = ref(false); // Controla a visibilidade do diálogo de confirmação
const fileInput = ref(null); // Referência ao input de arquivo (imagens)
const previewImage = ref(null); // URL de prévia da imagem selecionada
const showSearchResults = ref(false); // Controla a visibilidade do dropdown de resultados

// Objeto reativo para armazenar os dados do veículo em edição
// Usado para isolar as alterações antes de salvar
const editedCar = reactive({
  ano_fabricacao: 0,
  cor: "",
  descricao_carro: "",
  modelo_id: null,
  modelo_nome: "", // Nome do modelo para exibição no campo de visualização
});

// Estados relacionados ao upload de imagem e salvamento
const newImage = ref(null); // Arquivo de imagem selecionado para upload
const isSaving = ref(false); // Controla o estado de salvamento (feedback visual)

// Computed properties

/**
 * Determina se o componente está sendo acessado diretamente
 * através do menu ou via botão de visualização
 */
const isDirectAccess = computed(() => !route.params.id);

/**
 * Filtra a lista de carros com base no termo de pesquisa
 * Usada tanto para o dropdown quanto para o select
 */
const filteredCars = computed(() => {
  const term = searchTerm.value.trim().toLowerCase();
  if (!term) return cars.value; // Se não há termo, retorna a lista completa

  // Filtra os carros que correspondem ao termo de pesquisa
  return cars.value.filter((carItem) => {
    const marcaModelo =
      `${carItem.modelo?.nome_marca} ${carItem.modelo?.nome_modelo}`.toLowerCase();
    const cor = (carItem.cor || "").toLowerCase();
    const ano = carItem.ano_fabricacao?.toString() || "";

    // Retorna true se qualquer um dos campos contiver o termo
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
    name: "Visualizar e Editar Veiculo",
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
    // Se não houver ID e for acesso direto, apenas finaliza o carregamento
    if (isDirectAccess.value) {
      isLoading.value = false;
      return;
    }

    // Caso contrário, mostra erro
    errorMessage.value = "ID do veículo não especificado";
    isLoading.value = false;
    return;
  }

  try {
    isLoading.value = true;
    // Remove os zeros à esquerda do ID se necessário (converter 0003 para 3)
    const cleanId = id.replace(/^0+/, "");
    const response = await apiClient.getCarro(cleanId);
    car.value = response.data;

    // Inicializa os dados para edição com os valores atuais
    editedCar.ano_fabricacao = car.value.ano_fabricacao || 0;
    editedCar.cor = car.value.cor || "";
    editedCar.descricao_carro = car.value.descricao_carro || "";

    // Prepara o nome completo do modelo para exibição
    editedCar.modelo_nome = car.value.modelo
      ? `${car.value.modelo.nome_marca} ${car.value.modelo.nome_modelo}`
      : "";

    // Obtém o ID do modelo, convertendo de "CAR001" para 1 se necessário
    if (car.value.modelo?.id) {
      if (
        typeof car.value.modelo.id === "string" &&
        car.value.modelo.id.startsWith("CAR")
      ) {
        // Se o ID estiver no formato "CARxxx", extrai apenas o número
        editedCar.modelo_id = parseInt(
          car.value.modelo.id.replace("CAR", ""),
          10
        );
      } else {
        // Caso contrário, usa o valor como está
        editedCar.modelo_id = car.value.modelo?.id || null;
      }
    } else {
      editedCar.modelo_id = null;
    }

    // Limpa o preview da imagem
    previewImage.value = null;
  } catch (error) {
    // Tratamento de diferentes tipos de erro para feedback informativo
    if (error.response) {
      // Erro retornado pelo servidor com código de status
      errorMessage.value = `Erro ${error.response.status}: ${
        error.response.data?.detail || "Erro ao carregar dados do veículo"
      }`;
    } else if (error.request) {
      // Requisição enviada mas sem resposta (timeout, etc)
      errorMessage.value = "Sem resposta do servidor. Verifique sua conexão.";
    } else {
      // Erro durante a preparação da requisição
      errorMessage.value = `Erro: ${error.message}`;
    }
  } finally {
    // Sempre finaliza o estado de carregamento
    isLoading.value = false;
  }
};

/**
 * Busca todos os veículos disponíveis para o select e pesquisa
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
      name: "Visualizar e Editar Veiculo",
      params: { id: selectedCarId.value },
    });

    // Busca os detalhes do veículo selecionado
    fetchCarDetails(selectedCarId.value);
  }
};

/**
 * Exclui o veículo atual após confirmação do usuário
 * Chamado pelo diálogo de confirmação
 */
const confirmDelete = async () => {
  try {
    const carId = route.params.id || selectedCarId.value;
    // Remove os zeros à esquerda do ID se necessário
    const cleanCarId = carId.replace(/^0+/, "");
    await apiClient.deleteCarro(cleanCarId);
    alert("Veículo excluído com sucesso!");
    router.push("/"); // Redireciona para a página inicial após exclusão
  } catch (error) {
    alert(`Erro ao excluir veículo: ${error.message}`);
  }
};

/**
 * Volta para a tela de seleção de veículo (modo de acesso direto)
 * Mantém o mesmo URL, mas altera o estado do componente
 */
const backToSelection = async () => {
  // Limpa o ID da URL para evitar confusão
  router.replace({ path: "/edit" });

  // A mudança da rota acima vai causar a remontagem do componente com isDirectAccess = true

  // Carrega os carros para o select e a pesquisa
  await fetchAllCars();

  // Redefine outros estados relevantes
  editMode.value = false;
  errorMessage.value = "";
  selectedCarId.value = "";
  searchTerm.value = "";
};

/**
 * Manipulador para lidar com a seleção de uma nova imagem
 * Cria uma prévia da imagem selecionada e armazena o arquivo para upload
 */
const handleImageChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    newImage.value = file; // Armazena o arquivo para envio posteriormente

    // Criar uma prévia da imagem usando FileReader
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target.result; // URL base64 da imagem para prévia
    };
    reader.readAsDataURL(file);
  }
};

/**
 * Salva as alterações feitas no formulário
 * Envia dados para a API incluindo a nova imagem se houver
 */
const saveChanges = async () => {
  try {
    isSaving.value = true; // Ativa indicador de salvamento

    // Cria um FormData para envio multipart/form-data (necessário para upload de arquivos)
    const formData = new FormData();
    formData.append("ano_fabricacao", editedCar.ano_fabricacao);
    formData.append("cor", editedCar.cor);
    formData.append("descricao_carro", editedCar.descricao_carro);

    // Trata o modelo_id, garantindo formato correto para a API
    if (editedCar.modelo_id) {
      // Se o ID do modelo estiver no formato "CARxxx", extrai apenas o número
      if (
        typeof editedCar.modelo_id === "string" &&
        editedCar.modelo_id.startsWith("CAR")
      ) {
        const numericId = parseInt(editedCar.modelo_id.replace("CAR", ""), 10);
        formData.append("modelo_id", numericId);
      } else {
        // Caso contrário, usa o valor como está
        formData.append("modelo_id", editedCar.modelo_id);
      }
    }

    // Adiciona a nova imagem ao FormData se houver
    if (newImage.value) {
      formData.append("imagem_principal", newImage.value);
    }

    // Enviar para API
    const carId = route.params.id || selectedCarId.value;
    // Remove os zeros à esquerda do ID se necessário
    const cleanCarId = carId.replace(/^0+/, "");
    await apiClient.updateCarro(cleanCarId, formData);

    // Recarrega os detalhes atualizados do veículo
    await fetchCarDetails(carId);

    // Sai do modo de edição após salvar com sucesso
    editMode.value = false;
    alert("Veículo atualizado com sucesso!");
  } catch (error) {
    alert(`Erro ao atualizar veículo: ${error.message}`);
    console.error("Erro ao atualizar:", error);
  } finally {
    isSaving.value = false; // Desativa indicador de salvamento
  }
};

/**
 * Cancela a edição e restaura valores originais
 * Descarta alterações não salvas
 */
const cancelEdit = () => {
  // Restaura os valores originais do veículo
  editedCar.ano_fabricacao = car.value.ano_fabricacao || 0;
  editedCar.cor = car.value.cor || "";
  editedCar.descricao_carro = car.value.descricao_carro || "";
  editedCar.modelo_id = car.value.modelo?.id || null;
  editedCar.modelo_nome = car.value.modelo
    ? `${car.value.modelo.nome_marca} ${car.value.modelo.nome_modelo}`
    : "";

  // Limpa a seleção de imagem e sua prévia
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

// Hook de ciclo de vida - executado quando o componente é montado
onMounted(async () => {
  if (isDirectAccess.value) {
    // Se for acesso direto pelo menu, busca todos os carros para o select
    await fetchAllCars();

    // Verificar se há um ID salvo e tentar carregar automaticamente
    // Recurso de conveniência para manter o último veículo visualizado
    const savedVehicleId = localStorage.getItem("lastViewedVehicleId");
    if (savedVehicleId) {
      selectedCarId.value = savedVehicleId;
      // Carrega automaticamente os detalhes do veículo
      await fetchCarDetails(savedVehicleId);
    }

    isLoading.value = false;
  } else {
    // Se for acesso via botão Visualizar, busca apenas o carro específico
    fetchCarDetails(route.params.id);
  }
});
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

// Estilos principais do componente
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
    font-family: $font-primary; // Variável de fonte definida no arquivo de variáveis
    font-size: 29px;
    font-weight: 500;
    color: $color-text-secondary; // Variável de cor definida no arquivo de variáveis
  }

  // Estilos para o modo de acesso direto
  &__direct-access {
    width: 100%;
    margin-top: 20px;
  }

  // Container para o campo de pesquisa e dropdown
  &__search-container {
    display: flex;
    align-items: center;
    gap: 15px;
    width: 100%;
  }

  // Wrapper para posicionar o dropdown de resultados
  &__search-wrapper {
    position: relative;
    flex: 1;
  }

  // Campo de pesquisa com ícone
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

    // Input dentro do campo de pesquisa
    &-input {
      border: none;
      outline: none;
      flex: 1;
      background-color: transparent;
      font-size: 14px;
    }
  }

  // Dropdown de resultados da pesquisa
  &__search-results {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    max-height: 250px;
    overflow-y: auto; // Barra de rolagem se houver muitos resultados
    background-color: white;
    border: 1px solid $color-border-table;
    border-top: none; // Conecta visualmente ao campo de pesquisa
    border-radius: 0 0 6px 6px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 10; // Para sobrepor outros elementos
  }

  // Item individual no dropdown de resultados
  &__search-option {
    padding: 10px 16px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    color: $color-text-secondary;

    &:hover {
      background-color: #f5f5f5; // Destaca o item ao passar o mouse
    }
  }

  // Mensagem quando nenhum resultado é encontrado
  &__search-no-results {
    padding: 10px 16px;
    color: $color-text-tertiary;
    font-style: italic;
  }

  // Select tradicional (alternativa ao campo de pesquisa)
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

  // Container dos botões de ação
  &__actions {
    display: flex;
    align-items: center;
    gap: 20px;
  }

  // Área principal de conteúdo
  &__content {
    margin: 0 55px 68px 55px;
  }

  // Estilos para mensagens de estado
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

  // Seção de gerenciamento de imagens do veículo
  .vehicle-images {
    display: flex;
    flex-direction: column;
    gap: 10px;

    // Container da imagem principal com overlay de edição
    .main-image-container {
      position: relative;
      width: 100%;
      height: 240px;
      border-radius: 8px;
      overflow: hidden;

      .main-image {
        width: 100%;
        height: 100%;
        object-fit: cover; // Mantém a proporção da imagem
      }

      // Overlay que aparece ao passar o mouse para editar a imagem
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
        background-color: rgba(0, 0, 0, 0.5); // Fundo semi-transparente
        color: white;
        opacity: 0; // Inicialmente invisível
        transition: opacity 0.3s ease; // Animação suave
        cursor: pointer;

        &:hover {
          opacity: 1; // Aparece ao passar o mouse
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

    // Container das miniaturas
    .thumbnail-container {
      display: flex;
      gap: 10px;

      // Item individual de miniatura
      .thumbnail {
        position: relative;
        width: 80px;
        height: 60px;
        border-radius: 4px;
        overflow: hidden;
        cursor: pointer;

        // Destaque para a miniatura ativa
        &.active {
          border: 2px solid $color-button-primary;
        }

        // Estilo para miniaturas vazias (placeholder)
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

        // Ícone de edição que aparece ao passar o mouse
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

  // Layout para o conteúdo do veículo (visualização e edição)
  .vehicle-content {
    display: flex;
    gap: 20px;

    // Ajuste de layout quando em modo de edição
    &.edit-mode {
      justify-content: space-between;
    }
  }

  // Card de visualização do veículo
  .vehicle-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 100%;
    max-width: 428px;
    height: 100%;
    min-height: 737px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    background-color: $color-bg-page-edit-view;
    transition: width 0.3s ease; // Animação suave ao reduzir

    // Quando em modo de edição, o card é reduzido
    &.reduced {
      max-width: 100%;
      width: 38%; // Quando na edição do veiculo, card de visualização fica com 38%
    }

    &__image {
      width: 100%;
      max-height: 235px;
      object-fit: cover;
      border-radius: 8px;
    }

    // Container das miniaturas
    &__thumbs {
      display: flex;
      gap: 10px;
    }

    // Miniatura individual (placeholder)
    &__thumb {
      width: 60px;
      height: 60px;
      border-radius: 4px;
      background-color: #f0f0f0;
      // Padrão xadrez para indicar fundo transparente
      background-image: linear-gradient(45deg, #ccc 25%, transparent 25%),
        linear-gradient(-45deg, #ccc 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #ccc 75%),
        linear-gradient(-45deg, transparent 75%, #ccc 75%);
      background-size: 12px 12px;
      background-position: 0 0, 0 6px, 6px -6px, -6px 0px;
    }

    &__title {
      font-family: $font-secondary;
      font-size: 18px;
      font-weight: 600;
      text-align: start;
      line-height: 150%;
      color: $color-text-secondary;
    }

    &__divider {
      border: 0;
      border-top: 1px solid $color-light-bg;
    }

    // Informações detalhadas do veículo
    &__info {
      display: flex;
      flex-direction: column;
      gap: 10px;

      p {
        font-family: $font-secondary;
        font-size: 14px;
        font-weight: 400;
        line-height: 150%;
        color: $color-text-secondary;
      }
    }
  }

  // Card de edição (aparece apenas em modo de edição)
  .vehicle-edit-card {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 60%; // Ocupa 60% do espaço quando visível
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

      // Estilo dos campos do formulário
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

      // Ajustes específicos para áreas de texto
      .form-textarea {
        resize: vertical; // Permite redimensionar verticalmente
        min-height: 100px;
      }
    }

    // Container dos botões do formulário
    .form-buttons {
      display: flex;
      justify-content: flex-end;
      gap: 15px;
      margin-top: 30px;
    }
  }

  // Input de arquivo oculto (acionado pelos botões de edição)
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
      // Em telas pequenas, empilha os cards de visualização e edição
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
