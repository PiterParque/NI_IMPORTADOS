from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection


class Command(BaseCommand):
    help = "Apaga TODOS os registros do banco (TRUNCATE CASCADE)"

    def handle(self, *args, **options):

        confirmacao = input(
            "⚠️ Isso vai APAGAR TODOS os dados do banco. Digite 'SIM' para continuar: "
        )

        if confirmacao != "SIM":
            self.stdout.write(self.style.WARNING("Operação cancelada."))
            return

        models = apps.get_models()

        tabelas = []
        for model in models:
            tabelas.append(model._meta.db_table)

        with connection.cursor() as cursor:
            cursor.execute(
                "TRUNCATE TABLE {} RESTART IDENTITY CASCADE;".format(
                    ", ".join(tabelas)
                )
            )

        self.stdout.write(
            self.style.SUCCESS(" Banco limpo com sucesso (TRUNCATE CASCADE)!")
        )
