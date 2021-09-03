import requests
session = requests.Session()
session.auth = ("www.respublica.bar", "9km#ffm87")

xml_interface = "https://195.208.129.244:82/rk7api/v0/xmlinterface.xml"


request_data = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetDishRests"/></RK7Query>"""
request_menu = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetRefData" RefName="MenuItems"/></RK7Query>"""
request_price = """<?xml version="1.0" encoding="utf-8"?><RK7Query><RK7CMD CMD="GetRefData" RefName="PRICES"/></RK7Query>"""

headers = {'Content-Type': 'application/xml'}
response = session.post(xml_interface, data=request_price, verify=False)

print(response.content.decode('utf8'))

f = open("price.xml", "a", encoding="utf-8")
f.write(response.content.decode('utf8'))
f.close()