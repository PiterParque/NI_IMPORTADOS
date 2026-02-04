from django.shortcuts import render,redirect,get_object_or_404
from .models import Produto,Categoria,Usuario,ImagemProduto,Endereco,Notificacao
from django.core.files.base import ContentFile
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
import os
from datetime import date
import json
from django.http import JsonResponse
from decimal import Decimal

# Create your views here.
def index(request):
    produtos = (
        Produto.objects
        .filter(ativo=True, estoque__gt=0)
        .order_by('-data_cadastro')[:10]
    )

    return render(
        request,
        "loja/static/html/inicio/index.html",
        {"produtos": produtos}
    )
def produto(request,slug):
    produto_principal=Produto.objects.filter(slug=slug).first()
    id_categoria=produto_principal.categoria_id
    produtos=Produto.objects.filter(categoria=id_categoria).order_by('-data_cadastro')
    imagesn_produto_principal=ImagemProduto.objects.filter(produto=produto_principal.id)
    usuario_id =request.session.get('usuario_id')
    usuario=Usuario.objects.filter(id=usuario_id).first()
    return render(request,'./loja/static/html/inicio/produto.html',{
        'produtos':produtos,'produto_principal':produto_principal,
        "imagens_produto_principal":imagesn_produto_principal,
        'cliente':usuario})

#------Perfil-------
def tela_logon(request):
    return render(request,'./loja/static/html/perfil/tela_logon.html')
def logon_validation(request):
    error=None
    if request.method == "POST":
        username = request.POST.get("username")
        password=request.POST.get("password")
        user= Usuario.objects.filter(nome=username, senha=password).first()
        if user :
            if user.tipo_usuario == "Administrador":
                request.session['usuario_id'] = user.id
                return redirect('administracao')
   
            request.session['usuario_id'] = user.id
            return redirect('index')
        else:
            error="Usuário ou senha incorretos."
    return render(request,'./loja/static/html/perfil/tela_logon.html',{'error':error})
def criar_conta(request):
    return render(request,'./loja/static/html/perfil/criar_conta.html')
def perfil(request):
    usuario_id = request.session.get('usuario_id')

    usuario=Usuario.objects.filter(id=usuario_id).first()
    return render(request,'./loja/static/html/perfil/perfil.html',{"cliente":usuario})
def dados_pessoais(request):
    usuario_id = request.session.get('usuario_id')



    usuario = Usuario.objects.filter(id=usuario_id).first()



    # 🔹 SE FOR POST → SALVAR DADOS
    if request.method == "POST":
        usuario.nome = request.POST.get("nome")
        usuario.CPF = request.POST.get("cpf")
        usuario.telefone = request.POST.get("telefone")
        usuario.data_nascimento = request.POST.get("data_nascimento")

        genero = request.POST.get("GENERO")
        genero_outro = request.POST.get("genero_outro")
        usuario.email = request.POST.get("email")

        if genero == "OUTRO" and genero_outro:
            usuario.genero = genero_outro
        else:
            usuario.genero = genero

        # Se quiser permitir alterar email futuramente
        # usuario.email = request.POST.get("email")

        usuario.save()

        messages.success(request, "Dados atualizados com sucesso!")

        return redirect("dados_pessoais")  # evita reenvio do formulário

    return render(
        request,
        "./loja/static/html/perfil/dados_pessoais.html",
        {"cliente": usuario}
    )
def endereco(request):
    usuario_id = request.session.get('usuario_id')



    usuario = Usuario.objects.filter(id=usuario_id).first()


    if request.method == "POST":
        acao = request.POST.get("acao")

        # 🔹 ADICIONAR
        if acao == "adicionar":
            Endereco.objects.create(
                user=usuario,
                endereco=request.POST.get("endereco"),
                cep=request.POST.get("cep")
            )

        # 🔹 ATUALIZAR
        elif acao == "editar":
            endereco_id = request.POST.get("endereco_id")
            endereco = Endereco.objects.filter(id=endereco_id, user=usuario).first()

            if endereco:
                endereco.endereco = request.POST.get("endereco")
                endereco.cep = request.POST.get("cep")
                endereco.save()

        # 🔹 DELETAR
        elif acao == "deletar":
            endereco_id = request.POST.get("endereco_id")
            Endereco.objects.filter(id=endereco_id, user=usuario).delete()

        return redirect("endereco")

    enderecos = Endereco.objects.filter(user=usuario)

    return render(
        request,
        "./loja/static/html/perfil/endereco.html",
        {"enderecos": enderecos,"cliente":usuario}
    )

def notificacao(request):

    return render(
        request,
        './loja/static/html/perfil/notificacao.html',
    )
def pedidos(request):
    usuario_id = request.session.get('usuario_id')

    usuario=Usuario.objects.filter(id=usuario_id).first()
    return render(request,'./loja/static/html/perfil/pedidos.html',{"cliente":usuario})
def sair(request):
    request.session.pop('usuario_id', None)
    return redirect('index')

#------------------

def produtos(request):
    produtos_ = Produto.objects.all()

    # Criar um dicionário com pelo menos uma imagem por produto
    imagens_produtos = {}
    for produto in produtos_:
        imagens = ImagemProduto.objects.filter(produto=produto)
        if imagens.exists():
            imagens_produtos[produto.id] = imagens.first().imagem.url
        else:
            # imagem padrão
            imagens_produtos[produto.id] = '/static/imagens/perfumes_1.jpg'
    print(produtos_.values())
    return render(request, "./loja/static/html/administrador/produtos.html", {
        'produtos': produtos_,
        'imagens_produtos': imagens_produtos
    })

def adicionar_ao_carrinho(request):
    if request.method == "POST":
        produto_id = request.POST.get("produto_id")
        produto = get_object_or_404(Produto, id=produto_id)

        carrinho = request.session.get("carrinho", {})

        if str(produto_id) in carrinho:
            carrinho[str(produto_id)]["quantidade"] += 1
        else:
            carrinho[str(produto_id)] = {
                "nome": produto.nome,
                "preco": float(produto.preco_promocional or produto.preco),
                "imagem": produto.imagem_principal.url if produto.imagem_principal else "",
                "quantidade": 1,
            }

        request.session["carrinho"] = carrinho
        request.session.modified = True

        return JsonResponse({"status": "ok", "carrinho": carrinho})
    

def salvar_carrinho(request):
    if request.method == "POST":
        carrinho = json.loads(request.body)

        request.session["carrinho"] = carrinho
        request.session.modified = True

        return JsonResponse({"ok": True})

    return JsonResponse({"ok": False})
def detalhes_pedido(request):
    carrinho = request.session.get("carrinho", {})
    itens = []
    total = Decimal("0.00")
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    enderecos_entrega=Endereco.objects.filter(user=user).values()
    

    for id, item in carrinho.items():
        produto = Produto.objects.get(id=id)
        subtotal = produto.preco * item["quantidade"]

        itens.append({
            "imagem_principal":produto.imagem_principal,
            "nome": produto.nome,
            "quantidade": item["quantidade"],
            "preco": produto.preco,
            "subtotal": subtotal,
        })

        total += subtotal

    return render(request, "./loja/static/html/inicio/detalhes_pedido.html", {
        "itens": itens,
        "total": total,
         "enderecos_entrega":enderecos_entrega,
    })