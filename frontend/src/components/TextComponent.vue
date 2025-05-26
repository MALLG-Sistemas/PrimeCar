<template>
  <p :class="textClass">
    {{ text }}
  </p>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    required: true,
  },
  textClass: {
    type: String,
    default: "text-default",
  },
});
</script>
