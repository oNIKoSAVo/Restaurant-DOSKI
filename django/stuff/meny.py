import xml.etree.ElementTree as ET

tree = ET.parse('menu.XML')
root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)

n = 0

for item in root.iter('Item'):
    # print(item.attrib)
    print(item.get('Name'))
    print(item.get('CategPath').split('Меню'))
    n = n+1

print(n)