<template>
  <section class="add-model__section">
    <h1 class="section-title__title">Cadastro e Edição de Modelos</h1>
    <section class="content">
      <!-- Cadastro de Modelo -->
      <div class="cadastro-modelo">
        <h2 class="section-title">Cadastro de Modelos</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <div class="field">
              <label for="codigo">ID Modelo</label>
              <input
                type="number"
                id="codigo"
                disabled
                placeholder="Será gerado automaticamente"
                class="disabled-input" />
            </div>
            <div class="field">
              <label for="marca">Marca</label>
              <input
                type="text"
                id="marca"
                v-model="form.nome_marca"
                placeholder="Ford"
                required />
            </div>
            <div class="field">
              <label for="modelo">Nome do Modelo</label>
              <input
                type="text"
                id="modelo"
                v-model="form.nome_modelo"
                placeholder="Territory"
                required />
            </div>
            <div class="field">
              <label for="ano">Ano do Modelo</label>
              <input
                type="number"
                id="ano"
                v-model="form.ano_modelo"
                placeholder="2020"
                required />
            </div>
            <div class="field__description">
              <label for="descricao">Descrição</label>
              <textarea
                rows="4"
                type="text"
                id="descricao"
                v-model="form.descricao_modelo"
                placeholder="Ford Territory SEL"
                required />
            </div>
          </div>

          <ButtonComponent
            class="submit-button"
            type="submit"
            size="xxlarge"
            textColor="#fff"
            fontSize="16px"
            fontWeight="500"
            height="49px"
            :disabled="isSubmitting">
            {{ isSubmitting ? "Cadastrando..." : "Cadastrar Modelo" }}
          </ButtonComponent>
        </form>
      </div>

      <!-- Cadastro com Sucesso -->
      <div
        class="success-card"
        v-if="showSuccess">
        <h2 class="section-title">Modelo Cadastrado com Sucesso!</h2>
        <div class="form-group">
          <div class="field">
            <label>ID Modelo</label>
            <input
              type="text"
              :value="success?.id || ''"
              readonly />
          </div>
          <div class="field">
            <label>Marca</label>
            <input
              type="text"
              :value="success?.nome_marca || ''"
              readonly />
          </div>
          <div class="field">
            <label>Nome do Modelo</label>
            <input
              type="text"
              :value="success?.nome_modelo || ''"
              readonly />
          </div>
          <div class="field">
            <label>Ano do Modelo</label>
            <input
              type="text"
              :value="success?.ano_modelo || ''"
              readonly />
          </div>
          <div class="field__description">
            <label>Descrição</label>
            <textarea
              :rows="3"
              type="text"
              :value="success?.descricao_modelo || ''"
              readonly />
          </div>
        </div>

        <ButtonComponent
          class="submit-button"
          @click="showSuccess = false"
          size="xxlarge"
          fontSize="16px"
          fontWeight="500"
          height="49px"
          textColor="#fff">
          Cadastrar Outro Modelo
        </ButtonComponent>
      </div>

      <!-- Edição de Modelo -->
      <div class="edit-modelo">
        <h2 class="section-title">Edição de Modelo</h2>
        <form @submit.prevent="handleEdit">
          <div class="form-group">
            <div class="field search-field">
              <label for="edit-codigo">ID Modelo</label>
              <div class="input-with-button">
                <input
                  type="text"
                  id="edit-codigo"
                  v-model="editForm.codigo"
                  placeholder="Informe o código para buscar"
                  required />
                <ButtonComponent
                  class="search-button"
                  @click.prevent="handleSearchModel"
                  size="small"
                  textColor="#fff"
                  fontSize="14px"
                  fontWeight="500"
                  height="38px">
                  Buscar
                </ButtonComponent>
              </div>
            </div>
            <div class="field">
              <label for="edit-marca">Marca</label>
              <input
                type="text"
                id="edit-marca"
                v-model="editForm.nome_marca"
                placeholder="Alterar Marca" />
            </div>
            <div class="field">
              <label for="edit-modelo">Nome do Modelo</label>
              <input
                type="text"
                id="edit-modelo"
                v-model="editForm.nome_modelo"
                placeholder="Alterar Modelo" />
            </div>
            <div class="field">
              <label for="edit-ano">Ano do Modelo</label>
              <input
                type="number"
                id="edit-ano"
                v-model="editForm.ano_modelo"
                placeholder="Alterar Ano" />
            </div>
            <div class="field__description">
              <label for="edit-descricao">Descrição</label>
              <textarea
                rows="4"
                type="text"
                id="edit-descricao"
                v-model="editForm.descricao_modelo"
                placeholder="Alterar Descrição" />
            </div>
          </div>

          <ButtonComponent
            class="submit-button"
            type="submit"
            size="xxlarge"
            textColor="#fff"
            fontSize="16px"
            fontWeight="500"
            height="49px">
            Salvar Alterações
          </ButtonComponent>
        </form>
      </div>

      <!-- ALERTA DE ERRO -->
      <AlertComponent
        v-if="alert.visible"
        :isVisible="alert.visible"
        :message="alert.message"
        :type="alert.type"
        @close="alert.visible = false" />
    </section>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRoute } from "vue-router";
