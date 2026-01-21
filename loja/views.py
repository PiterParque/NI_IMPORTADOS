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
    produtos=Produto.objects.filter(ativo=True).order_by('-data_cadastro')
    usuario_id =request.session.get('usuario_id')
    usuario=Usuario.objects.filter(id=usuario_id).first()
    return render(request,'./loja/static/html/inicio/index.html',{'produtos':produtos,'cliente':usuario})
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
    usuario_id = request.session.get('usuario_id')


    usuario = Usuario.objects.filter(id=usuario_id).first()


    # 🔹 Buscar notificações do usuário + notificações globais
    notificacoes = Notificacao.objects.filter(
        Q(user=usuario) | Q(user__isnull=True)
    ).order_by('-criado_em')

    return render(
        request,
        './loja/static/html/perfil/notificacao.html',
        {
          
            "notificacoes": notificacoes
        }
    )
def pedidos(request):
    usuario_id = request.session.get('usuario_id')

    usuario=Usuario.objects.filter(id=usuario_id).first()
    return render(request,'./loja/static/html/perfil/pedidos.html',{"cliente":usuario})
def sair(request):
    request.session.pop('usuario_id', None)
    return redirect('index')

#------------------
def administracao(request):

    return render(request,"./loja/static/html/administrador/administracao.html")
def usaurios(request):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    _usuarios=Usuario.objects.all()
    _usuarios=_usuarios.values()
    for i,_usuario in enumerate(_usuarios):
        if isinstance(_usuario['data_nascimento'], date):
            ano,mes,dia=str(_usuarios[i]['data_nascimento']).split('-')
            _usuarios[i]['data_nascimento']=dia+"/"+mes+"/"+ano
    quatidade_usuario=len(Usuario.objects.all().values())

      


    
    return render(request,"./loja/static/html/administrador/usuarios.html",{'usuarios':_usuarios,"quantidade_usuarios":quatidade_usuario})
def usuario(request,id):
    _usuario=False
    usuario_alterado=False
    mensagem=''
    try:
        usuario_id = request.session.get('usuario_id')
        user=Usuario.objects.filter(id=usuario_id).values()
       
        if user:
            if user[0]['tipo_usuario'] != "Administrador":
                redirect('perfil')
        user=Usuario.objects.filter(id=id).values()
        user=user[0]
        if isinstance(user['data_nascimento'], date):
            print(user['data_nascimento'])
            ano,mes,dia=str(user['data_nascimento'].strftime("%d/%m/%Y")).split("/")
            user['data_nascimento']=dia+"-"+mes+"-"+ano
        usuario_alterado=False
        mensagem="Falha em alterar o usuario"
        if user :
            if user['tipo_usuario'] != "Admisnitrador":
                redirect('perfil')
        if id:
            _usuario=Usuario.objects.filter(id=id).first()
        try:
           if request.method == "POST":
            
                    usuario_obj = Usuario.objects.get(id=id)

                    imagem = request.FILES.get("imagem_usuario")
                    nome = request.POST.get("usuario_nome")
                    cpf = request.POST.get("usuario_cpf")
                    data_nascimento = request.POST.get("usuario_nascimento")
                    telefone = request.POST.get("usuario_telefone")
                    genero = request.POST.get("genero")
                    if genero == "OUTRO":
                        genero = request.POST.get("outro_genero")

                    tipo_usuario = request.POST.get("usuario_tipo")

                    usuario_obj.nome = nome
                    usuario_obj.CPF = cpf
                    usuario_obj.data_nascimento = data_nascimento
                    usuario_obj.telefone = telefone
                    usuario_obj.genero = genero
                    usuario_obj.tipo_usuario = tipo_usuario

                    if imagem:
                        usuario_obj.imagem_usuario = imagem

                    usuario_obj.save()

                    usuario_alterado = True
                    mensagem = "Usuário alterado com sucesso"

        
          
                
        except Exception as e:
                print("Erro:",e)
    except Exception as e :
        print("Erro:",e)
        

    return render(request,"./loja/static/html/administrador/usuario.html",{'usuario':_usuario,'usuario_alterado':usuario_alterado,"mensagem":mensagem})
