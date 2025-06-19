from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# from django_filters.rest_framework import DjangoFilterBackend
from .models import Modelo, Carro, ImagemCarro
from .serializers import ModeloSerializer, CarroSerializer, ImagemCarroSerializer


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

    @action(detail=True, methods=["delete"])
    def delete_imagem(self, request, pk=None):
        """
        Deleta uma imagem específica do veículo.

        Args:
            request: Objeto de requisição com o ID da imagem
            pk: ID do veículo

        Returns:
            Response confirmando a exclusão ou erro
        """
        carro = self.get_object()

        try:
            imagem_id = request.data.get("imagem_id") or request.query_params.get(
                "imagem_id"
            )
            if not imagem_id:
                return Response(
                    {"detail": "É necessário fornecer um ID de imagem."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            imagem = get_object_or_404(ImagemCarro, id=imagem_id, carro=carro)

            # Se a imagem a ser excluída for a principal, atualiza o campo imagem_principal do carro
            if imagem.e_principal and carro.imagem_principal:
                carro.imagem_principal = None
                carro.save(update_fields=["imagem_principal"])

            imagem.delete()
            return Response({"detail": "Imagem excluída com sucesso."})

        except Exception as e:
            return Response(
                {"detail": f"Erro ao excluir imagem: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def reordenar_imagens(self, request, pk=None):
        """
        Reordena as imagens de um veículo.

        Args:
            request: Objeto de requisição com a lista de IDs e ordens
            pk: ID do veículo

        Returns:
            Response confirmando a reordenação ou erro
        """
        carro = self.get_object()

        try:
            imagens_ordem = request.data.get("imagens", [])

            if not imagens_ordem or not isinstance(imagens_ordem, list):
                return Response(
                    {
                        "detail": "É necessário fornecer uma lista de imagens e suas ordens."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Atualizar a ordem de cada imagem
            for item in imagens_ordem:
                imagem_id = item.get("id")
                nova_ordem = item.get("ordem")

                if imagem_id is not None and nova_ordem is not None:
                    ImagemCarro.objects.filter(id=imagem_id, carro=carro).update(
                        ordem=nova_ordem
                    )

            return Response({"detail": "Imagens reordenadas com sucesso."})

        except Exception as e:
            return Response(
                {"detail": f"Erro ao reordenar imagens: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["post"])
    def set_imagem_principal(self, request, pk=None):
        """
        Define uma imagem específica como principal.

        Args:
            request: Objeto de requisição com o ID da imagem
            pk: ID do veículo

        Returns:
            Response confirmando a alteração ou erro
        """
        carro = self.get_object()

        try:
            imagem_id = request.data.get("imagem_id")
            if not imagem_id:
                return Response(
                    {"detail": "É necessário fornecer um ID de imagem."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Busca a imagem que será definida como principal
            nova_imagem_principal = get_object_or_404(
                ImagemCarro, id=imagem_id, carro=carro
            )

            # Importante: primeiro remova o status de principal das outras imagens,
            # Não exlue
            ImagemCarro.objects.filter(carro=carro, e_principal=True).update(
                e_principal=False
            )

            # Define a nova imagem como principal
            nova_imagem_principal.e_principal = True
            nova_imagem_principal.save()

            # Atualiza o campo imagem_principal do carro para manter compatibilidade
            carro.imagem_principal = nova_imagem_principal.imagem
            carro.save(update_fields=["imagem_principal"])

            return Response(
                {
                    "detail": "Imagem principal definida com sucesso.",
                    "imagem_principal_url": (
                        request.build_absolute_uri(nova_imagem_principal.imagem.url)
                        if nova_imagem_principal.imagem
                        else None
                    ),
                }
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro ao definir imagem principal: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
