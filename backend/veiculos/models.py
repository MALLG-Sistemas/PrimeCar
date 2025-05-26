from django.db import models


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

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ["-data_cadastro"]

    def __str__(self):
        return f"{self.modelo} - {self.cor} - ({self.ano_fabricacao})"