def criar_usuario(request):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    usuario_criado=None
 
    try:
           if request.method == "POST":
            
                    usuario_obj = Usuario.objects.create()

                    imagem = request.FILES.get("imagem_usuario")
                    nome = request.POST.get("entrada_nome")
                    senha=request.POST.get("entrada_senha")
                    cpf = request.POST.get("entrada_cpf")
                    data_nascimento = request.POST.get("entrada_nascimento")
                    telefone = request.POST.get("entrada_telefone")
                    genero = request.POST.get("genero")
                    if genero == "OUTRO":
                        genero = request.POST.get("campo_outro_genero")

                    tipo_usuario = request.POST.get("tipo_de_usuario")

                    usuario_obj.nome = nome
                    usuario_obj.senha = senha
                    usuario_obj.CPF = cpf
                    usuario_obj.data_nascimento = data_nascimento
                    usuario_obj.telefone = telefone
                    usuario_obj.genero = genero
                    usuario_obj.tipo_usuario = tipo_usuario

                    if imagem:
                        usuario_obj.imagem_usuario = imagem

                    usuario_obj.save()

                    usuario_alterado = True
                    mensagem = "Usuário alterado com sucesso"

        
    except Exception as e:
                print("Erro:",e)
        

    return render(request,"./loja/static/html/administrador/usuario_criar.html",{'usuario_criado':usuario_criado})
def alterar_senha(request,id):
    usuario_id = request.session.get('usuario_id')
    user=Usuario.objects.filter(id=usuario_id).first()
    if user :
        if user.tipo_usuario != "Admisnitrador":
            redirect('perfil')
    senha_alterada=None
    usuario_senha=None
    try:
       usuario_senha=Usuario.objects.filter(id=id).first()
       if request.method == "POST":
           senha= request.POST.get("senha")
           usuario_senha.senha=senha
           usuario_senha.save()
           senha_alterada="Senha Alterada com Sucesso"
    except Exception as e:
        print("Erro:",e)
    return render(request,"./loja/static/html/administrador/alterar_senha.html",{'senha_alterada':senha_alterada,"usuario":usuario_senha})
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
def produto_edit(request, id):

    usuario_id = request.session.get('usuario_id')
    user = Usuario.objects.filter(id=usuario_id).first()

    # Usuário inválido ou não administrador
    if not user:
        return redirect('login')

    if user.tipo_usuario != "Administrador":
        return redirect('perfil')

    # Carregar produto
    produto = get_object_or_404(Produto, id=id)

    # Carregar imagens do produto
    imagens = ImagemProduto.objects.filter(produto=produto)

    # Carregar categorias
    categorias = Categoria.objects.all()
    # Carrega todas as marcas
    marcas=Produto.objects.values_list('marca',flat=True).distinct().order_by('marca')
    # 🚀 Se for POST, atualizar dados
    if request.method == "POST":
        try:
   
            produto.imagem_principal=request.FILES.get('entrada_imagem_1')
            produto.nome = request.POST.get('nome')
            produto.subtitulo = request.POST.get('subtitulo')
            produto.marca = request.POST.get('marca')
            produto.ml = request.POST.get('ml')
            produto.preco = request.POST.get('preco')
            produto.estoque = request.POST.get('estoque')
            produto.tamanho = request.POST.get('tamanho')
            # Foreign Key → precisa puxar o objeto categoria
            categoria_nome = request.POST.get('categoria')
            produto.descricao=request.POST.get('descricao')
            if categoria_nome:
                categoria_obj = Categoria.objects.filter(nome=categoria_nome).first()
                if categoria_obj:
                    produto.categoria = categoria_obj
            produto.save()
            imagens_={}
            for i in "12345":
               imagens_["imagem_"+i]=request.FILES.get("entrada_imagem_"+str(i))
            for i,img in enumerate(list(imagens_.keys())[1:]):
                if imagens_[img] != None:
                    s=ImagemProduto.objects.get(id=imagens[i].id)
                    s.imagem=imagens_[img]
                    s.save()
                    
            
            return redirect('produto_editar', id=id)

        except Exception as e:
            print("Erro ao atualizar:", e)

    return render(request,
        "./loja/static/html/administrador/produto_edit.html",
        {
            'produto': produto,
            'imagens': imagens,
            'categorias': categorias,
            'marcas':marcas
        }
    )
