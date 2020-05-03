# root = r'D:\Installer\Accounting\Inventoria-Backup-2020-04'
root = r'D:\Installer\Accounting\Cth Inputan Sales 27-04\Inventoria-Backup-2020-04-27'
from pprint import pprint

item1 = 'Name=SY001&Value=28000&CostDigits=0&Price=30000&ValueDigits=0&TaxRate=0&Description=WORTEL&Measure=gram&Category=3&LastUsed=2019-07-11&OrderDate=2019-07-11&LocationsAndQuantities=&Quantity=0.000000&CheckWaringEmail=0&WarnQuantity=0.000000&IdealQuantity=0.000000'
item1 = 'Name=MPR0001&Value=1285553&CostDigits=2&Price=5000000&ValueDigits=2&TaxRate=0&Description=SAYUR%20GUDEG&Measure=PAX&BillOfMaterials=%22SY0029%2F50%22%2C%22SY0006%2F10%22%2C%22SY0007%2F12%22%2C%22BC0001%2F0.20%22%2C%22BK0057%2F5%22%2C%22BK0018%2F25%22%2C%22BK0013%2F5%22%2C%22BC0037%2F20%22%2C%22MY0001%2F0.50%22%2C%22BK0012%2F15%22%2C%22BK0010%2F3%22%2C%22BK0041%2F5%22%2C&LocationsAndQuantities=&Category=12&SubCategory=RECIPE'
# item1 = 'Name=BK0057&Value=1000&CostDigits=2&Price=1000000&ValueDigits=2&TaxRate=0&Description=KEMIRI&Measure=GRAM&Category=9&CheckWaringEmail=0&LocationsAndQuantities=%222%2F750%2F0%2F0%22%2C&Quantity=750.000000&WarnQuantity=0.000000&IdealQuantity=0.000000'
from urllib.parse import urlparse, parse_qsl,parse_qs,unquote
# URL='https://someurl.com/with/query_string?i=main&mode=front&sid=12ab&enc=+Hello'
# parsed_url = urlparse(URL)
# parse_qs(parsed_url.query)
a = parse_qs(item1)
print('a#',a)
a = parse_qsl(item1)
pprint(dict(a))
# print('a#',unquote(item1))

# import urllib
# b= urllib.urlencode(a, True)
# print('b@', b )