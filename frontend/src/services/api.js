/* Módulo de serviços de API para comunicação com o backend
 *
 * Comunicação com a API através de metodos HTTP
 */
import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1",
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export default {
  getCarros() {
    return apiClient.get("/veiculos/carros/");
  },
  getCarro(id) {
    return apiClient.get(`/veiculos/carros/${id}/`);
  },

  // Adicionar outros metodos conforme necessário
};
