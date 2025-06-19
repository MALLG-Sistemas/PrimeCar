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
  // Método para buscar todos os carros do endpoint /veiculos/carros/
  getCarros() {
    return apiClient.get("carros/");
  },
  // Método para buscar um carro específico pelo ID do endpoint /veiculos/carros/{id}/
  getCarro(id) {
    return apiClient.get(`carros/${id}/`);
  },
  // Método para excluir um carro pelo ID
  deleteCarro(id) {
    return apiClient.delete(`carros/${id}/`);
  },

  // Adicionar outros metodos conforme necessário
};
