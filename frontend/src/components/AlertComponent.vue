<template>
  <transition name="fade">
    <div
      v-if="isVisible"
      :class="['alert', `alert--${type}`]">
      <span class="alert__message">{{ message }}</span>
    </div>
  </transition>
</template>

<script setup>
import { defineProps, defineEmits, watch, onBeforeUnmount } from "vue";

const props = defineProps({
  isVisible: { type: Boolean, default: false },
  message: { type: String, required: true },
  type: { type: String, default: "info" }, // success|error|warning|info
});
const emit = defineEmits(["close"]);
let timeoutId = null;

watch(
  () => props.isVisible,
  (visible) => {
    if (visible) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => emit("close"), 3000);
    }
  }
);

onBeforeUnmount(() => clearTimeout(timeoutId));
</script>

<style lang="scss" scoped>
@use "../styles/variables" as vars;

.alert {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  display: flex;
  align-items: center;
  min-width: 240px;
  padding: 12px 16px;
  border-radius: 4px;
  color: vars.$color-light-text;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 10000;

  &__message {
    flex: 1;
    font-size: 0.875rem;
  }

  // gera .alert--success, .alert--error, .alert--warning, .alert--info
  @each $state, $color in vars.$alert-colors {
    &--#{$state} {
      background-color: $color;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
