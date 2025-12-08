from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index,name='index'),
    path('produto/<slug:slug>',views.produto,name="produto"),
    path('logon/',views.logon_validation,name="tela_logon"),
    path('perfil/',views.perfil,name="perfil"),
    path('perfil/dados_pessoais',views.dados_pessoais,name="dados_pessoais"),
    path('perfil/endereco',views.endereco,name="endereco"),
    path('perfil/pedidos',views.pedidos,name="pedidos"),
    path('perfil/metodos_pagamento',views.metodos_pagamento,name="metodos_pagamento"),
    path('perfil/autenticacao',views.autenticacao,name="autenticacao"),
    path('perfil/notificacao',views.notificacao,name="notificacao"),
    path('administracao/',views.administracao,name='administracao'),
    path('administracao/usuarios',views.usaurios,name="usuarios"),
    path('administracao/usuario/<int:id>',views.usuario,name="usuario"),
    path('administracao/usuario/criar',views.criar_usuario,name="usuario_criar"),
    path('administracao/usuario/alterar_senha/<int:id>',views.alterar_senha,name="alterar_senha"),
    path('administracao/produtos',views.produtos,name="produtos"),
    path('administracao/produtos/editar/<int:id>',views.produto_edit,name="produto_editar"),
    path('administracao/produtos/criar',views.criar_produto,name="produto_criar"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)