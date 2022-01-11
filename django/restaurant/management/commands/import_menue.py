from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from restaurant.models import Category, Menue, Restaraunt, MenueInRestaraunt

import xml.etree.ElementTree as ET

import requests
session = requests.Session()
session.auth = ("www.respublica.bar", "9km#ffm87")

class Command(BaseCommand):
    help = 'Импорт продукции из XML'

    def handle(self, *args, **options):

        xml_interface = "https://195.208.129.244:82/rk7api/v0/xmlinterface.xml"
        request_menu_with_rests = """
        <RK7Query >
            <RK7CMD CMD="GetRefData" RefName="ClassificatorGroups" OnlyActive="1" WithChildItems="2" RefItemIdent="9985" MacroPropTags="1" PropMask="RIChildItems.(
                Ident, 
                GUIDString, 
                Name, 
                CategPath, 
                propTRADEGROUPS, 
                CLASSIFICATORGROUPS^10496, 
                CLASSIFICATORGROUPS^10240, 
                propPRICETYPES, 
                SalesTerms_StartSale, 
                SalesTerms_StopSale, 
                UseStartSale, 
                UseStopSale, 
                genPORTIONWEIGHText, 
                genPORTIONNAMEext, 
                CLASSIFICATORGROUPS^10497)"/>
        </RK7Query>"""
        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass
        response = session.post(xml_interface, data=request_menu_with_rests, verify=False)

        categories = {}
        for category in Category.objects.all():
            categories[category.name] = category.id
        
        print(response.content.decode('utf8'))
        root = ET.fromstring(response.content.decode('utf8'))
        # root = tree.getroot()
        for item in root.iter('TRK7MenuItem'):
            for property in item.find('PropTRADEGROUPS').iter('Property'):
                # print(property.get('Ident'), property.get('Value'))
                name = item.get('Name')
                if(len(item.get('CategPath').split('Меню')) > 1):
                    categPath = item.get('CategPath').split("\\")[1:]
                    parent = None
                    for path in categPath:
                        if(path not in categories):
                            category_find = Category.objects.filter(name=path)
                            if(category_find.exists()):
                                parent = category_find.first().id
                            else:
                                category_created = Category.objects.create(name=path, parent=parent)
                                parent = category_created.id
                            categories[path] = parent

        # menues = []
        # for menue in Menue.objects.all():
        #     menues.append(menue.dish)

        self.stdout.write("Категории: %s" % self.style.NOTICE(categories))


        n = 0
        for item in root.iter('TRK7MenuItem'):
            name = item.get('Name')
            print(name)
            prices = {}
            if(len(item.get('CategPath').split('Меню')) > 1):
                category = item.get('CategPath').split("\\")[-1]

            for price in item.find('PropPRICETYPES').iter('Property'):
                prices[price.get('Ident')] = float(price.get('Value')) / 100

            for property in item.find('PropTRADEGROUPS').iter('Property'):
                # print(property.get('Ident'), property.get('Value'))
                if(category in categories):
                    # print(name)
                    # print(categories[category])
                    # if(name not in menues):
                    weight = f"{item.get('genPORTIONWEIGHText')}"
                    is_drink = None
                    if item.get('genPORTIONNAMEext') == "г":
                        is_drink = False
                    if item.get('genPORTIONNAMEext') == "мл":
                        is_drink = True

                    try:
                        menue = Menue.objects.get(ident=item.get('Ident'))
                    except Menue.DoesNotExist:
                        menue = Menue.objects.create(
                                    dish=name, category_id=categories[category], ident=item.get('Ident'), weight=weight, is_drink=is_drink)
                    try:
                        restaraunt = Restaraunt.objects.get(ident=property.get('Ident'))
                        menue_in_restaraunt = MenueInRestaraunt.objects.filter(restaraunt=restaraunt, menue=menue)
                        price = prices[restaraunt.price_ident]
                        if price == 9223372036854775807:
                            price = -1
                        if(menue_in_restaraunt.exists()):
                            print("!")
                            menue_in_restaraunt.update(price=prices[restaraunt.price_ident])
                            menue.weight=weight
                            menue.is_drink=is_drink
                            menue.save()
                        else:
                            print("?")
                            MenueInRestaraunt.objects.create(restaraunt=restaraunt, menue=menue, price=prices[restaraunt.price_ident])
                            n += 1
                    except Restaraunt.DoesNotExist:
                        print(property.get('Ident'), "not exist")
                    except ValueError:
                        print("erro")

        # self.stdout.write(self.style.SUCCESS('Successfully import "%s"' % n))
