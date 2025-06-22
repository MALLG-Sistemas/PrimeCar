<template>
  <section class="section-add-veiculo">
    <div class="container">
      <h1 class="title">Adicionar Veículo</h1>
      <ButtonComponent @click="addVehicle" size="xlarge" bgColor="#3D5E73" textColor="#FFFFFF" fontSize="14px">
        Adicionar Veículo
      </ButtonComponent>
    </div>

    <div class="container-data">
      <h2 class="title-data">Dados do Veículo</h2>

      <form @submit.prevent="addVehicle" class="form-layout">
        <!-- Linha 1 do Formulário -->
        <div class="form-row">
          <div class="form-group">
            <label class="label-general" for="modelo">Modelo</label>
            <select id="modelo" v-model="newVehicle.modelo_id" class="input-geral" required>
              <option :value="null" disabled>
                Selecione um modelo
              </option>
              <option v-for="modelo in modelos" :key="modelo.id" :value="modelo.id.replace('M', '')">
                {{ modelo.nome_marca }} {{ modelo.nome_modelo }} ({{
                  modelo.ano_modelo
                }})
              </option>
            </select>
          </div>
          <div class="form-group">
            <label class="label-general" for="ano">Ano Fabricação</label>
            <input class="input-geral-two" type="number" id="ano" v-model.number="newVehicle.ano_fabricacao"
              placeholder="2023" required />
          </div>
        </div>

        <!-- Linha 2 do Formulário -->
        <div class="form-row">
          <div class="form-group">
            <label class="label-general" for="cor">Cor</label>
            <input class="input-geral" type="text" id="cor" v-model="newVehicle.cor" placeholder="Vermelho" required />
          </div>
          <div class="form-group">
            <label class="label-general" for="descricao">Descrição</label>
            <input class="input-geral-two" type="text" id="descricao" v-model="newVehicle.descricao_carro"
              placeholder="Carro impecável" />
          </div>
        </div>
      </form>
    </div>

    <div class="container-images">
      <h2 class="title-data">Fotos/Imagens</h2>
      <div class="image-gallery">
        <div class="image-slot main-slot" @click="triggerFileInput">
          <img v-if="imagePreviews[0]" :src="imagePreviews[0]" alt="Preview principal" />
          <span v-else class="material-symbols-outlined add-icon">
            add_photo_alternate
          </span>
        </div>
        <div class="thumbnail-flex">
          <div class="thumbnail-grid">
            <div v-for="i in 4" :key="i" class="image-slot thumb-slot" @click="triggerFileInput">
              <img v-if="imagePreviews[i]" :src="imagePreviews[i]" :alt="`Preview ${i + 1}`" />
              <span v-else class="material-symbols-outlined add-icon">add_photo_alternate
              </span>
            </div>
          </div>
          <div class="thumbnail-grid">
            <div v-for="i in 4" :key="i" class="image-slot thumb-slot" @click="triggerFileInput">
              <img v-if="imagePreviews[i]" :src="imagePreviews[i]" :alt="`Preview ${i + 1}`" />
              <span v-else class="material-symbols-outlined add-icon">add_photo_alternate
              </span>
            </div>
          </div>
        </div>
      </div>
      <input type="file" ref="fileInput" @change="handleImageUpload" multiple accept="image/*" class="file-input" />
    </div>
  </section>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import apiClient from "../services/api";
import ButtonComponent from "../components/ButtonComponent.vue";

const router = useRouter();
const modelos = ref([]);
const fileInput = ref(null);
const imagePreviews = ref([]);

const newVehicle = reactive({
  modelo_id: null,
  ano_fabricacao: null,
  cor: "",
  descricao_carro: "",
  imagens_para_upload: [],
});

const fetchModelos = async () => {
  try {
    const response = await apiClient.getModelos();
    modelos.value = response.data.results || [];
  } catch (error) {
    console.error("Erro ao buscar modelos:", error);
    alert("Não foi possível carregar os modelos de veículos.");
  }
};

