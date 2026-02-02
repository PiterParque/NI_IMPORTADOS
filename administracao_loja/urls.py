from django.urls import path,include
from administracao_loja import views
urlpatterns = [
    path('',views.painel_gestao,name="index")
]
