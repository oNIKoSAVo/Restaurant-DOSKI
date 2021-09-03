from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from restaurant.models import Category

import xml.etree.ElementTree as ET

class Command(BaseCommand):
    help = 'Импорт категорий из XML'

    def handle(self, *args, **options):
        tree = ET.parse(settings.BASE_DIR / 'stuff' / 'menu.XML')
        root = tree.getroot()
        for item in root.iter('Item'):
            name = item.get('Name')
            if(len(item.get('CategPath').split('Меню')) > 1):
                categPath = item.get('CategPath').split("\\")[1:]

                parent = None
                for path in categPath:
                    category = Category.objects.filter(name=path)
                    if(category.exists()):
                        parent = category.first().id
                    else:
                        category = Category.objects.create(name=path, parent=parent)
                        parent = category.id