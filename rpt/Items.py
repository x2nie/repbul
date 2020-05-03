from Categories import dats as cats
from dat import load_dats

def getCategoryName(id):
    for cat in cats:
        if cat['id'] == id:
            return cat['Name']

def getCategory(id):
    for cat in cats:
        if cat['id'] == id:
            return cat

def onrow(d):
    # d['CategoryName'] = getCategoryName(d['Category'])
    d['Description'] = d['Description'].strip()
    cat = getCategory(d['Category'])
    d['CategoryName'] = cat['Name']
    d['Subcategory'] = cat.get('Subcategory')
    Price = d['Price']
    frix = int(d['CostDigits'])*-1
    d['Price'] = float(Price[:frix]+'.'+Price[frix:])
    if d.get('Quantity'):
        d['Quantity'] = float(d['Quantity'])
    
    Value = d['Value']
    frix = int(d['ValueDigits'])*-1
    d['Value'] = float(Value[:frix]+'.'+Value[frix:])
    BoM = []
    if d.get('BillOfMaterials'):  #  {'BillOfMaterials': '"SY0031/1","SY0064/1","PK0015/1",',
        p = d['BillOfMaterials']
        a = p.strip(',').replace('"','').split(',')
        for q in a:
            BoM.append(q.split('/'))
    d['BoM'] = BoM  # [ [SY0031,'1'], ['SY0064','1'] ]
        
        
dats = load_dats('Items', onrow)

def getItemByName(name):
    for item in dats:
        if item['Name'] == name:
            return item

def getItemById(id):
    for item in dats:
        if item['id'] == id:
            return item

if __name__ == "__main__":
    # print(dats)
    import pprint
    pprint.pprint([d for d in dats if d.get('BillOfMaterials')])