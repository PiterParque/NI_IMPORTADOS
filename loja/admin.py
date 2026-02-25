from django.contrib import admin
from .models import Produto, Categoria ,Usuario,ImagemProduto,Endereco,Pedido,ItemPedido

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'categoria', 'preco', 'estoque', 'ativo')
    list_filter = ('categoria', 'marca', 'ativo')
    search_fields = ('nome', 'marca', 'descricao', 'sku')
    prepopulated_fields = {'slug': ('nome',)}  # gera o slug automaticamente no admin
    ordering = ('nome',)
    list_editable = ('ativo',)
     
    def has_add_permission(self, request):
        return request.user.has_perm('loja.add_produto')

    def has_change_permission(self, request, obj=None):
        return request.user.has_perm('loja.change_produto')

    def has_delete_permission(self, request, obj=None):
        return request.user.has_perm('loja.delete_produto')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome','CPF','data_nascimento','telefone','genero','email','tipo_usuario','imagem_usuario')
@admin.register(ImagemProduto)
class ImagemProdutoAdmin(admin.ModelAdmin):
    list_display=('produto','imagem')
@admin.register(Endereco)
class ImagemProdutoAdmin(admin.ModelAdmin):
    list_display=('user','endereco','cep')
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0  # não mostra linhas vazias extras

@admin.register(Pedido)
class PedidosAdmin(admin.ModelAdmin):
    list_display = (
        'numero_pedido',
        'cliente',
        'listar_itens',
        'data_pedido',
        'status',
        'valor_total'
    )

    list_filter = ('status', 'data_pedido')
    search_fields = ('numero_pedido', 'cliente__nome')
    inlines = [ItemPedidoInline]

    def listar_itens(self, obj):
        return ", ".join(
            [f"{item.quantidade}x {item.perfume.nome}" for item in obj.itens.all()]
        )

    listar_itens.short_description = "Produtos"


