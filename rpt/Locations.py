from dat import load_dats

       
        
dats = load_dats('Locations')

def getLocationById(id):
    for item in dats:
        if item['id'] == id:
            return item

if __name__ == "__main__":
    # print(dats)
    import pprint
    pprint.pprint([d for d in dats ])