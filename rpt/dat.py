__all__ = ['load_dats']

import os
from os import listdir
from os.path import isfile, join
from urllib.parse import urlparse, parse_qsl,parse_qs,unquote
from pprint import pprint

def _donothing(data):
    pass

def load_dats(folder, onrow=None):
    "It simply load all *.dat inside folder and return as list of dict"
    
    from config import data_dir
    dats_dir = os.path.join(data_dir, folder)
    # fpath = os.path.join(data_dir, folder, '1.dat')
    # print( fpath )
    # onlyfiles = [f for f in listdir(dats_dir) if isfile(join(dats_dir, f))]
    # dat_files = [join(dats_dir, f) for f in listdir(dats_dir) if isfile(join(dats_dir, f)) if f.endswith('.dat')]
    dat_files = [f for f in listdir(dats_dir) if isfile(join(dats_dir, f)) if f.endswith('.dat')]
    # print(dat_files)
    
    data = []
    ids = {}
    for dat_file in dat_files:
        print( 'loading',folder,':',dat_file )
        with open(join(dats_dir, dat_file), 'r') as f: 
            row = f.read()
        # print( row )

        o = dict(parse_qsl(row))
        o['id'] = _id = dat_file[:-4] # got '123' from '123.dat'
        ids[_id] = len(data)
        if onrow:
            onrow(o)
        data.append(o)
        
        # if len(data) > 15:
        #     break #limit dev
        # print(o)
    # pprint(data)
    # pprint([d for d in data if d.get('BillOfMaterials')])
    return data
    
    
if __name__ == "__main__":
    load_dats('items')