from django.contrib import admin
from django.utils.html import mark_safe
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
    list_display = (
        "__str__",
        "modelo",
        "ano_fabricacao",
        "cor",
        "data_cadastro",
        "image_preview_list",
    )
    list_filter = ("modelo__nome_marca", "modelo__nome_modelo", "ano_fabricacao", "cor")
    search_fields = (
        "modelo__nome_marca",
        "modelo__nome_modelo",
        "cor",
        "descricao_carro",
    )
    readonly_fields = ("data_cadastro", "image_preview_form")

    # Controle explícito dos campos e sua ordem no formulário do admin
    fields = (
        "modelo",
        "ano_fabricacao",
        "cor",
        "descricao_carro",
        "imagem_principal",  # Campo para upload
        "image_preview_form",  # Preview da imagem
        "data_cadastro",
    )

    def image_preview_list(self, carro: Carro):  # Tipo opcional adicionado
        """
        Exibe uma miniatura da imagem principal na lista de carros do admin.

        Args:
            carro (Carro): Instância do modelo Carro contendo a imagem principal a ser exibida.

        Returns:
            str: Um trecho de HTML seguro que exibe uma imagem em miniatura se a imagem principal existir e possuir uma URL; caso contrário, retorna uma string indicando que não há imagem.
        """
        if carro.imagem_principal and hasattr(carro.imagem_principal, "url"):
            return mark_safe(
                f'<img src="{carro.imagem_principal.url}" width="100" alt="Preview de {carro}" />'
            )
        return "(Sem imagem)"

    image_preview_list.short_description = "Imagem (Lista)"

    def image_preview_form(self, carro: Carro):  # Tipo opcional adicionado
        """
        Exibe um preview da imagem principal do carro no formulário de edição.

        Verifica se o objeto 'carro' possui uma imagem principal válida com o atributo 'url'.
        Se a imagem estiver disponível, retorna um fragmento HTML seguro contendo a imagem com
        estilos CSS para exibição (largura definida e margem superior). Caso contrário, retorna
        uma mensagem indicando que nenhuma imagem principal foi selecionada.

        Parâmetros:
            carro (Carro): Instância de Carro que possui um atributo 'imagem_principal' a ser verificado.

        Retorna:
            str: Código HTML seguro para visualização da imagem ou uma mensagem de aviso.
        """
        if carro.imagem_principal and hasattr(carro.imagem_principal, "url"):
            return mark_safe(
                f'<img src="{carro.imagem_principal.url}" width="200" '
                f'style="margin-top: 10px; display: block;" alt="Preview de {carro}" />'
            )
        return "Nenhuma imagem principal selecionada."

    image_preview_form.short_description = "Preview (Formulário)"
