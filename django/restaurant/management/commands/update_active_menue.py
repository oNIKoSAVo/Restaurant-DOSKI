import traceback
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from restaurant.models import Category, Menue, Restaraunt

import xml.etree.ElementTree as ET
import requests

session = requests.Session()
session.auth = ("www.respublica.bar", "9km#ffm87")


class Command(BaseCommand):
    help = 'Скрытие не активных товаров в меню'

    def handle(self, *args, **options):
        request_menu = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetRefData" RefName="MenuItems"/></RK7Query>"""

        menues_pull = []
        for restaraunt in Restaraunt.objects.all():
            if restaraunt.r_keeper is None:
                continue
            try:
                response = session.post(
                    f"https://{restaraunt.r_keeper}/rk7api/v0/xmlinterface.xml", data=request_menu, verify=False)
                response = response.content.decode('utf8')

                root = ET.fromstring(response)

                for item in root.iter('Item'):
                    if(item.get('ItemIdent') not in menues_pull):
                        menues_pull.append(item.get('ItemIdent'))
            except Exception:
                print(traceback.format_exc())

        if len(menues_pull) > 0:
            menues_hidde = Menue.objects.exclude(
                ident__in=menues_pull).update(active=False)
            menues_show = Menue.objects.filter(
                ident__in=menues_pull).update(active=True)

        self.stdout.write(self.style.SUCCESS(
            'Successfully hide "%s"' % menues_hidde))
        self.stdout.write(self.style.SUCCESS(
            'Successfully show "%s"' % menues_show))
