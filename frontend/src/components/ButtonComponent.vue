<template>
  <button
    class="btn btn-primary"
    @click="handleClick">
  </button>
</template>

<script setup>
// import { ref } from "vue";

const handleClick = () => {
  console.log("Button clicked!");
};

// const buttonText = ref("Click Me");
</script>

<style lang="scss" scoped>
.btn-primary {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}
</style>
