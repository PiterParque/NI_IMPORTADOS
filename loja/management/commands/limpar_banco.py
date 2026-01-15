from django.core.management.base import BaseCommand
from loja.models import (
    Notificacao, ItemPedido, Pedido, Endereco,
    Usuario, ImagemProduto, Produto, Categoria
)
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = 'Apaga TODOS os registros do banco'

    def handle(self, *args, **options):
        # Deletar registros dependentes de Allauth primeiro
        EmailAddress.objects.all().delete()

        # Depois apagar suas tabelas
        Notificacao.objects.all().delete()
        ItemPedido.objects.all().delete()
        Pedido.objects.all().delete()
        Endereco.objects.all().delete()
        ImagemProduto.objects.all().delete()
        Produto.objects.all().delete()
        Categoria.objects.all().delete()
        Usuario.objects.all().delete()
        
        # Por último, apagar usuários
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            'Todos os registros foram apagados com sucesso!'
        ))
