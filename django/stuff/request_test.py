import requests
session = requests.Session()
session.auth = ("www.bardoski.ru", "24dc9c14c74255560ad7f4e4438523b4")

xml_interface = "https://188.235.2.92:82/rk7api/v0/xmlinterface.xml"


request_data = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetDishRests"/></RK7Query>"""
request_menu = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetRefData" RefName="MenuItems"/></RK7Query>"""
request_price = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetRefData" RefName="PRICES"/></RK7Query>"""
request_menu_with_rests = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetRefData" RefName="ClassificatorGroups" OnlyActive="1" WithChildItems="2" RefItemIdent="9985" MacroPropTags="1" PropMask="RIChildItems.(Ident, GUIDString, Name, CategPath, propTRADEGROUPS, propPRICETYPES, SalesTerms_StartSale, SalesTerms_StopSale, UseStartSale, UseStopSale)" /></RK7Query>"""


headers = {'Content-Type': 'application/xml'}
response = session.post(xml_interface, data=request_menu_with_rests, verify=False)

print(response.content.decode('utf8'))

f = open("menu.XML", "a", encoding="utf-8")
f.write(response.content.decode('utf8'))
f.close()