from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify

from loja.models import Produto, Categoria, ImagemProduto


class Command(BaseCommand):
    help = "Gera produtos falsos com imagem principal e exatamente 4 imagens extras"

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        # Criar categorias padrão
        categorias_padrao = ['Eletrônicos', 'Roupas', 'Calçados', 'Acessórios', 'Perfumes']
        for nome in categorias_padrao:
            Categoria.objects.get_or_create(nome=nome, defaults={'slug': slugify(nome)})

        categorias = list(Categoria.objects.all())

        url_imagem = "https://picsum.photos/600"

        for _ in range(15):  # Criar 15 produtos
            nome = fake.word().capitalize() + " " + fake.word().capitalize()
            preco = round(random.uniform(20, 800), 2)
            preco_promocional = round(preco * random.choice([1, 0.9, 0.8]), 2)

            slug = slugify(nome)

            # Baixar imagem principal
            try:
                img_response = requests.get(url_imagem)
                imagem_principal_file = ContentFile(img_response.content, name=f"{slug}-principal.jpg")
            except Exception as e:
                print("Erro ao baixar imagem principal:", e)
                continue  # Sem imagem principal, não cria o produto

            # Criar produto com imagem principal
            produto = Produto.objects.create(
                nome=nome,
                descricao=fake.text(200),
                marca=fake.company(),
                categoria=random.choice(categorias),
                preco=preco,
                preco_promocional=preco_promocional,
                estoque=random.randint(0, 300),
                sku=fake.unique.ean(length=8),
                slug=slug,
                ativo=True,
                tamanho=random.choice(["P", "M", "G", "GG", "Único", None]),
                ml=f"{random.randint(30, 1000)}ml",
                imagem_principal=imagem_principal_file,
            )

            # Criar exatamente 4 imagens extras
            for i in range(4):
                try:
                    response = requests.get(url_imagem)
                    imagem_file = ContentFile(response.content, name=f"{produto.slug}-extra-{i}.jpg")

                    ImagemProduto.objects.create(
                        produto=produto,
                        imagem=imagem_file
                    )
                except Exception as e:
                    print(f"Erro ao baixar imagem extra {i} para {produto.nome}: {e}")

        self.stdout.write(self.style.SUCCESS("Produtos criados com 1 imagem principal e 4 extras!"))
