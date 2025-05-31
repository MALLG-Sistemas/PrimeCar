<template>
  <button
    class="btn-custom"
    :class="buttonClass"
    :style="buttonStyle"
    @click="handleClick">
    <slot>Click Me</slot>
  </button>
</template>

<script setup>
import { computed } from "vue";

// Props que o componente aceitará
const props = defineProps({
  // Tamanho do botão
  size: {
    type: String,
    default: "medium",
  },
  // Cor de fundo do botão
  bgColor: {
    type: String,
    default: "#007bff", // Azul padrão
  },
  // Cor do texto do botão
  textColor: {
    type: String,
    default: "#ffffff", // Branco padrão
  },
});

// Função/Evento para lidar com o clique do botãos
const handleClick = () => {
  console.log("Button clicked!");
};

// const buttonText = ref("Click Me");
</script>

<style lang="scss" scoped>
.btn-custom {
  transition: background-color 0.3s ease;

  // Ajustar a cor do hover
  &:hover {
    background-color: darken(var(--bg-color), 10%);
  }
}
</style>
