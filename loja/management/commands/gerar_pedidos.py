# arquivo: loja/management/commands/gerar_pedidos.py
from django.core.management.base import BaseCommand
from faker import Faker
import random

from loja.models import Produto, Usuario, Endereco, Pedido, ItemPedido

class Command(BaseCommand):
    help = "Gera pedidos falsos para usuários existentes"

    def handle(self, *args, **kwargs):
        fake = Faker('pt_BR')

        usuarios = list(Usuario.objects.all())
        produtos = list(Produto.objects.filter(ativo=True, estoque__gt=0))
        enderecos = list(Endereco.objects.all())

        if not usuarios or not produtos or not enderecos:
            self.stderr.write("É necessário ter usuários, produtos e endereços cadastrados.")
            return

        # Quantidade de pedidos falsos a criar
        num_pedidos = 10

        for _ in range(num_pedidos):
            usuario = random.choice(usuarios)
            # Escolhe um endereço do usuário
            endereco_usuario = Endereco.objects.filter(user=usuario).first()
            if not endereco_usuario:
                continue  # pular se usuário não tiver endereço

            # Cria pedido
            pedido = Pedido.objects.create(
                cliente=usuario,
                endereco_entrega=endereco_usuario,
                metodo_pagamento=random.choice(['pix', 'cartao', 'boleto']),
                status=random.choice(['P', 'PAGO', 'E', 'F', 'C']),
            )

            # Escolher de 1 a 5 produtos aleatórios para o pedido
            itens_pedido = random.sample(produtos, k=random.randint(1, 5))
            total = 0

            for produto in itens_pedido:
                quantidade = random.randint(1, 3)
                preco_unitario = float(produto.preco_promocional or produto.preco)

                ItemPedido.objects.create(
                    pedido=pedido,
                    perfume=produto,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario
                )

                total += preco_unitario * quantidade

            pedido.valor_total = total
            pedido.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Pedido {pedido.numero_pedido} criado para {usuario.nome or usuario.email} - Total: R${total:.2f}"
                )
            )

        self.stdout.write(self.style.SUCCESS("Pedidos falsos gerados com sucesso!"))