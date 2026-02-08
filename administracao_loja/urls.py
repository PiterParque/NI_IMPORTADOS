from django.urls import path
from administracao_loja import views

urlpatterns = [
    path('', views.painel_gestao, name='index'),

    path('usuarios/', views.Usuarios, name='usuarios'),
    path('usuarios/criar/', views.criar_usuario, name='criar_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),

    path('produtos/', views.lista_produtos, name='PRODUTOS'),
    path('produtos/criar/', views.criar_produto, name='criar_produto'),
    path('produtos/editar/<int:id>/', views.editar_produto, name='editar_produto'),

    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/criar/', views.criar_pedido, name='criar_pedido'),
    path('pedidos/editar/<slug:id>/', views.editar_pedido, name='editar_pedido'),
]
