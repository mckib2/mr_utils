from mr_utils.load_data import load_mat

def mat_keys(filename,ignore_dbl_underscored=True,no_print=False):
    '''Give the keys found in a .mat file.

    filename -- .mat filename.
    ignore_dbl_underscored -- Remove keys beginng with two underscores.
    '''

    data = load_mat(filename)
    keys = list(data.keys())

    if ignore_dbl_underscored:
        keys = [ x for x in keys if not x.startswith('__') ]

    if not no_print:
        print('Keys: ',keys)
        
    return(keys)

if __name__ == '__main__':
    pass
