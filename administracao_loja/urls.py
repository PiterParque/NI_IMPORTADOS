from django.urls import path,include
from administracao_loja import views
urlpatterns = [
    path('',views.painel_gestao,name="index"),
    path('usuarios',views.Usuarios,name="usuarios"),
    path('pedidos',views.pedidos,name="pedidos")
]
