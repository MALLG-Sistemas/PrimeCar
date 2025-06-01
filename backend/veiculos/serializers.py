from rest_framework import serializers
from .models import Modelo, Carro


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
                f"CAR{instance.id:03d}"  # Formata o ID como CAR001, CAR002, etc.
            )
        return rep


class CarroSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo Carro.

    Responsável por converter instâncias de Carro em JSON, incluindo os detalhes
    do modelo relacionado e a URL absoluta da imagem principal, quando disponível
    Faz a conversão para JSON para poder enviar os dados.
    """

    modelo = ModeloSerializer(read_only=True)
    modelo_id = serializers.PrimaryKeyRelatedField(
        queryset=Modelo.objects.all(),
        source="modelo",
        write_only=True,
        allow_null=True,
        required=False,
    )
    # Para exibir a URL completa da imagem
    imagem_principal_url = serializers.SerializerMethodField()

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
            "data_cadastro",
        ]
        read_only_fields = (
            "data_cadastro",
            "imagem_principal_url",
        )  # Campos que não serão escritos pela API

    # Função para obter a URL completa da imagem
    def get_imagem_principal_url(self, obj):
        request = self.context.get("request")
        if obj.imagem_principal and hasattr(obj.imagem_principal, "url"):
            return request.build_absolute_uri(obj.imagem_principal.url)
        return None

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
