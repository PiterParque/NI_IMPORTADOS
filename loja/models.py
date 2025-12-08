import os
from django.db import models
from django.utils.text import slugify
from django.db.utils import IntegrityError


# CAMINHO PARA AS IMAGENS DO PRODUTO (recomendado)
def produto_image_path(instance, filename):
    return os.path.join('produtos', instance.slug or str(instance.id), filename)


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=False)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=200)
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
    imagem_principal = models.ImageField(upload_to='produtos_imagens/', blank=True, null=True)

    slug = models.SlugField(unique=True)
    ml = models.CharField(max_length=5, default='0')

    def save(self, *args, **kwargs):
        try:
            if not self.slug:
                self.slug = slugify(self.nome)
            super().save(*args, **kwargs)
        except  IntegrityError:
            return "Nome ja existe ou ilegivel para cadasstro"

    def __str__(self):
        return self.nome
class ImagemProduto(models.Model):
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.CASCADE, 
        related_name='imagens'
    )
    imagem = models.ImageField(upload_to='imagens/produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"



class Usuario(models.Model):
    imagem_usuario = models.ImageField(
        upload_to='usuarios/',
        null=True,
        blank=True
    )

    nome = models.CharField(max_length=30)
    senha = models.CharField(max_length=128)
    CPF = models.CharField(max_length=15)
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=15)
    genero = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    tipo_usuario = models.CharField(max_length=200, default="Comum")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} <{self.email}>"


class Endereco(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    endereco = models.CharField(max_length=200)
    cep = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.nome} - {self.endereco}"


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('PAGO', 'Pago'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
        ('C', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')
    perfumes = models.ManyToManyField(Produto, through='ItemPedido')
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='P')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome}"

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