import ButtonComponent from "../components/ButtonComponent.vue";
import AlertComponent from "../components/AlertComponent.vue";
import apiClient from "../services/api";

// Hooks do Vue Router
const route = useRoute();

// Estado reativo para os formulários
const form = reactive({
  nome_marca: "",
  nome_modelo: "",
  ano_modelo: "",
  descricao_modelo: "",
});

const editForm = reactive({
  codigo: "",
  nome_marca: "",
  nome_modelo: "",
  ano_modelo: "",
  descricao_modelo: "",
});

// Estado para alertas
const alert = reactive({
  visible: false,
  message: "",
  type: "error",
});

// Estados para controlar a UI
const showSuccess = ref(false);
const isSubmitting = ref(false);
const errorMessage = ref("");
const success = ref(null);

// Antes de enviar o modelo para a API, adicione uma verificação
async function checkIfModelExists(brand, model, year) {
  try {
    const response = await apiClient.getModelos();
    const modelos = response.data.results || [];

    return modelos.some(
      (m) =>
        m.nome_marca.toLowerCase() === brand.toLowerCase() &&
        m.nome_modelo.toLowerCase() === model.toLowerCase() &&
        m.ano_modelo === year
    );
  } catch (error) {
    console.error("Erro ao verificar existência do modelo:", error);
    return false;
  }
}

/**
 * Manipula o envio do formulário de cadastro
 * Envia os dados para a API e exibe o card de sucesso
 */
async function handleSubmit() {
  if (isSubmitting.value) return;

  try {
    isSubmitting.value = true;
    errorMessage.value = "";

    // Validação básica
    if (!form.nome_marca || !form.nome_modelo || !form.ano_modelo) {
      errorMessage.value = "Por favor, preencha os campos obrigatórios.";
      alert.message = errorMessage.value;
      alert.type = "error";
      alert.visible = true;
      return;
    }

    // Verifica se o modelo já existe antes de enviar
    const modelExists = await checkIfModelExists(
      form.nome_marca.trim(),
      form.nome_modelo.trim(),
      parseInt(form.ano_modelo, 10)
    );

    if (modelExists) {
      alert.message = `O modelo ${form.nome_marca} ${form.nome_modelo} (${form.ano_modelo}) já está cadastrado.`;
      alert.type = "error";
      alert.visible = true;
      isSubmitting.value = false;
      return;
    }

    // Prepara os dados para envio
    const modeloData = {
      nome_marca: form.nome_marca.trim(),
      nome_modelo: form.nome_modelo.trim(),
      ano_modelo: parseInt(form.ano_modelo, 10),
      descricao_modelo: form.descricao_modelo || "",
    };

    // Envia para a API
    const response = await apiClient.createModelo(modeloData);

    // Armazena dados de sucesso para mostrar no card
    success.value = response.data;

    // Mostra card de sucesso
    showSuccess.value = true;

    // Limpa o formulário
    Object.assign(form, {
      nome_marca: "",
      nome_modelo: "",
      ano_modelo: "",
      descricao_modelo: "",
    });
  } catch (error) {
    console.error("Erro ao cadastrar modelo:", error);

    // Mensagem específica para o erro de unicidade
    if (error.response?.data?.non_field_errors) {
      const message = error.response.data.non_field_errors.join("\n");
      alert.message = `Erro: ${message}\n\nJá existe um modelo com essa combinação de marca, nome e ano.`;
      alert.type = "error";
      alert.visible = true;
    } else if (error.response && error.response.data) {
      const errorDetails = Object.entries(error.response.data)
        .map(([field, errors]) => `${field}: ${errors.join(", ")}`)
        .join("\n");

      errorMessage.value = `Erro ao cadastrar modelo:\n${errorDetails};`;
      alert.message = errorMessage.value;
      alert.type = "error";
      alert.visible = true;
    } else {
      errorMessage.value =
        "Ocorreu um erro ao cadastrar o modelo. Por favor, tente novamente.";
      alert.message = errorMessage.value;
      alert.type = "error";
      alert.visible = true;
    }
  } finally {
    isSubmitting.value = false;
  }
}

/**
 * Função para buscar os detalhes do modelo pelo ID
 * @param {string} id - ID do modelo (pode ser "Mxxxx" ou numérico)
 */
async function fetchModelDetails(id) {
  try {
    const cleanId = String(id).replace(/^M/, "");
    const numericId = parseInt(cleanId, 10);

    if (isNaN(numericId)) {
      alert.message = "ID do modelo inválido.";
      alert.type = "error";
      alert.visible = true;
      Object.assign(editForm, {
        nome_marca: "",
        nome_modelo: "",
        ano_modelo: "",
        descricao_modelo: "",
      });
      return;
    }

    const response = await apiClient.getModelo(numericId);

    editForm.codigo = response.data.id;
    editForm.nome_marca = response.data.nome_marca;
    editForm.nome_modelo = response.data.nome_modelo;
    editForm.ano_modelo = response.data.ano_modelo;
    editForm.descricao_modelo = response.data.descricao_modelo;
  } catch (error) {
    // Se não encontrar, mostra alerta amigável
    alert.message = "O modelo buscado nao está cadastrado";
    alert.type = "error";
    alert.visible = true;
    Object.assign(editForm, {
      nome_marca: "",
      nome_modelo: "",
      ano_modelo: "",
      descricao_modelo: "",
    });
  }
}

