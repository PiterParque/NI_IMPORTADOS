from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Usuario, Produto, Pedido,Endereco
from .forms import UsuarioForm, ProdutoForm, PedidoForm,EnderecoForm,EnderecoFormSet



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
    produtos = Produto.objects.all()
    print(produtos)
    return render(request, './administracao_loja/static/html/produtos.html', {'produtos': produtos})

# editar dados
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)

    form = UsuarioForm(
        request.POST or None,
        request.FILES or None,
        instance=usuario
    )

    formset = EnderecoFormSet(
        request.POST or None,
        instance=usuario
    )

    if request.method == "POST":
        if form.is_valid() and formset.is_valid():
            usuario = form.save()
            formset.instance = usuario
            formset.save()

            return redirect('usuarios')

    return render(
        request,
        'administracao_loja/static/html/edit_usuario.html',
        {
            'form': form,
            'formset': formset
        }
    )

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('PRODUTOS')

    return render(request, './administracao_loja/static/html/edit_produto.html', {'form': form})


def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    form = PedidoForm(request.POST or None, instance=pedido)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('pedidos')

    return render(request, 'administracao_loja/static/html/edit_pedido.html', {'form': form})

# criar dados
def criar_usuario(request):
    form = UsuarioForm(request.POST or None)
    form_endereco = EnderecoForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            usuario = form.save()

            if form_endereco.is_valid() and request.POST.get("criar_endereco"):
                endereco = form_endereco.save(commit=False)
                endereco.user = usuario
                endereco.save()

            return redirect('usuarios')

    return render(
        request,
        './administracao_loja/static/html/criar_usuario.html',
        {
            'form': form,
            'form_endereco': form_endereco
        }
    )



def criar_produto(request):
    form = ProdutoForm()
    if request.method == "POST":
        form = ProdutoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('PRODUTOS')
        else:
            return render(request, './administracao_loja/static/html/criar_produto.html', {'form': form})
    else:
        return render(request, './administracao_loja/static/html/criar_produto.html', {'form': form})


def criar_pedido(request):
    form = PedidoForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            pedido = form.save(commit=False)

            # gera numero simples
            ultimo = Pedido.objects.last()
            if ultimo:
                pedido.numero_pedido = str(int(ultimo.numero_pedido) + 1)
            else:
                pedido.numero_pedido = "1"

            pedido.save()

            return redirect('pedidos')

    return render(
        request,
        'administracao_loja/static/html/criar_pedido.html',
        {'form': form}
    )

