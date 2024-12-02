import pyodbc

from django.core.management import BaseCommand

from config.settings import DATABASE, USER, PASSWORD, HOST, PAD_DATABASE, DRIVER


class Command(BaseCommand):
    """Создание БД"""

    def handle(self, *args, **options):
        ConnectionString = f'''DRIVER={DRIVER};
                               SERVER={HOST};
                               DATABASE={PAD_DATABASE};
                               UID={USER};
                               PWD={PASSWORD}'''
        try:
            conn = pyodbc.connect(ConnectionString)
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            conn.autocommit = True
            try:
                conn.execute(fr'CREATE DATABASE {DATABASE};')
            except pyodbc.ProgrammingError as ex:
                print(ex)
            else:
                print(f'База данных {DATABASE} успешно создана!')
