from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import IntegrityError

from loja.models import Produto, Categoria, ImagemProduto, Marcas, Tamanhos


class Command(BaseCommand):
    help = "Gera produtos falsos com imagem principal e 4 imagens extras"

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        # -------------------------
        # Criar categorias
        # -------------------------
        categorias_padrao = ['Eletrônicos', 'Roupas', 'Calçados', 'Acessórios', 'Perfumes']

        for nome in categorias_padrao:
            Categoria.objects.get_or_create(
                nome=nome,
                defaults={'slug': slugify(nome)}
            )

        categorias = list(Categoria.objects.all())

        # -------------------------
        # Criar marcas
        # -------------------------
        marcas_padrao = ['Nike', 'Adidas', 'Puma', 'Gucci', 'Chanel']

        for nome in marcas_padrao:
            Marcas.objects.get_or_create(
                nome=nome,
                defaults={'slug': slugify(nome)}
            )

        marcas = list(Marcas.objects.all())

        # -------------------------
        # Criar tamanhos
        # -------------------------
        tamanhos_padrao = ['P', 'M', 'G', 'GG', 'Único']

        for nome in tamanhos_padrao:
            Tamanhos.objects.get_or_create(
                nome=nome,
                defaults={'slug': slugify(nome)}
            )

        tamanhos = list(Tamanhos.objects.all())

        url_imagem = "https://picsum.photos/600"

        # -------------------------
        # Criar produtos
        # -------------------------
        for _ in range(15):

            nome = f"{fake.word().capitalize()} {fake.word().capitalize()}"
            subtitulo = fake.sentence(nb_words=6)
            descricao = fake.text(max_nb_chars=300)

            preco = round(random.uniform(50, 800), 2)
            desconto = random.choice([0, 0.1, 0.2])
            preco_promocional = round(preco * (1 - desconto), 2) if desconto else None

            base_slug = slugify(nome)
            slug = base_slug
            contador = 1

            while Produto.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1

            # baixar imagem principal
            try:
                img_response = requests.get(url_imagem, timeout=10)
                img_response.raise_for_status()

                imagem_principal = ContentFile(
                    img_response.content,
                    name=f"{slug}-principal.jpg"
                )

            except Exception as e:
                self.stderr.write(f"Erro ao baixar imagem: {e}")
                continue

            try:
                produto = Produto.objects.create(
                    nome=nome,
                    subtitulo=subtitulo,
                    descricao=descricao,
                    marca=random.choice(marcas),
                    categoria=random.choice(categorias),
                    preco=preco,
                    preco_promocional=preco_promocional,
                    estoque=random.randint(0, 300),
                    sku=fake.unique.ean(length=8),
                    tamanho=random.choice(tamanhos),
                    ml=str(random.randint(30, 200)),
                    ativo=True,
                    slug=slug,
                    imagem_principal=imagem_principal,
                )

            except IntegrityError as e:
                self.stderr.write(f"Erro ao criar produto: {e}")
                continue

            # -------------------------
            # 4 imagens extras
            # -------------------------
            for i in range(4):

                try:
                    response = requests.get(url_imagem, timeout=10)
                    response.raise_for_status()

                    imagem_extra = ContentFile(
                        response.content,
                        name=f"{slug}-extra-{i}.jpg"
                    )

                    ImagemProduto.objects.create(
                        produto=produto,
                        imagem=imagem_extra
                    )

                except Exception as e:
                    self.stderr.write(
                        f"Erro ao baixar imagem extra: {e}"
                    )

        self.stdout.write(
            self.style.SUCCESS("Produtos criados com sucesso!")
        )