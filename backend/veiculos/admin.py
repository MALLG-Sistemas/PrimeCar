from django.contrib import admin
from .models import Modelo, Carro


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = (
        "nome_marca",
        "nome_modelo",
        "ano_modelo",
    )
    list_filter = ("nome_marca", "ano_modelo")
    search_fields = ("nome_marca", "nome_modelo", "descricao_modelo")


@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ("__str__", "modelo", "ano_fabricacao", "cor", "data_cadastro")
    list_filter = ("modelo__nome_marca", "modelo__nome_modelo", "ano_fabricacao", "cor")
    search_fields = (
        "modelo__nome_marca",
        "modelo__nome_modelo",
        "cor",
        "descricao_carro",
    )
