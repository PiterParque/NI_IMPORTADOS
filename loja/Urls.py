from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("pesquisa/", views.pesquisa, name="pesquisa"),
    path('categoria/<int:categoria_id>/',views.categoria,name='categoria'),
    path('marca/<int:marca_id>/',views.marca,name='marca'),
    path('tamanho/<int:tamanho_id>/',views.tamanho,name='tamanho'),
    path('produto/<slug:slug>/', views.produto, name="produto"),
    path('logon/', views.logon_validation, name="tela_logon"),
    path('criar_conta/', views.criar_conta, name="criar_conta"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/dados_pessoais/', views.dados_pessoais, name="dados_pessoais"),
    path('perfil/endereco/', views.endereco, name="endereco"),
    path('perfil/pedidos/', views.pedidos, name="pedidos"),
    path('perfil/notificacao/', views.notificacao, name="notificacao"),
    path('obter_carrinho/', views.obter_carrinho, name='obter_carrinho'),
    path("adicionar_carrinho/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path('remover_carrinho/', views.remover_carrinho, name='remover_carrinho'),
    path("checkout/", views.checkout, name="chekout"),
    path("detalhes_pedido/<uuid:pedido_id>/", views.detalhes_pedido, name="detalhes_pedido"),
    path('sair/', views.sair, name='logout'),
    path('accounts/', include('allauth.urls')),  # se quiser usar django-allauth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)