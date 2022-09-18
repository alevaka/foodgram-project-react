import csv
import json

from django.core.management.base import BaseCommand
from django.db import models
from recipes.models import Ingredient


def importjson2db(model: models.Model, json_file: str):
    """Импортирует из файла json_file в базу модели model
    """
    with open(json_file, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
        for item in data:
            try:
                model.objects.create(**item)
            except Exception as err1:
                print(f'Ошибка импорта файла {jsonfile}, элемент {item}')
                print(err1)


def importcsv2db(model: models.Model, csv_file: str, field_list: list):
    """Импортирует из файла csv_file в базу модели model
    в field_list - список с именем полей.
    """

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        row_number = 0
        for row in csvreader:
            if row[0] != 'id':
                try:
                    print(dict(zip(field_list, row)))
                    model.objects.create(**dict(zip(field_list, row)))
                except Exception as err1:
                    print(f'Ошибка импорта строки {row_number}')
                    print(err1)
            row_number += 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        importjson2db(
            Ingredient,
            '..//data//ingredients.json'
        )
