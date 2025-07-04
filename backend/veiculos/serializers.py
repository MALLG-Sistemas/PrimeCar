from rest_framework import serializers
from .models import Modelo, Carro, ImagemCarro


class ModeloSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Modelo.

    Converte instâncias de Modelo em representações JSON, incluindo os campos
    essenciais para identificação e descrição do modelo.
    """

    class Meta:
        model = Modelo
        fields = ["id", "nome_marca", "nome_modelo", "descricao_modelo", "ano_modelo"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.id:
            rep["id"] = (
                f"M{instance.id:04d}"  # Formata o ID de Modelo como M0001, M0002, etc.
            )
        return rep


class ImagemCarroSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo ImagemCarro.

    Converte instâncias de ImagemCarro em representações JSON, incluindo
    a URL absoluta da imagem.
    """

    url_imagem = serializers.SerializerMethodField()

    class Meta:
        model = ImagemCarro
        fields = ["id", "imagem", "url_imagem", "e_principal", "ordem"]
        read_only_fields = ("url_imagem",)

    def get_url_imagem(self, obj):
        request = self.context.get("request")
        if obj.imagem and hasattr(obj.imagem, "url"):
            return request.build_absolute_uri(obj.imagem.url)
        return None


class CarroSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Carro.

    Responsável por converter instâncias de Carro em JSON, incluindo os detalhes
    do modelo relacionado e a URL absoluta da imagem principal, quando disponível.
    Também gerencia as imagens adicionais do veículo.
    """

    modelo = ModeloSerializer(read_only=True)
    modelo_id = serializers.PrimaryKeyRelatedField(
        queryset=Modelo.objects.all(),
        source="modelo",
        write_only=True,
        allow_null=True,
        required=False,
    )

    # Para exibir a URL completa da imagem principal (compatibilidade com frontend)
    imagem_principal_url = serializers.SerializerMethodField()

    # Para gerenciar as imagens
    imagens = ImagemCarroSerializer(many=True, read_only=True)
    imagens_para_upload = serializers.ListField(
        child=serializers.ImageField(
            max_length=100000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Carro
        fields = [
            "id",
            "modelo",
            "modelo_id",
            "ano_fabricacao",
            "cor",
            "descricao_carro",
            "imagem_principal",
            "imagem_principal_url",
            "imagens",
            "imagens_para_upload",
            "data_cadastro",
        ]
        read_only_fields = (
            "data_cadastro",
            "imagem_principal_url",
            "imagens",
        )

    def get_imagem_principal_url(self, obj):
        """
        Obtém a URL da imagem principal do veículo para compatibilidade com frontend.
        Primeiro verifica se há uma imagem principal no modelo ImagemCarro,
        se não encontrar, usa o campo imagem_principal tradicional.
        """
        request = self.context.get("request")

        # Busca a imagem marcada como principal
        imagem_principal = obj.imagens.filter(e_principal=True).first()

        if imagem_principal and imagem_principal.imagem:
            return request.build_absolute_uri(imagem_principal.imagem.url)

        # Fallback para o campo imagem_principal original
        if obj.imagem_principal and hasattr(obj.imagem_principal, "url"):
            return request.build_absolute_uri(obj.imagem_principal.url)

        return None

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.id:
            rep["id"] = f"{instance.id:04d}"  # Formata o ID como 0001, 0002, etc.
        return rep

    def create(self, validated_data):
        imagens_data = validated_data.pop("imagens_para_upload", None)

        # Se tiver imagem_principal no request, move para imagens_data para processamento unificado
        imagem_principal = validated_data.pop("imagem_principal", None)

        # Cria o carro sem imagens ainda
        carro = super().create(validated_data)

        # Processa a imagem principal, se fornecida
        if imagem_principal:
            ImagemCarro.objects.create(
                carro=carro, imagem=imagem_principal, e_principal=True, ordem=0
            )

        # Processa imagens adicionais
        if imagens_data:
            for i, imagem in enumerate(imagens_data):
                # A primeira imagem será a principal apenas se não houver imagem principal
                e_principal = (
                    i == 0
                    and not imagem_principal
                    and not ImagemCarro.objects.filter(
                        carro=carro, e_principal=True
                    ).exists()
                )

                ImagemCarro.objects.create(
                    carro=carro, imagem=imagem, e_principal=e_principal, ordem=i + 1
                )

        return carro

    def update(self, instance, validated_data):
        imagens_data = validated_data.pop("imagens_para_upload", None)
        imagem_principal = validated_data.pop("imagem_principal", None)

        # Atualiza os campos básicos do carro
        carro = super().update(instance, validated_data)

        # Processa a imagem principal, se fornecida
        if imagem_principal:
            # Verifica se já existe uma imagem principal
            imagem_principal_existente = carro.imagens.filter(e_principal=True).first()

            if imagem_principal_existente:
                # Atualiza a imagem principal existente
                imagem_principal_existente.imagem = imagem_principal
                imagem_principal_existente.save()
            else:
                # Cria uma nova imagem principal
                ImagemCarro.objects.create(
                    carro=carro, imagem=imagem_principal, e_principal=True, ordem=0
                )

            # Para compatibilidade com o frontend, também atualiza o campo imagem_principal
            if instance.imagem_principal != imagem_principal:
                instance.imagem_principal = imagem_principal
                instance.save(update_fields=["imagem_principal"])

        # Processa imagens adicionais
        if imagens_data:
            # Obtém a próxima ordem disponível
            ultima_ordem = (
                carro.imagens.filter(e_principal=False)
                .order_by("-ordem")
                .values_list("ordem", flat=True)
                .first()
                or 0
            )

            # Verifica se já existe uma imagem principal antes de processar novas
            tem_imagem_principal = carro.imagens.filter(e_principal=True).exists()

            # Adiciona as novas imagens
            for i, imagem in enumerate(imagens_data):
                # Se não houver imagem principal e esta for a primeira, marca como principal
                e_principal = (
                    i == 0 and not tem_imagem_principal and not imagem_principal
                )

                # Se esta imagem for marcada como principal, desmarca outras que possam estar assim
                if e_principal:
                    ImagemCarro.objects.filter(carro=carro, e_principal=True).update(
                        e_principal=False
                    )

                ImagemCarro.objects.create(
                    carro=carro,
                    imagem=imagem,
                    e_principal=e_principal,
                    ordem=ultima_ordem + i + 1,
                )

        return carro
