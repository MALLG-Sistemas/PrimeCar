from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ModeloViewSet, CarroViewSet

router = DefaultRouter()
router.register(r"modelos", ModeloViewSet, basename="modelo")
router.register(r"carros", CarroViewSet, basename="carro")

urlpatterns = [
    path("", include(router.urls)),
]
