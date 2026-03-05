from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal

from .models import Produto, Categoria, Usuario, ImagemProduto, Endereco, Notificacao, Pedido, ItemPedido

# ----------------------------
# PÁGINA INICIAL E PRODUTOS
# ----------------------------
def index(request):
    produtos = Produto.objects.filter(ativo=True, estoque__gt=0).order_by('-data_cadastro')[:10]
    return render(
        request,
        "loja/static/html/inicio/index.html",
        {"produtos": produtos, "usuario": request.user if request.user.is_authenticated else None}
    )

def produto(request, slug):
    produto_principal = get_object_or_404(Produto, slug=slug)
    produtos = Produto.objects.filter(categoria=produto_principal.categoria).order_by('-data_cadastro')
    imagens_produto_principal = ImagemProduto.objects.filter(produto=produto_principal)
    usuario = Usuario.objects.filter(auth_user=request.user).first() if request.user.is_authenticated else None

    return render(request, './loja/static/html/inicio/produto.html', {
        'produtos': produtos,
        'produto_principal': produto_principal,
        "imagens_produto_principal": imagens_produto_principal,
        'cliente': usuario
    })

# ----------------------------
# LOGIN, LOGOUT E CADASTRO
# ----------------------------
def tela_logon(request):
    return render(request,'./loja/static/html/perfil/tela_logon.html')

