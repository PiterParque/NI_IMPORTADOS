from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from loja.models import Produto, Pedido

# Grupo: Gerente de Produtos
grupo_produtos, created = Group.objects.get_or_create(name='Gerente de Produtos')
content_type_produto = ContentType.objects.get_for_model(Produto)
permissoes_produto = Permission.objects.filter(
    content_type=content_type_produto,
    codename__in=['add_produto','change_produto','delete_produto']
)
grupo_produtos.permissions.set(permissoes_produto)

# Grupo: Atendente de Pedidos
grupo_pedidos, created = Group.objects.get_or_create(name='Atendente de Pedidos')
content_type_pedido = ContentType.objects.get_for_model(Pedido)
permissoes_pedido = Permission.objects.filter(
    content_type=content_type_pedido,
    codename__in=['view_pedido','change_pedido']
)
grupo_pedidos.permissions.set(permissoes_pedido)