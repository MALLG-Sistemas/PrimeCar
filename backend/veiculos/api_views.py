from rest_framework import viewsets, permissions, filters

# from django_filters.rest_framework import DjangoFilterBackend
from .models import Modelo, Carro
from .serializers import ModeloSerializer, CarroSerializer


class ModeloViewSet(
    viewsets.ModelViewSet
):  # ModelViewSet fornece os metodos list, create, retrieve, update, partial_update, destroy.
    queryset = Modelo.objects.all().order_by("nome_marca", "nome_modelo")
    serializer_class = ModeloSerializer
    # Futuramente aqui codificamos as permissions


class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all().select_related("modelo").order_by("-data_cadastro")
    serializer_class = CarroSerializer

    # Filtros e Buscas
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = [
        "cor",
        "ano_fabricacao",
        "modelo__nome_marca",
        "modelo__nome_modelo",
    ]  # Campos para filtro
    search_fields = [
        "cor",
        "descricao_carro",
        "modelo__nome_marca",
        "modelo__nome_modelo",
    ]  # Campos para busca
    ordering_fields = [
        "ano_fabricacao",
        "data_cadastro",
        "modelo__nome_marca",
        "modelo__nome_modelo",
    ]  # Campos que pode ordenar
    ordering = ["-data_cadastro"]  # Ordenação

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
