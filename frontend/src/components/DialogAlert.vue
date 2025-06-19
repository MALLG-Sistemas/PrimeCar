<template>
  <div
    v-if="isVisible"
    class="dialog-overlay"
    @click.self="closeOnBackdrop && handleCancel()">
    <div class="dialog-container">
      <div class="dialog-header">
        <span class="material-symbols-outlined dialog-icon">warning</span>
        <h3 class="dialog-title">AVISO</h3>
      </div>

      <div class="dialog-content">
        <p class="dialog-message">
          {{ message || "Você deseja excluir este registro?" }}
        </p>
      </div>

      <div class="dialog-actions">
        <ButtonComponent
          class="dialog-button dialog-button--confirm"
          size="medium"
          bgColor="#f00"
          textColor="#FFFFFF"
          fontSize="14px"
          @click="handleConfirm">
          Excluir
        </ButtonComponent>
        <ButtonComponent
          class="dialog-button dialog-button--cancel"
          size="medium"
          bgColor="#3d5e73"
          textColor="#FFFFFF"
          fontSize="14px"
          @click="handleCancel">
          Cancelar
        </ButtonComponent>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import ButtonComponent from "./ButtonComponent.vue";

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false,
  },
  message: {
    type: String,
    default: "Você deseja excluir este registro?",
  },
  closeOnBackdrop: {
    type: Boolean,
    default: true,
  },
});

const emit = defineEmits(["confirm", "cancel", "close"]);

const handleConfirm = () => {
  emit("confirm");
  emit("close");
};

const handleCancel = () => {
  emit("cancel");
  emit("close");
};
</script>

<style lang="scss" scoped>
@use "../styles/variables" as *;

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.dialog-container {
  background-color: $color-bg-dialog-alert;
  display: flex;
  width: 100%;
  max-width: 292px;
  height: 100%;
  max-height: 146px;
  padding: 10px 20px;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  aspect-ratio: 291.02/146;
  border-radius: 8px;
}

.dialog-header {
  display: inline-flex;
  justify-content: center;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid $color-dark-bg;
  padding-bottom: 8px;
  width: 100%;

  .dialog-icon {
    color: #f00;
    font-size: 24px;
  }

  .dialog-title {
    margin: 0;
    font-family: $font-primary;
    font-size: 18px;
    font-weight: 600;
    color: $color-text-secondary;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
}

.dialog-content {
  .dialog-message {
    margin: 0;
    font-size: 14px;
    font-weight: 500;
    color: $color-text-secondary;
    text-align: center;
    line-height: 15px;
  }
}

.dialog-actions {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  padding: 0 0;

  .dialog-button {
    flex: 1;
  }
}
</style>
