from django.contrib import admin
from django.utils.html import mark_safe
from .models import Modelo, Carro, ImagemCarro


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = (
        "nome_marca",
        "nome_modelo",
        "ano_modelo",
    )
    list_filter = ("nome_marca", "ano_modelo")
    search_fields = ("nome_marca", "nome_modelo", "descricao_modelo")


class ImagemCarroInline(admin.TabularInline):
    """
    Inline admin para imagens de veículos.
    Permite adicionar, editar e remover imagens diretamente
    no formulário de edição do veículo.
    """

    model = ImagemCarro
    extra = 1  # Número de formulários vazios
    fields = ("imagem", "e_principal", "ordem", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        """
        Exibe uma prévia da imagem no admin.

        Args:
            obj: Instância do modelo ImagemCarro

        Returns:
            str: HTML seguro mostrando uma prévia da imagem
        """
        if obj.imagem and hasattr(obj.imagem, "url"):
            return mark_safe(
                f'<img src="{obj.imagem.url}" width="100" alt="Preview" />'
            )
        return "(Sem imagem)"

    image_preview.short_description = "Preview"


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
    inlines = [ImagemCarroInline]

    # Controle explícito dos campos e sua ordem no formulário do admin
    fields = (
        "modelo",
        "ano_fabricacao",
        "cor",
        "descricao_carro",
        "imagem_principal",  # Mantido para compatibilidade
        "image_preview_form",  # Preview da imagem principal
        "data_cadastro",
    )

    def image_preview_list(self, carro: Carro):
        """
        Exibe uma miniatura da imagem principal na lista de carros do admin.
        """
        # Primeiro tenta buscar a imagem marcada como principal no novo modelo
        imagem_principal = carro.imagens.filter(e_principal=True).first()

        if (
            imagem_principal
            and imagem_principal.imagem
            and hasattr(imagem_principal.imagem, "url")
        ):
            return mark_safe(
                f'<img src="{imagem_principal.imagem.url}" width="100" alt="Preview de {carro}" />'
            )

        # Fallback para o campo antigo
        if carro.imagem_principal and hasattr(carro.imagem_principal, "url"):
            return mark_safe(
                f'<img src="{carro.imagem_principal.url}" width="100" alt="Preview de {carro}" />'
            )

        return "(Sem imagem)"

    image_preview_list.short_description = "Imagem (Lista)"

    def image_preview_form(self, carro: Carro):
        """
        Exibe um preview da imagem principal do carro no formulário de edição.
        """
        # Primeiro tenta buscar a imagem marcada como principal no novo modelo
        imagem_principal = carro.imagens.filter(e_principal=True).first()

        if (
            imagem_principal
            and imagem_principal.imagem
            and hasattr(imagem_principal.imagem, "url")
        ):
            return mark_safe(
                f'<img src="{imagem_principal.imagem.url}" width="200" '
                f'style="margin-top: 10px; display: block;" alt="Preview de {carro}" />'
            )

        # Fallback para o campo antigo
        if carro.imagem_principal and hasattr(carro.imagem_principal, "url"):
            return mark_safe(
                f'<img src="{carro.imagem_principal.url}" width="200" '
                f'style="margin-top: 10px; display: block;" alt="Preview de {carro}" />'
            )

        return "Nenhuma imagem principal selecionada."

    image_preview_form.short_description = "Preview (Formulário)"

    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método save_model para garantir sincronização entre
        imagem_principal e ImagemCarro.
        """
        super().save_model(request, obj, form, change)

        # Se o campo imagem_principal foi preenchido/alterado
        if "imagem_principal" in form.changed_data and obj.imagem_principal:
            # Verifica se já existe uma imagem principal
            imagem_principal_existente = obj.imagens.filter(e_principal=True).first()

            if imagem_principal_existente:
                # Atualiza a imagem principal existente
                imagem_principal_existente.imagem = obj.imagem_principal
                imagem_principal_existente.save()
            else:
                # Cria uma nova imagem principal
                ImagemCarro.objects.create(
                    carro=obj, imagem=obj.imagem_principal, e_principal=True, ordem=0
                )


@admin.register(ImagemCarro)
class ImagemCarroAdmin(admin.ModelAdmin):
    """
    Admin para o modelo ImagemCarro.
    Permite gerenciar todas as imagens de forma independente.
    """

    list_display = (
        "carro",
        "e_principal",
        "ordem",
        "data_upload",
        "image_preview_list",
    )
    list_filter = (
        "e_principal",
        "carro__modelo__nome_marca",
        "carro__modelo__nome_modelo",
    )
    search_fields = ("carro__modelo__nome_marca", "carro__modelo__nome_modelo")
    list_editable = ("e_principal", "ordem")

    def image_preview_list(self, obj):
        if obj.imagem and hasattr(obj.imagem, "url"):
            return mark_safe(
                f'<img src="{obj.imagem.url}" width="100" alt="Preview" />'
            )
        return "(Sem imagem)"

    image_preview_list.short_description = "Preview"

    def save_model(self, request, obj, form, change):
        """
        Sobrescreve o método save_model para garantir que apenas
        uma imagem seja marcada como principal para cada carro.
        """
        # Se esta imagem está sendo marcada como principal
        if "e_principal" in form.changed_data and obj.e_principal:
            # Desmarca todas as outras imagens do mesmo carro
            ImagemCarro.objects.filter(carro=obj.carro, e_principal=True).exclude(
                pk=obj.pk
            ).update(e_principal=False)

            # Atualiza também o campo imagem_principal do carro para manter compatibilidade
            obj.carro.imagem_principal = obj.imagem
            obj.carro.save(update_fields=["imagem_principal"])

        super().save_model(request, obj, form, change)
