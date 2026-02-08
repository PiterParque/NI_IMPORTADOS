import os
from django.db import models
from django.utils.text import slugify
from django.db.utils import IntegrityError
import uuid

def produto_image_path(instance, filename):
    return os.path.join('produtos', instance.slug or str(instance.id), filename)


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=False)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200)
    descricao = models.TextField()
    marca = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    tamanho = models.CharField(max_length=50, blank=True, null=True)
    avaliacao_media = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    quantidade_avaliacoes = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    imagem_principal = models.ImageField(upload_to='./administracao_loja/static/produtos_imagens/', blank=True, null=True)

    slug = models.SlugField(unique=True)
    ml = models.CharField(max_length=5, default='0')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            raise IntegrityError("Nome ou SKU já existe ou ilegível para cadastro")

    def __str__(self):
        return self.nome


class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='imagens/produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"


class Usuario(models.Model):
    imagem_usuario = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    nome = models.CharField(max_length=30, blank=True)
    CPF = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    GENEROS = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outro'),
    ]

    genero = models.CharField(max_length=1, blank=True, choices=GENEROS)
    email = models.EmailField(max_length=254)
    tipo_usuario = models.CharField(max_length=200, default="Comum")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome or self.email



class Endereco(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=200)
    cep = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.nome} - {self.endereco}"


import uuid
import random
import string
from django.db import models

class Pedido(models.Model):

    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('PAGO', 'Pago'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
        ('C', 'Cancelado'),
    ]

    #  Identificador interno seguro
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Número visível pro cliente
    numero_pedido = models.CharField(
        max_length=12,
        unique=True,
        blank=True
    )

    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='pedidos')
    perfumes = models.ManyToManyField('Produto', through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='P')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    endereco_entrega = models.ForeignKey('Endereco', on_delete=models.SET_NULL, null=True)

    def gerar_numero_pedido(self):
        letras = string.ascii_uppercase
        numeros = string.digits
        return 'NL-' + ''.join(random.choices(letras + numeros, k=6))

    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            while True:
                numero = self.gerar_numero_pedido()
                if not Pedido.objects.filter(numero_pedido=numero).exists():
                    self.numero_pedido = numero
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_pedido} - {self.cliente.nome}"

    def calcular_total(self):
        total = sum(item.subtotal() for item in self.itens.all())
        self.valor_total = total
        self.save()
        return total

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    perfume = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.perfume.nome} (Pedido #{self.pedido.id})"


class Notificacao(models.Model):
    hora = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    lida = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificacoes')