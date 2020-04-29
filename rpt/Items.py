from dat import load_dats

def onrow(d):
    BoM = []
    if d.get('BillOfMaterials'):  #  {'BillOfMaterials': '"SY0031/1","SY0064/1","PK0015/1",',
        p = d['BillOfMaterials']
        a = p.strip(',').replace('"','').split(',')
        for q in a:
            BoM.append(q.split('/'))
    d['BoM'] = BoM  # [ [SY0031,'1'], ['SY0064','1'] ]
        
        
dats = load_dats('Items', onrow)



if __name__ == "__main__":
    # print(dats)
    import pprint
    pprint.pprint([d for d in dats if d.get('BillOfMaterials')])