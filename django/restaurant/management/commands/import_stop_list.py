from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from restaurant.models import Category, Menue, Restaraunt, MenueInRestaraunt

import xml.etree.ElementTree as ET

import requests
session = requests.Session()
# session.auth = ("www.respublica.bar", "9km#ffm87")

class Command(BaseCommand):
    help = 'Импорт стоп листов из XML'
    def handle(self, *args, **options):
        request_data = """
        <?xml version="1.0" encoding="utf-8"?>
        <RK7Query>
        <RK7CMD CMD="GetDishRests"/>
        </RK7Query>"""
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass
       
       

        for restaraunt in Restaraunt.objects.all():
            session.auth = (restaraunt.r_keeper, restaraunt.r_keeper_pass)
            xml_interface = f"https://{restaraunt.r_keeper_ip}/rk7api/v0/xmlinterface.xml"
            response = session.post(xml_interface, data=request_data, verify=False)
            root = ET.fromstring(response.content.decode('utf8'))
            for rest in root.iter('DishRest'):
                try:
                    menue = Menue.objects.get(ident=rest.get('id'))
                    menue_in_restaraunt = MenueInRestaraunt.objects.get(menue=menue)
                    menue_in_restaraunt.stop_list = False
                    if(rest.get('prohibited') is not None):
                        menue_in_restaraunt.stop_list = True
                    menue_in_restaraunt.save()
                except (Menue.DoesNotExist, MenueInRestaraunt.DoesNotExist):
                    print(rest.get('id'), "Not exists in Menue")