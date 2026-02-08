from django.core.management.base import BaseCommand
from faker import Faker
import random
from loja.models import Usuario, Endereco


class Command(BaseCommand):
    help = "Gera usuários falsos para testes usando Faker"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")

        generos = ["M", "F", "O"]

        for _ in range(15):
            usuario = Usuario.objects.create(
                nome=fake.name(),
                CPF=fake.cpf(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=70),
                telefone=fake.phone_number(),
                genero=random.choice(generos),
                email=fake.unique.email(),
            )

            Endereco.objects.create(
                user=usuario,
                endereco=fake.street_address(),
                cep=fake.postcode()
            )

        self.stdout.write(
            self.style.SUCCESS("Usuários de teste criados com sucesso!")
        )