def criar_produto(request):
    usuario_id = request.session.get('usuario_id')
    user = Usuario.objects.filter(id=usuario_id).first()
    if not user or user.tipo_usuario != "Administrador":
        return redirect('perfil')
    retorno = {"retorno": '', "sinal_retorno": True}
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        try:
            # Dados do formulário
            nome = request.POST.get('nome')
            subtitulo = request.POST.get('subtitulo')
            sku = request.POST.get('sku')
            marca = request.POST.get('marca')
            categoria_id = request.POST.get('categoria')
            ml = request.POST.get('ml')
            preco = request.POST.get('preco')
            estoque = request.POST.get('estoque')
            tamanho = request.POST.get('tamanho')
            descricao=request.POST.get('descricao')
            # Imagens recebidas
            imagem_1 = request.FILES.get('imagem_1_principal')
            imagem_2 = request.FILES.get('imagem_2')
            imagem_3 = request.FILES.get('imagem_3')
            imagem_4 = request.FILES.get('imagem_4')
            imagem_5 = request.FILES.get('imagem_5')
            # Caminho da imagem padrão (corrigido para usar os.path.join e barras corretas)
            caminho_padrao = os.path.join(settings.BASE_DIR, 'loja', 'static', 'imagens', 'image.jpg')
            with open(caminho_padrao, "rb") as f:
                imagem_padrao = ContentFile(f.read(), name="padrao.jpg")
            # Substitui imagens vazias pela imagem padrão
            imagens = [
                imagem_2,
                imagem_3,
                imagem_4,
                imagem_5,
            ]
            for i,img in enumerate(imagens):
                if img == None:
                    imagens[i]= imagem_padrao

            # Cria o produto com imagem principal
            produto_ = Produto.objects.create(
                nome=nome,
                subtitulo=subtitulo,
                sku=sku,
                marca=marca,
                categoria_id=categoria_id,
                ml=ml,
                preco=preco,
                estoque=estoque,
                tamanho=tamanho,
                imagem_principal=imagem_1,
                descricao=descricao
            )
            produto_.save()
            
            # Cria imagens extras (2 a 5)
            for img in imagens:
                i=ImagemProduto.objects.create(
                    produto=produto_,
                    imagem=img
                ).save()
               
            retorno = {"retorno": "Produto cadastrado com sucesso", "sinal_retorno": True}
        except Exception as e:
            print("Erro:", e)
            retorno = {"retorno": str(e), "sinal_retorno": False}
    return render(request, "loja/static/html/administrador/produto_criar.html", {
        "categorias": categorias,
        "retorno": retorno
    })
def gerenciamentos_pedidos(request):
    return render(request, "loja/static/html/administrador/gerenciamento_pedidos.html")
def gerenciamento_pedido(request):
    return render(request, "loja/static/html/administrador/gerenciamento_pedido.html")
from django.http import JsonResponse
from .models import Produto


def adicionar_carrinho(request):
    if request.method == "POST":
        produto_id = request.POST.get("produto_id")

        if not produto_id:
            return JsonResponse(
                {"erro": "Produto inválido"},
                status=400
            )

        carrinho = request.session.get("carrinho", {})

        if produto_id in carrinho:
            carrinho[produto_id]["quantidade"] += 1
        else:
            produto = get_object_or_404(Produto, id=int(produto_id))
            carrinho[produto_id] = {
                "nome": produto.nome,
                "preco": str(produto.preco),
                "quantidade": 1
            }

        request.session["carrinho"] = carrinho
        request.session.modified = True

        return JsonResponse({
            "status": "ok",
            "carrinho": carrinho
        })


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