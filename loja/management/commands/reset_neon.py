from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Reseta completamente o banco Neon (DEV ONLY)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("\n🔥 RESETANDO BANCO NEON...\n"))

        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")

        self.stdout.write(self.style.SUCCESS(" Schema recriado"))

        self.stdout.write("\n Rodando migrations...\n")
        call_command("migrate")

        self.stdout.write("\n👤 Criando superuser padrão...\n")

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@admin.com",
                password="123456"
            )
            self.stdout.write(self.style.SUCCESS("Superuser criado"))
        else:
            self.stdout.write(" Superuser já existe")

        self.stdout.write(self.style.SUCCESS("\n BANCO RESETADO COM SUCESSO!\n"))
