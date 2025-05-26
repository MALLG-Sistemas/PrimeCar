from django.db import models
import os  # Importação o módulo os para manipulação das imagens


# Entidade de Modelos
class Modelo(models.Model):
    nome_marca = models.CharField(max_length=100, verbose_name="Nome da Marca")
    nome_modelo = models.CharField(max_length=100, verbose_name="Nome do Modelo")
    descricao_modelo = models.TextField(
        blank=True, null=True, verbose_name="Descrição do Modelo"
    )
    ano_modelo = models.PositiveIntegerField(verbose_name="Ano do Modelo do Veículo")

    class Meta:
        verbose_name = "Modelo de Veículo"
        verbose_name_plural = "Modelos de Veículos"
        unique_together = ("nome_marca", "nome_modelo", "ano_modelo")
        ordering = ["nome_marca", "nome_modelo"]

    def __str__(self):
        return f"{self.nome_marca} {self.nome_modelo} ({self.ano_modelo})"


# Função para definir o caminho de upload da imagem do carro
def get_upload_path_imagem_carro(instance, filename):
    # O arquivo será enviado para MEDIA_ROOT/imagens_carros/<id_do_carro>/<filename>
    # Garante que o carro tenha um ID antes de tentar usá-lo no caminho
    carro_id_path = instance.id if instance.id else "temp_carro_id"
    return os.path.join("imagens_carros", str(carro_id_path), filename)


# Entidade de Carros
class Carro(models.Model):
    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.PROTECT,
        related_name="carros_especificos",
        verbose_name="Modelo Específico do Veículo",
    )  # Relacionamento com Modelo e 'PROTECT' para evitar exclusão de modelos associados

    data_cadastro = models.DateTimeField(
        auto_now_add=True, verbose_name="Data de Cadastro"
    )
    ano_fabricacao = models.PositiveIntegerField(verbose_name="Ano de Fabricação")
    cor = models.CharField(max_length=50, verbose_name="Cor do Veículo")
    descricao_carro = models.TextField(
        blank=True, null=True, verbose_name="Descrição do Carro/Modelo"
    )

    # Campo para armazenar a imagem do carro
    imagem_principal = models.ImageField(
        upload_to=get_upload_path_imagem_carro,
        verbose_name="Imagem Principal do Veículo",
        null=True,  # Permite que o carro seja cadastrado sem imagem inicialmente
        blank=True,  # Permite que o campo seja opcional no formulário do admin
    )

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ["-data_cadastro"]

    def __str__(self):
        modelo_str = str(self.modelo) if self.modelo else "Modelo Desconhecido"
        return f"{self.modelo} - {self.cor} - ({self.ano_fabricacao})"
