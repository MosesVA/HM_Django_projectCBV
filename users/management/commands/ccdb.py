from django.core.management import BaseCommand
import pyodbc
from config.settings import DATABASE, USER, PASSWORD, HOST


class Command(BaseCommand):
    connectionString = f'''DRIVER={{ODBC Driver 17 for SQL Server}};
                           SERVER={HOST};
                           DATABASE=Academy;
                           UID={USER};
                           PWD={PASSWORD}'''
    try:
        conn = pyodbc.connect(connectionString)
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
