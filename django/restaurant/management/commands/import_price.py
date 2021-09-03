from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from restaurant.models import Category, Menue

import xml.etree.ElementTree as ET

class Command(BaseCommand):
    help = 'Импорт цен к продуктам из XML'

    def handle(self, *args, **options):
        tree = ET.parse(settings.BASE_DIR / 'stuff' / 'price.XML')
        root = tree.getroot()
        n = 0
        for item in root.iter('Item'):
            price = int(item.get('Value')) / 100
            if(Menue.objects.filter(ident=item.get('ObjectID')).update(price=price) != 0):
                n += 1

        self.stdout.write(self.style.SUCCESS('Successfully import "%s"' % n))