import { createApp } from "vue";
import App from "./App.vue";
import "./styles/main.scss"; // Importação do arquivo de estilos principal
import router from "./router"; // Importação de router que gerencia as rotas da aplicação

const app = createApp(App);

app.use(router); // Configuração do router na aplicação Vue

app.mount("#app"); // Montagem da aplicação Vue no elemento com id "app"
