from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import IntegrityError

from loja.models import Produto, Categoria, ImagemProduto


class Command(BaseCommand):
    help = "Gera produtos falsos com imagem principal e exatamente 4 imagens extras"

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        # Criar categorias padrão
        categorias_padrao = ['Eletrônicos', 'Roupas', 'Calçados', 'Acessórios', 'Perfumes']
        for nome in categorias_padrao:
            Categoria.objects.get_or_create(
                nome=nome,
                defaults={'slug': slugify(nome)}
            )

        categorias = list(Categoria.objects.all())
        url_imagem = "https://picsum.photos/600"

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

            # Baixar imagem principal
            try:
                img_response = requests.get(url_imagem, timeout=10)
                img_response.raise_for_status()
                imagem_principal = ContentFile(
                    img_response.content,
                    name=f"{slug}-principal.jpg"
                )
            except Exception as e:
                self.stderr.write(f"Erro ao baixar imagem principal: {e}")
                continue

            try:
                produto = Produto.objects.create(
                    nome=nome,
                    subtitulo=subtitulo,
                    descricao=descricao,
                    marca=fake.company(),
                    categoria=random.choice(categorias),
                    preco=preco,
                    preco_promocional=preco_promocional,
                    estoque=random.randint(0, 300),
                    sku=fake.unique.ean(length=8),
                    tamanho=random.choice(["P", "M", "G", "GG", "Único"]),
                    ml=f"{random.randint(30, 1000)}ml",
                    ativo=True,
                    slug=slug,
                    imagem_principal=imagem_principal,
                )
            except IntegrityError as e:
                self.stderr.write(f"Erro ao criar produto {nome}: {e}")
                continue

            # Criar exatamente 4 imagens extras
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
                        f"Erro ao baixar imagem extra {i} para {produto.nome}: {e}"
                    )

        self.stdout.write(
            self.style.SUCCESS("Produtos criados com sucesso (1 imagem principal + 4 extras)!")
        )
