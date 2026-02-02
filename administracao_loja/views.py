from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from loja.models import Usuario, Pedido



def painel_gestao(request):
    usuarios = Usuario.objects.all()
    pedidos = Pedido.objects.select_related('cliente').order_by('-data_pedido')

    return render(request, './administracao_loja/static/html/index.html', {
        'usuarios': usuarios,
        'pedidos': pedidos
    })
