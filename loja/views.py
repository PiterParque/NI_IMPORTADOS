from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from .models import Produto,Categoria,Usuario,ImagemProduto,Endereco,Notificacao,Pedido
from django.core.files.base import ContentFile
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
import os
from datetime import date
import json
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.auth import login


# Create your views here.
def index(request):
    produtos = (
        Produto.objects
        .filter(ativo=True, estoque__gt=0)
        .order_by('-data_cadastro')[:10]
    )
    usuario=None
    if request.user.is_authenticated:
        usuario=request.user
    return render(
        request,
        "loja/static/html/inicio/index.html",
        {"produtos": produtos,
         "usuario":usuario}
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
    usuario_id = request.user
    usuario=Usuario.objects.filter(auth_user_id=usuario_id).first()
    id_user_loja=usuario.id

    return render(request,'./loja/static/html/perfil/perfil.html',{"cliente":usuario})
def dados_pessoais(request):
    usuario = Usuario.objects.get(auth_user_id=request.user)
    
    if request.method == "POST":
        try:
            usuario.nome=request.POST.get("nome")
            usuario.CPF=request.POST.get("CPF")
            usuario.genero=request.POST.get("genero")
            data_nascimento=request.POST.get("data_nascimento")
            if data_nascimento != "":
              usuario.data_nascimento=data_nascimento
            usuario.save()
            messages.success(request, "Dados atualizados com sucesso!")
            return redirect("dados_pessoais") 
        except:
            messages.error(request, "Erro ao atualizar os dados.")
            return redirect("dados_pessoais")
        


       
   
    return render(
        request,
        "./loja/static/html/perfil/dados_pessoais.html",
        {"cliente": usuario}
    )
def endereco(request):
    usuario = Usuario.objects.filter(auth_user_id=request.user).first()

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

        # 🔥 AQUI MUDA TUDO
        return JsonResponse({"status": "ok"})

    enderecos = Endereco.objects.filter(user=usuario)

    return render(
        request,
        "./loja/static/html/perfil/endereco.html",
        {"enderecos": enderecos, "cliente": usuario}
    )

def notificacao(request):
    notificacao = Notificacao.objects.filter(usuario=request.user.id)
    return render(
        request,
        './loja/static/html/perfil/notificacao.html',
        {'notificacaos':notificacao}
    )
def pedidos(request):
    Pedidos = Pedido.objects.filter(cliente=request.user.id)

    return render(request,'./loja/static/html/perfil/pedidos.html',{"pedidos":Pedidos})
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
@require_POST
def adicionar_carrinho(request):

    produto_id = request.POST.get("produto_id")

    if not produto_id:
        return JsonResponse({"erro": "Produto não enviado"}, status=400)

    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        return JsonResponse({"erro": "Produto não encontrado"}, status=404)

    # Pega o carrinho da sessão
    carrinho = request.session.get("carrinho", {})

    # Se já existir no carrinho, soma quantidade
    if produto_id in carrinho:
        carrinho[produto_id]["quantidade"] += 1
    else:
        carrinho[produto_id] = {
        "nome": produto.nome,
        "preco": float(produto.preco),
        "quantidade": 1,
        "imagem": produto.imagem_principal.url if produto.imagem_principal else ""
    }


    # Salva novamente na sessão
    request.session["carrinho"] = carrinho
    request.session.modified = True

    return JsonResponse({
        "status": "sucesso",
        "carrinho": carrinho
    })
def chekout(request):
    if not request.user.is_authenticated:
        redirect("google")
        
    return render(request,"./loja/static/html/chekout/chekout.html")            