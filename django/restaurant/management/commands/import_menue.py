from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from restaurant.models import Category, Menue

import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = 'Импорт продукции из XML'

    def handle(self, *args, **options):
        categories = {}
        for category in Category.objects.all():
            categories[category.name] = category.id

        menues = []
        for menue in Menue.objects.all():
            menues.append(menue.dish)

        self.stdout.write("Категории: %s" % self.style.NOTICE(categories))

        tree = ET.parse(settings.BASE_DIR / 'stuff' / 'menu.XML')
        root = tree.getroot()

        n = 0
        for item in root.iter('Item'):
            name = item.get('Name')
            if(len(item.get('CategPath').split('Меню')) > 1 and (item.get('ActiveHierarchy') == 'true') and (item.get('Status') == 'rsActive')):
                category = item.get('CategPath').split("\\")[-1]
                print(category)
                if(category in categories):
                    # print(name)
                    # print(categories[category])
                    if(name not in menues):
                        Menue.objects.create(
                            dish=name, category_id=categories[category], restaraunt_id=1, ident=item.get('ItemIdent'))
                        n += 1

        self.stdout.write(self.style.SUCCESS('Successfully import "%s"' % n))
