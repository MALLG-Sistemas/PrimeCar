# MALLG Sistemas – Backend do PrimeCar 🚗

## Curso: Análise e Desenvolvimento de Sistemas (ADS) - Disciplina Hands On Work VI – Faculdade Univali 🎓

### Descrição do Projeto

Este repositório contém o backend em Django para o sistema de gerenciamento de veículos da MALLG Sistemas. A API oferece:

- CRUD de `Modelos` de veículos.
- CRUD de `Carros`, com upload de imagem principal e preview no Django Admin.
- Persistência de dados em banco MySQL.
- Configuração para servir arquivos de mídia via `MEDIA_URL`.

### Funcionalidades Principais

- Registro de marcas e modelos de veículos ([`veiculos.models.Modelo`](veiculos/models.py)).
- Cadastro de veículos específicos ([`veiculos.models.Carro`](veiculos/models.py)), incluindo ano, cor, descrição e imagem.
- Interface de administração customizada com previews em lista e formulário ([`veiculos.admin.CarroAdmin`](veiculos/admin.py)).
- Endpoints REST em desenvolvimento com Django REST Framework.

### Tecnologias Utilizadas

- Python 3.x
- Django 5.2.1
- Django REST Framework 3.16.0
- MySQL
- Pillow
- python-dotenv

### Pré-requisitos

- Python 3.8+
- MySQL
- `pip` e `virtualenv`

### Estrutura de Pastas

```
backend/
├── core/                # Configurações do projeto Django (urls, settings, wsgi, asgi)
├── veiculos/            # App de veículos (models, admin, views, tests, migrations)
├── media/               # Upload de imagens
└── requirements.txt
```

### Autores

- André Vicente Guesser – https://www.linkedin.com/in/andr%C3%A9-guesser-184823356/
- Guilherme Veloso de Oliveira – https://www.linkedin.com/in/guilherme-veloso-de-oliveira-6a6b72260/
- Lucas Sagaz da Silva – https://www.linkedin.com/in/lucas-sagaz-da-silva-6a41b3230/
- Mauricio Macedo da Silva – https://www.linkedin.com/in/mauricio-macedo-22570085/
- Lucas Elias Dickmann – https://linkedin.com/in/lucas-dickmann
