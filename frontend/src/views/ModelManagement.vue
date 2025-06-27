<template>
  <section class="model-management">
    <!-- Dialog de confirmação para exclusão -->
    <DialogAlert
      :isVisible="showDeleteDialog"
      :message="`Tem certeza que deseja excluir o modelo: ${
        modelToDelete ? modelToDelete.nome_modelo : ''
      }?`"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
      @close="cancelDelete" />

    <!--Alert Componente-->
    <AlertComponent
      :isVisible="showAlert"
      :message="alertMessage"
      :type="alertType"
      @close="showAlert = false" />

    <header class="model-management__header">
      <h1 class="model-management__title">Gerenciamento de Modelos</h1>
      <ButtonComponent
        class="model-management__add-button"
        size="large"
        bgColor="#3D5E73"
        textColor="#FFFFFF"
        fontSize="12px"
        fontWeight="600"
        @click="addModel">
        Cadastrar Modelo
      </ButtonComponent>
    </header>

    <div
      v-if="isLoading"
      class="model-management__status-message">
      Carregando modelos...
    </div>
    <div
      v-else-if="errorMessage"
      class="model-management__status-message model-management__status-message--error">
      {{ errorMessage }}
    </div>

    <table
      v-else
      class="model-management__table">
      <thead>
        <tr>
          <th>ID Modelo</th>
          <th>Marca</th>
          <th>Ano</th>
          <th>Modelo</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="modelo in modelos"
          :key="modelo.id">
          <td>{{ modelo.id }}</td>
          <td>{{ modelo.nome_marca }}</td>
          <td>{{ modelo.ano_modelo }}</td>
          <td>{{ modelo.nome_modelo }}</td>
          <td class="model-management__actions">
            <ButtonComponent
              size="little"
              bgColor="#878787"
              textColor="#FFFFFF"
              height="40px"
              @click="editModel(modelo)">
              <span class="material-symbols-outlined">edit</span>
            </ButtonComponent>
            <ButtonComponent
              size="little"
              bgColor="#FF0000"
              textColor="#FFFFFF"
              height="40px"
              @click="prepareDelete(modelo)">
              <span class="material-symbols-outlined">delete</span>
            </ButtonComponent>
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import apiClient from "../services/api";
import ButtonComponent from "../components/ButtonComponent.vue";
import DialogAlert from "../components/DialogAlert.vue";
import AlertComponent from "../components/AlertComponent.vue";

const router = useRouter();

// Estado para os dados e UI
const modelos = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");

// Estado para o alerta
const showAlert = ref(false);
const alertMessage = ref("");
const alertType = ref("");

// Estado para o dialog de exclusão
const showDeleteDialog = ref(false);
const modelToDelete = ref(null);

// Busca os modelos da API
const fetchModelos = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const response = await apiClient.getModelos();
    modelos.value = response.data.results || response.data;
  } catch (error) {
    console.error("Erro ao buscar modelos:", error);
    errorMessage.value =
      "Falha ao carregar os modelos. Tente novamente mais tarde.";
  } finally {
    isLoading.value = false;
  }
};

// Funções de ação
const addModel = () => {
  router.push({ name: "Add Modelo" });
};

const editModel = (modelo) => {
  router.push({
    name: "Add Modelo",
    params: { id: modelo.id },
  });
};

const prepareDelete = (modelo) => {
  modelToDelete.value = modelo;
  showDeleteDialog.value = true;
};

const confirmDelete = async () => {
  if (!modelToDelete.value) return;
  const modelName = modelToDelete.value.nome_modelo;

  try {
    const numericId = parseInt(
      String(modelToDelete.value.id).replace(/\D/g, ""),
      10
    );
    if (isNaN(numericId)) {
      throw new Error("ID do modelo inválido para exclusão.");
    }

    await apiClient.deleteModelo(numericId);
    // mostra alert de sucesso
    alertType.value = "success";
    alertMessage.value = `Modelo ${modelName} excluído com sucesso!`;
    showAlert.value = true;
    await fetchModelos();
  } catch (error) {
    console.error("Erro ao excluir modelo:", error);
    alertType.value = "error";
    if (error.response?.status === 500) {
      alertMessage.value = `Não é possível excluir o modelo ${modelName} porque ele está sendo usado por um ou mais veículos.`;
    } else {
      alertMessage.value = `Falha ao excluir o modelo: ${
        error.response?.data?.detail || error.message
      }`;
    }
    showAlert.value = true;
  } finally {
    cancelDelete();
  }
};

const cancelDelete = () => {
  showDeleteDialog.value = false;
  modelToDelete.value = null;
};

onMounted(() => {
  fetchModelos();
});
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;
@use "sass:color";

.model-management {
  padding: 44px 40px;

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    &__add-button {
      font-family: $font-primary;
    }
  }

  &__title {
    font-family: $font-primary;
    font-size: 29px;
    font-weight: 500;
    color: $color-text-secondary;
  }

  &__status-message {
    padding: 20px;
    text-align: center;
    font-size: 1.2rem;
    color: $color-text-tertiary;

    &--error {
      color: $color-button-danger;
      font-weight: 500;
    }
  }

  &__table {
    width: 100%;
    margin-top: 20px;
    border: 1px solid $color-border-table;
    border-radius: 8px;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba($color-dark-bg, 0.05);

    thead {
      th {
        padding: 16px;
        text-align: left;
        font-family: $font-primary;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px dashed $color-border-table;
      }
    }

    tbody {
      font-size: 14px;
      font-weight: 500;
      color: $color-text-secondary;
      border-bottom: 1px dashed $color-border-table;

      tr {
        &:last-child td {
          border-bottom: none;
        }
      }

      td {
        padding: 12px 16px;
        font-family: $font-primary;
        font-size: 14px;
        font-weight: 500;
        color: $color-text-secondary;
        border-bottom: 1px solid
          color.adjust($color-border-table, $lightness: 35%);
      }
    }
  }

  &__actions {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;

    .material-symbols-outlined {
      display: flex;
      align-items: center;
      font-size: 18px;
    }
  }
}
</style>
