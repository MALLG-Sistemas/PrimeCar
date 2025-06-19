# PrimeCar - Sistema de Gerenciamento de Veículos 🚗

## Curso: Análise e Desenvolvimento de Sistemas (ADS) - Disciplina Hands On Work VI – Faculdade Univali 🎓

O PrimeCar é um sistema completo de gerenciamento de veículos desenvolvido pela MALLG Sistemas como projeto acadêmico. O sistema permite o cadastro, visualização, edição e exclusão de veículos e seus modelos.

### Estrutura do Projeto/Sistema

O repositório está organizado em duas partes principais:

```
PrimeCar/
├── backend/      # API REST desenvolvida em Django
└── frontend/     # Interface de usuário desenvolvida em Vue.js
```

### Backend

O backend é uma API REST desenvolvida em Django e Django REST Framework que gerencia os dados do sistema:

- CRUD completo para modelos de veículos
- CRUD completo para veículos específicos
- Upload e gerenciamento de imagens
- Conexão com banco de dados MySQL
- Endpoints RESTful para comunicação com o frontend

### Frontend

O frontend é uma aplicação SPA (Single Page Application) desenvolvida em Vue.js que oferece uma interface intuitiva para:

- Dashboard de visualização de veículos
- Formulários para adição/edição de veículos e modelos
- Visualização detalhada de veículos com suporte a imagens
- Interface responsiva e moderna
- Conexão eficiente com a API do backend

### Como Executar o Projeto

#### Pré-requisitos

- Python 3.8+
- Node.js 16+
- MySQL
- pip e virtualenv
- npm ou yarn

#### Configuração do Backend

1. Navegue até a pasta do backend:
   ```
   cd backend
   ```
2. Crie um ambiente virtual e ative-o:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Configure o arquivo `.env` com as credenciais do banco de dados
5. Execute as migrações:
   ```
   python manage.py migrate
   ```
6. Inicie o servidor:
   ```
   python manage.py runserver
   ```

#### Configuração do Frontend

1. Navegue até a pasta do frontend:
   ```
   cd frontend
   ```
2. Instale as dependências:
   ```
   npm install  # ou yarn
   ```
3. Inicie o servidor de desenvolvimento:
   ```
   npm run dev  # ou yarn dev
   ```
4. Acesse a aplicação em `http://localhost:5173`

### Tecnologias Utilizadas

- **Backend**: Python, Django, Django REST Framework, MySQL
- **Frontend**: Vue.js, Vue Router, Axios, SCSS
- **Ferramentas**: Git, VSCode, Vite

### Autores

- André Vicente Guesser – [LinkedIn](https://www.linkedin.com/in/andr%C3%A9-guesser-184823356/)
- Guilherme Veloso de Oliveira – [LinkedIn](https://www.linkedin.com/in/guilherme-veloso-de-oliveira-6a6b72260/)
- Mauricio Macedo da Silva – [LinkedIn](https://www.linkedin.com/in/mauricio-macedo-22570085/)
- Lucas Elias Dickmann – [LinkedIn](https://linkedin.com/in/lucas-dickmann)
- Lucas Sagaz da Silva – [LinkedIn](https://www.linkedin.com/in/lucas-sagaz-da-silva-6a41b3230/)

---

© 2025 MALLG Sistemas - Todos os direitos reservados
