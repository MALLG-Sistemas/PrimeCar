<template>
  <button
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
    default: "#3d5e73",
  },
  // Cor do texto do botão
  textColor: {
    type: String,
    default: "#ffffff",
  },
});

// Computed para definir a classe do botão
const buttonClass = computed(() => ({
  "btn-custom": true,
}));

// Define os tamanhos do botão
const sizeStyles = {
  small: { width: "90px" },
  medium: { width: "113px" },
  large: { width: "124px" },
};

// Computed para definir os estilos inline do botão
const buttonStyle = computed(() => ({
  backgroundColor: props.bgColor,
  color: props.textColor,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  height: "37px",
  border: "none",
  borderRadius: "6px",
  cursor: "pointer",
  ...(sizeStyles[props.size] || sizeStyles.medium), // fallback para "medium"
}));

// Função/Evento para lidar com o clique do botãos
const handleClick = () => {
  console.log("Button clicked!");
};
</script>

<style lang="scss" scoped>
@use "sass:color";
@use "../styles/variables" as *;

.btn-custom {
  transition: background-color 0.3s ease;

  // Ajustar a cor do hover
  &:hover {
    background-color: color.adjust($color-button-primary, $lightness: -10%);
  }
}
</style>