const addVehicle = async () => {
  if (!newVehicle.modelo_id) {
    alert("Por favor, selecione um modelo.");
    return;
  }

  const formData = new FormData();
  formData.append("modelo_id", newVehicle.modelo_id);
  formData.append("ano_fabricacao", newVehicle.ano_fabricacao);
  formData.append("cor", newVehicle.cor);
  formData.append("descricao_carro", newVehicle.descricao_carro);

  if (newVehicle.imagens_para_upload.length > 0) {
    newVehicle.imagens_para_upload.forEach((file) => {
      formData.append("imagens_para_upload", file);
    });
  }

  try {
    await apiClient.createCarro(formData);
    alert("Veículo adicionado com sucesso!");
    router.push("/");
  } catch (error) {
    console.error("Erro ao adicionar veículo:", error);
    alert("Erro ao adicionar veículo. Verifique os dados e tente novamente.");
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleImageUpload = (event) => {
  const files = Array.from(event.target.files);
  newVehicle.imagens_para_upload = files;

  imagePreviews.value = [];
  files.forEach((file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreviews.value.push(e.target.result);
    };
    reader.readAsDataURL(file);
  });
};

onMounted(fetchModelos);
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *; // Importa as variáveis SCSS
@use "sass:math"; // Importa funções matemáticas do Sass

/* 
  Estilos para a seção principal de adicionar veículo
  Define o layout flexível e o espaçamento entre os elementos
*/
.section-add-veiculo {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 40px;
  gap: 40px;
  width: 100%;
  max-width: 1200px;
  box-sizing: border-box;
  overflow-x: hidden;

  /* Estilos para o container principal */
  .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
  }

  /* Estilos para o título da página */
  .title {
    color: $color-text-secondary;
    font-family: $font-primary;
    font-size: 29px;
    font-weight: 500;
  }
}

/* 
  Estilos para o container de dados do veículo
  Define a largura, preenchimento, sombra e cor de fundo
*/
.container-data {
  width: 100%;
  padding: 50px 25px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  box-sizing: border-box;
  background-color: #242323;
}

/* 
  Estilos para o container de imagens
  Semelhante ao container de dados, mas específico para imagens
*/
.container-images {
  width: 100%;
  padding: 50px 25px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #242323;
}

/* 
  Estilos para a galeria de imagens
  Define o layout flexível e o espaçamento entre as imagens
*/
.image-gallery {
  display: flex;
  gap: 20px;
}

/* Estilos para o título dos dados */
.title-data {
  color: $color-light-text;
  font-family: $font-primary;
  font-size: 22px;
  font-weight: 500;
  margin-bottom: 20px;
}

/* 
  Estilos para o layout do formulário
  Define o layout flexível e o espaçamento entre os elementos
*/
.form-layout {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 
  Estilos para a linha do formulário
  Define o layout flexível e o alinhamento dos elementos
*/
.form-row {
  display: flex;
  gap: 150px;
}

/* 
  Estilos para o grupo do formulário
  Define o layout flexível e o espaçamento entre os elementos
*/
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Estilos para o rótulo geral */
.label-general {
  color: $color-light-text;
  font-family: $font-primary;
  font-size: 14px;
  font-weight: 600;
}

/* 
  Estilos para os inputs gerais
  Define a altura, preenchimento, borda, fonte e cor do texto
*/
.input-geral,
.input-geral-two,
select.input-geral {
  height: 45px;
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid $color-border-table;
  font-family: $font-primary;
  font-size: 16px;
  font-weight: 400;

  /* Estilos para o placeholder */
  &::placeholder {
    color: $color-text-tertiary;
  }
}

/* Estilos para o input geral */
.input-geral {
  width: 100%;
  min-width: 390px;
  max-width: 690px;
  flex: 1 1 0;
  box-sizing: border-box;
}

/* Estilos para o input geral dois */
.input-geral-two {
  width: 100%;
  min-width: 290px;
  max-width: 500px;
  flex: 1 1 0;
  box-sizing: border-box;
}

/* 
  Estilos para o slot de imagem
  Define a cor de fundo, imagem de fundo, borda, cursor e overflow
*/
.image-slot {
  background-color: #f0f0f0;
  background-image: linear-gradient(45deg, #ccc 25%, transparent 25%),
    linear-gradient(-45deg, #ccc 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #ccc 75%),
    linear-gradient(-45deg, transparent 75%, #ccc 75%);
  background-size: 12px 12px;
  background-position: 0 0, 0 6px, 6px -6px, -6px 0px;
  border-radius: 8px;
  cursor: pointer;
  overflow: hidden;

  /* Estilos para a imagem */
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* Estilos para o ícone de adicionar */
  .add-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    font-size: 30px;
    color: $color-border-table;
  }
}

/* 
  Estilos para o slot principal
  Define a largura, altura, borda e sombra
*/
.main-slot {
  width: 310px;
  height: 310px;
  min-width: 220px;
  min-height: 220px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  flex-shrink: 0;

  /* Estilos para o hover */
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  }
}

/* 
  Estilos para o slot de miniatura
  Define a largura, altura, borda e sombra
*/
.thumb-slot {
  width: 150px;
  height: 145px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;

  /* Estilos para o hover */
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  }
}

/* Estilos para o input de arquivo */
.file-input {
  display: none;
}

/* 
  Estilos para a grade de miniaturas
  Define o layout flexível e o espaçamento entre as miniaturas
*/
.thumbnail-grid {
  display: flex;
  gap: 20px;
}

/* 
  Estilos para o flex de miniaturas
  Define o layout flexível e a direção da coluna
*/
.thumbnail-flex {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
