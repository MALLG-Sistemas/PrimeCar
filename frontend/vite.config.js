import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [
    vue({
      // Usando apenas a configuração nativa do Vue 3
      inspector: {
        enabled: true,
      },
    }),
  ],
});