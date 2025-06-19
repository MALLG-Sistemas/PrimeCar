# MALLG Sistemas – Backend do PrimeCar 🚗

## Curso: Análise e Desenvolvimento de Sistemas (ADS) - Disciplina Hands On Work VI – Faculdade Univali 🎓

### Descrição do Projeto

Este é o backend da aplicação PrimeCar, uma API RESTful desenvolvida com Django e Django REST Framework. Ele é responsável por toda a lógica de negócios, gerenciamento de dados e comunicação com o banco de dados MySQL.

- CRUD de `Modelos` de veículos.
- CRUD de `Carros`, com upload de imagem principal e preview no Django Admin.
- Persistência de dados em banco MySQL.
- Configuração para servir arquivos de mídia via `MEDIA_URL`.

### Funcionalidades Principais

- **CRUD de Modelos**: Gerenciamento completo de marcas e modelos de veículos.
- **CRUD de Carros**: Gerenciamento de veículos, incluindo detalhes como ano, cor e descrição.
- **Gerenciamento de Imagens**: Suporte para upload de múltiplas imagens por veículo, com a capacidade de definir uma imagem como principal.
- **API RESTful**: Endpoints para integração com o frontend ou outros clientes.
- **Admin Customizado**: Interface de administração do Django aprimorada para facilitar a gestão dos dados, com pré-visualização de imagens.

### Tecnologias Utilizadas

- Python 3.x
- Django 5.2.3
- Django REST Framework 3.16.0
- MySQL
- Pillow 11.2.1
- python-dotenv

### Endpoints da API

A URL base da API é `/api/v1/`.

#### Modelos (`/modelos/`)

- `GET /api/v1/modelos/`: Lista todos os modelos.
- `POST /api/v1/modelos/`: Cria um novo modelo.
- `GET /api/v1/modelos/{id}/`: Retorna os detalhes de um modelo específico.
- `PUT /api/v1/modelos/{id}/`: Atualiza um modelo.
- `DELETE /api/v1/modelos/{id}/`: Deleta um modelo.

#### Carros (`/carros/`)

- `GET /api/v1/carros/`: Lista todos os carros.
- `POST /api/v1/carros/`: Cria um novo carro (suporta upload de imagens).
- `GET /api/v1/carros/{id}/`: Retorna os detalhes de um carro específico.
- `PATCH /api/v1/carros/{id}/`: Atualiza parcialmente um carro (suporta upload de imagens).
- `DELETE /api/v1/carros/{id}/`: Deleta um carro.

#### Ações customizadas de Carros:

- `DELETE /api/v1/carros/{id}/delete_imagem/`: Deleta uma imagem específica de um carro.
  - **Body**: `{ "imagem_id": <id_da_imagem> }`
- `POST /api/v1/carros/{id}/set_imagem_principal/`: Define uma imagem como a principal do carro.
  - **Body**: `{ "imagem_id": <id_da_imagem> }`

### Autores

- André Vicente Guesser – [LinkedIn](https://www.linkedin.com/in/andr%C3%A9-guesser-184823356/)
- Guilherme Veloso de Oliveira – [LinkedIn](https://www.linkedin.com/in/guilherme-veloso-de-oliveira-6a6b72260/)
- Mauricio Macedo da Silva – [LinkedIn](https://www.linkedin.com/in/mauricio-macedo-22570085/)
- Lucas Elias Dickmann – [LinkedIn](https://linkedin.com/in/lucas-dickmann)
- Lucas Sagaz da Silva – [LinkedIn](https://www.linkedin.com/in/lucas-sagaz-da-silva-6a41b3230/)

---

© 2025 MALLG Sistemas - Todos os direitos reservados
