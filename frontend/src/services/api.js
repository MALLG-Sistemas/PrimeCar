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
  // Método para atualizar um carro pelo ID
  updateCarro(id, formData) {
    // Usando um cliente diferente para envio de arquivos (multipart/form-data)
    const formClient = axios.create({
      baseURL: "http://127.0.0.1:8000/api/v1",
      headers: {
        Accept: "application/json",
        "Content-Type": "multipart/form-data",
      },
    });
    return formClient.patch(`carros/${id}/`, formData);
  },

  // Método para excluir uma imagem específica de um carro
  deleteImagem(carroId, imagemId) {
    return apiClient.delete(`carros/${carroId}/delete_imagem/`, {
      data: { imagem_id: imagemId },
    });
  },

  // Método para reordenar as imagens de um carro
  reordenarImagens(carroId, imagens) {
    return apiClient.post(`carros/${carroId}/reordenar_imagens/`, {
      imagens: imagens,
    });
  },

  // Método para definir uma imagem como principal
  setImagemPrincipal(carroId, imagemId) {
    return apiClient.post(`carros/${carroId}/set_imagem_principal/`, {
      imagem_id: imagemId,
    });
  },
};
