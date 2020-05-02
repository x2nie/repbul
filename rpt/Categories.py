from dat import load_dats

       
        
dats = load_dats('Categories')



if __name__ == "__main__":
    # print(dats)
    import pprint
    pprint.pprint([d for d in dats ])