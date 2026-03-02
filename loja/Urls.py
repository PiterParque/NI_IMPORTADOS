from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('produto/<slug:slug>/', views.produto, name="produto"),
    path('logon/', views.logon_validation, name="tela_logon"),
    path('criar_conta/', views.criar_conta, name="criar_conta"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/dados_pessoais/', views.dados_pessoais, name="dados_pessoais"),
    path('perfil/endereco/', views.endereco, name="endereco"),
    path('perfil/pedidos/', views.pedidos, name="pedidos"),
    path('perfil/notificacao/', views.notificacao, name="notificacao"),
    path("adicionar_carrinho/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path("checkout/", views.checkout, name="chekout"),
    path("detalhes_pedido/<uuid:pedido_id>/", views.detalhes_pedido, name="detalhes_pedido"),
    path('sair/', views.sair, name='logout'),
    path('accounts/', include('allauth.urls')),  # se quiser usar django-allauth
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)