def logon_validation(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.groups.filter(name="Administrador").exists() or user.is_superuser:
                return redirect('administracao')
            return redirect('index')
        else:
            error = "Usuário ou senha incorretos."
    return render(request,'./loja/static/html/perfil/tela_logon.html',{'error': error})

def criar_conta(request):
    return render(request,'./loja/static/html/perfil/criar_conta.html')

@login_required
def sair(request):
    logout(request)
    return redirect('index')

# ----------------------------
# PERFIL DO USUÁRIO
# ----------------------------
@login_required
def perfil(request):
    usuario = Usuario.objects.filter(auth_user=request.user).first()
    return render(request,'./loja/static/html/perfil/perfil.html',{"cliente": usuario})

@login_required
def dados_pessoais(request):
    usuario = Usuario.objects.get(auth_user=request.user)
    if request.method == "POST":
        try:
            usuario.nome = request.POST.get("nome")
            usuario.CPF = request.POST.get("CPF")
            usuario.genero = request.POST.get("genero")
            data_nascimento = request.POST.get("data_nascimento")
            if data_nascimento:
                usuario.data_nascimento = data_nascimento
            usuario.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect("dados_pessoais") 
        except Exception:
            messages.error(request, "Erro ao atualizar os dados.")
            return redirect("dados_pessoais")
    return render(request, "./loja/static/html/perfil/dados_pessoais.html", {"cliente": usuario})

@login_required
def endereco(request):
    usuario = Usuario.objects.filter(auth_user=request.user).first()
    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "adicionar":
            Endereco.objects.create(
                user=usuario,
                endereco=request.POST.get("endereco"),
                cep=request.POST.get("cep")
            )
        elif acao == "editar":
            endereco_id = request.POST.get("endereco_id")
            endereco_obj = Endereco.objects.filter(id=endereco_id, user=usuario).first()
            if endereco_obj:
                endereco_obj.endereco = request.POST.get("endereco")
                endereco_obj.cep = request.POST.get("cep")
                endereco_obj.save()
        elif acao == "deletar":
            endereco_id = request.POST.get("endereco_id")
            Endereco.objects.filter(id=endereco_id, user=usuario).delete()
        return JsonResponse({"status": "ok"})
    enderecos = Endereco.objects.filter(user=usuario)
    return render(request, "./loja/static/html/perfil/endereco.html", {"enderecos": enderecos, "cliente": usuario})

@login_required
def notificacao(request):
    usuario = Usuario.objects.filter(auth_user=request.user).first()
    notificacoes = Notificacao.objects.filter(usuario=usuario)
    return render(request, './loja/static/html/perfil/notificacao.html', {'notificacaos': notificacoes})

@login_required
def pedidos(request):
    usuario = Usuario.objects.filter(auth_user=request.user).first()
    pedidos = Pedido.objects.filter(cliente=usuario)
    return render(request,'./loja/static/html/perfil/pedidos.html',{"pedidos": pedidos})

# ----------------------------
# ADMINISTRADOR - PRODUTOS
# ----------------------------
@login_required
@permission_required('loja.view_produto', raise_exception=True)
def produtos(request):
    produtos_ = Produto.objects.all()
    imagens_produtos = {}
    for produto in produtos_:
        imagens = ImagemProduto.objects.filter(produto=produto)
        imagens_produtos[produto.id] = imagens.first().imagem.url if imagens.exists() else '/static/imagens/perfumes_1.jpg'
    return render(request, "./loja/static/html/administrador/produtos.html", {'produtos': produtos_, 'imagens_produtos': imagens_produtos})


@require_POST
def adicionar_carrinho(request):
    produto_id = request.POST.get("produto_id")
    if not produto_id:
        return JsonResponse({"erro": "Produto não enviado"}, status=400)
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return JsonResponse({"erro": "Produto não encontrado"}, status=404)
    carrinho = request.session.get("carrinho", {})
    if produto_id in carrinho:
        carrinho[produto_id]["quantidade"] += 1
    else:
        carrinho[produto_id] = {
            "nome": produto.nome,
            "preco": float(produto.preco),
            "quantidade": 1,
            "imagem": produto.imagem_principal.url if produto.imagem_principal else ""
        }
    request.session["carrinho"] = carrinho
    request.session.modified = True
    return JsonResponse({"status": "sucesso", "carrinho": carrinho})

@login_required
def checkout(request):
    carrinho = request.session.get("carrinho", {})

    total_carrinho = sum(
        item["preco"] * item["quantidade"]
        for item in carrinho.values()
    )

    # Usuário logado
    usuario = Usuario.objects.filter(auth_user=request.user.id).first()

    # Endereços do usuário
    enderecos = Endereco.objects.filter(user=usuario)

    if request.method == "POST":
        
        endereco_selecionado = request.POST.get("endereco_id")
        metodo_pagamento = request.POST.get("pagamento")

        # Validar
        if not endereco_selecionado or not metodo_pagamento:
            messages.error(request, "Escolha um endereço e método de pagamento.")
            return redirect("chekout")

        endereco = Endereco.objects.get(id=endereco_selecionado, user=usuario)

        # Criar pedido
        pedido = Pedido.objects.create(
            cliente=usuario,
            endereco_entrega=endereco,
            metodo_pagamento=metodo_pagamento,
            status='P',  # Pendente
        )

        # Adicionar itens do carrinho
        total = 0
        for id_item, item in carrinho.items():
            produto = Produto.objects.get(id=id_item)
            ItemPedido.objects.create(
                pedido=pedido,
                perfume=produto,
                quantidade=item["quantidade"],
                preco_unitario=item["preco"]
            )
            total += item["quantidade"] * item["preco"]

        # Atualizar total
        pedido.valor_total = total
        pedido.save()

        # Limpar carrinho
        request.session["carrinho"] = {}

        messages.success(request, f"Pedido {pedido.numero_pedido} criado com sucesso!")
        return redirect("detalhes_pedido", pedido_id=pedido.id)

    return render(
        request,
        "./loja/static/html/chekout/chekout.html",
        {
            "carrinho": carrinho,
            "total": total_carrinho,
            "enderecos": enderecos,
        }
    )


@login_required
def detalhes_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    itens = pedido.itens.all()

    return render(
        request,
        "./loja/static/html/chekout/detalhes_pedido.html",
        {
            "pedido": pedido,
            "itens": itens,
        }
    )