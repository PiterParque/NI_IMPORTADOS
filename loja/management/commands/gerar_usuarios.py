from django.core.management.base import BaseCommand
from faker import Faker
import random
from loja.models import Usuario, enderecos
from django.utils import timezone


class Command(BaseCommand):
    help = "Gera usuários falsos para testes usando Faker"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")

        generos = ["Masculino", "Feminino", "Outro"]

        for _ in range(15):  # quantidade de usuários
            nome = fake.name()
            email = fake.unique.email()
            cpf = fake.ssn()
            telefone = fake.phone_number()
            genero = random.choice(generos)
            data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=70)

            usuario = Usuario.objects.create(
                nome=nome,
                senha=fake.password(length=12),
                CPF=cpf,
                data_nascimento=timezone.make_aware(fake.date_time_between(start_date='-70y')),
                telefone=telefone,
                genero=genero,
                email=email,
            )

            # Criar endereço do usuário
            enderecos.objects.create(
                user=usuario,
                endereco=fake.address(),
                cep=fake.postcode()
            )

        self.stdout.write(self.style.SUCCESS("Usuários de teste criados com sucesso!"))
