from django.contrib import admin
from .models import Produto, Categoria ,Usuario,ImagemProduto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'categoria', 'preco', 'estoque', 'ativo')
    list_filter = ('categoria', 'marca', 'ativo')
    search_fields = ('nome', 'marca', 'descricao', 'sku')
    prepopulated_fields = {'slug': ('nome',)}  # gera o slug automaticamente no admin
    ordering = ('nome',)
    list_editable = ('ativo',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome','senha','CPF','data_nascimento','telefone','genero','email','tipo_usuario','imagem_usuario')
@admin.register(ImagemProduto)
class ImagemProdutoAdmin(admin.ModelAdmin):
    list_display=('produto','imagem')