/**
 * Manipula a busca do modelo pelo ID
 */
async function handleSearchModel() {
  if (!editForm.codigo) {
    alert.message = "Por favor, informe o código do modelo para buscar.";
    alert.type = "error";
    alert.visible = true;
    return;
  }
  await fetchModelDetails(editForm.codigo);
}

/**
 * Manipula o envio do formulário de edição
 */
async function handleEdit() {
  if (isSubmitting.value) return;

  try {
    isSubmitting.value = true;
    errorMessage.value = "";

    if (!editForm.codigo) {
      errorMessage.value = "Por favor, informe o código do modelo.";
      alert.message = errorMessage.value;
      alert.type = "error";
      alert.visible = true;
      return;
    }

    const modeloId = editForm.codigo.replace(/^M/, "");

    const updateData = {};
    if (editForm.nome_marca) updateData.nome_marca = editForm.nome_marca;
    if (editForm.nome_modelo) updateData.nome_modelo = editForm.nome_modelo;
    if (editForm.ano_modelo)
      updateData.ano_modelo = parseInt(editForm.ano_modelo, 10);
    if (editForm.descricao_modelo)
      updateData.descricao_modelo = editForm.descricao_modelo;

    if (Object.keys(updateData).length > 0) {
      await apiClient.updateModelo(modeloId, updateData);
      alert.message = "Modelo atualizado com sucesso!";
      alert.type = "success";
      alert.visible = true;

      Object.assign(editForm, {
        codigo: "",
        nome_marca: "",
        nome_modelo: "",
        ano_modelo: "",
        descricao_modelo: "",
      });
    } else {
      alert.message = "Nenhuma alteração para salvar.";
      alert.type = "info";
      alert.visible = true;
    }
  } catch (error) {
    console.error("Erro ao atualizar modelo:", error);
    alert.message =
      error.response?.data?.detail ||
      "Erro ao atualizar o modelo. Verifique o código e tente novamente.";
    alert.type = "error";
    alert.visible = true;
  } finally {
    isSubmitting.value = false;
  }
}

onMounted(() => {
  const modelId = route.params.id;
  if (modelId) {
    fetchModelDetails(modelId);
  }
});
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

.add-model__section {
  padding: 29px 22px 0 22px;

  .section-title__title {
    color: $color-text-secondary;
    font-family: $font-primary;
    font-size: 29px;
    font-weight: 500;
    text-align: center;
    line-height: 121.168%;
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 30px;
    padding: 27px 0;
  }

  .cadastro-modelo,
  .edit-modelo {
    background-color: $color-primary;
    border: 1px solid $color-border-table;
    border-radius: 8px;
    padding: 20px;
  }

  .section-title {
    color: $color-light-text;
    font-family: $font-primary;
    font-size: 29px;
    font-weight: 500;
    text-align: center;
    line-height: 121.168%;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin-top: 30px;
  }

  .form-group {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 20px;
  }

  .submit-button {
    display: block;
    margin: 0 auto;
    font-family: $font-primary;
  }

  .field {
    flex: 1;
    min-width: 220px;
    display: flex;
    flex-direction: column;

    &__description {
      display: flex;
      flex-direction: column;
      gap: 10px;
      flex: 1;
      min-width: 100%;

      textarea {
        padding: 10px;
        border-radius: 4px;
      }
    }
  }

  // Estilos específicos para o campo de busca na edição
  .search-field {
    flex-basis: 100%;
  }

  .input-with-button {
    display: flex;
    gap: 10px;
    align-items: flex-end;

    input {
      flex-grow: 1;
    }
  }

  label {
    padding-bottom: 10px;
    font-size: 16px;
    color: $color-light-text;
    font-weight: 500;
    font-family: $font-primary;
    line-height: 15px;
    max-width: 150px;
  }

  input {
    padding: 10px;
    border: 1px solid $color-border-table;
    border-radius: 4px;
    font-size: 14px;
    font-family: $font-secondary;
  }

  .success-card {
    border: 2px solid $color-border-table;
    background-color: $color-primary;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(139, 138, 138, 0.1);
    margin-bottom: 30px;

    h2 {
      margin-bottom: 20px;
      line-height: 15px;
    }

    input {
      background-color: $color-light-bg;
      border-color: $color-border-table;
      color: $color-dark-text;
      font-weight: 600;
      font-family: $font-secondary;
    }
  }
}

@media (max-width: 768px) {
  .add-model__section {
    .field {
      min-width: 100%;
    }
  }
}
</style>
