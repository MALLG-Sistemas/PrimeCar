from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ModeloViewSet, CarroViewSet

"""
Módulo: api_urls
----------------
Este módulo configura o roteamento de URL para a aplicação backend 'veiculos'
usando o DefaultRouter do Django REST Framework. Ele registra dois viewsets com o roteador:
1. ModeloViewSet, acessível no endpoint 'modelos'.
2. CarroViewSet, acessível no endpoint 'carros'.
O DefaultRouter gera automaticamente o conjunto padrão de rotas CRUD para ambos
os endpoints, que são então incluídos na configuração geral de URL da aplicação.
Uso:
Inclua os urlpatterns deste módulo na configuração de URL do seu projeto para habilitar
os endpoints da API RESTful para os modelos de veículos e carros.
"""
router = DefaultRouter()
router.register(r"modelos", ModeloViewSet, basename="modelo")
router.register(r"carros", CarroViewSet, basename="carro")

urlpatterns = [
    path("", include(router.urls)),
]
