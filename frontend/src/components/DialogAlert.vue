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
          class="dialog-button dialog-button--cancel"
          size="large"
          bgColor="#878787"
          textColor="#FFFFFF"
          fontSize="14px"
          @click="handleCancel">
          Cancelar
        </ButtonComponent>

        <ButtonComponent
          class="dialog-button dialog-button--confirm"
          size="large"
          bgColor="#f00"
          textColor="#FFFFFF"
          fontSize="14px"
          @click="handleConfirm">
          Excluir
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.dialog-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 100%;
  max-width: 400px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dialog-header {
  display: inline-flex;
  padding: 10px 20px;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;

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
  padding: 5px 20px 15px;

  .dialog-message {
    margin: 0;
    font-size: 16px;
    color: $color-text-secondary;
    text-align: center;
  }
}

.dialog-actions {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  padding: 0 20px;

  .dialog-button {
    flex: 1;
  }
}
</style>
