import random
from django.core.management.base import BaseCommand
from loja.models import Usuario, Produto, Pedido, ItemPedido, Endereco


class Command(BaseCommand):
    help = "Gera um pedido aleatório usando dados do banco"

    def handle(self, *args, **kwargs):

        usuario = Usuario.objects.order_by('?').first()

        if not usuario:
            self.stdout.write(self.style.ERROR("Nenhum usuário encontrado"))
            return

        endereco = Endereco.objects.filter(user=usuario).first()

        if not endereco:
            self.stdout.write(self.style.ERROR("Usuário não possui endereço"))
            return

        produtos = list(Produto.objects.filter(ativo=True))

        if not produtos:
            self.stdout.write(self.style.ERROR("Nenhum produto encontrado"))
            return

        pedido = Pedido.objects.create(
            cliente=usuario,
            endereco_entrega=endereco
        )

        quantidade_itens = random.randint(1, 3)

        for produto in random.sample(produtos, min(len(produtos), quantidade_itens)):
            quantidade = random.randint(1, 2)

            ItemPedido.objects.create(
                pedido=pedido,
                perfume=produto,
                quantidade=quantidade,
                preco_unitario=produto.preco_promocional or produto.preco
            )

        pedido.calcular_total()

        self.stdout.write(
            self.style.SUCCESS(
                f"Pedido {pedido.numero_pedido} criado para {usuario.nome}"
            )
        )
