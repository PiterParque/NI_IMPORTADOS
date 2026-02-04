from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Usuario, Produto, Pedido
from .forms import UsuarioForm, ProdutoForm, PedidoForm



def painel_gestao(request):
    usuarios = Usuario.objects.all()
    
    return render(request, './administracao_loja/static/html/index.html', {
        'usuarios': usuarios,
        
    })
# painel para visualizar dados
def Usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, './administracao_loja/static/html/usuarios.html',{
        'usuarios': usuarios})
def pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').order_by('-data_pedido')
    return render(request, './administracao_loja/static/html/pedidos.html', {'pedidos': pedidos})
def lista_produtos(request):
    produtos = Produto.objects.filter(ativo=True)
    return render(request, './administracao_loja/static/html/produtos.html', {'produtos': produtos})

# editar dados
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    form = UsuarioForm(request.POST or None, request.FILES or None, instance=usuario)

    if form.is_valid():
        form.save()
        return redirect('usuarios')

    return render(request, 'administracao_loja/editar_usuario.html', {'form': form})


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)

    if form.is_valid():
        form.save()
        return redirect('PRODUTOS')

    return render(request, 'administracao_loja/editar_produto.html', {'form': form})


def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    form = PedidoForm(request.POST or None, instance=pedido)

    if form.is_valid():
        form.save()
        return redirect('pedidos')

    return render(request, 'administracao_loja/editar_pedido.html', {'form': form})

# criar dados
def criar_usuario(request):
    form = UsuarioForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('usuarios')

    return render(request, './administracao_loja/static/html/criar_usuario.html', {'form': form})


def criar_produto(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('PRODUTOS')

    return render(request, './administracao_loja/static/html/criar_produto.html', {'form': form})


def criar_pedido(request):
    form = PedidoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('pedidos')

    return render(request, './administracao_loja/static/html/criar_pedido.html', {'form': form})
