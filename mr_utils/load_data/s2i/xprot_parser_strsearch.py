'''Quick and lazy -- only read what we need from the XProtocol header.

This is a way engineered to Get the Job Done(TM).  It could be made a lot
better and faster, but right now I'm just trying to get it working after the
debacle with ply...

The lookup table seems like a good idea, but having a little trouble getting it
to work properly.  Currently it's supressing a lot of fields that don't exist,
it's just not letting us display the warning that it doesn't exist.
'''

from itertools import islice

import numpy as np

def findp(p, config):
    '''Decode the tag and return index.

    p -- Current path node.
    config -- The current header portion we're searching in.

    All of these tag assignments are ad hoc -- just to get something to work.
    '''
    if p in ['MEAS', 'YAPS', 'HEADER', 'IRIS', 'DERIVED', 'DICOM',
             'RECOMPOSE', ''] or p[:1] in ['s']:
        tag = 'ParamMap'
    elif p[:2] in ['as'] or p in ['aRxCoilSelectData']:
        tag = 'ParamArray'
    elif (p[:2] in ['al', 'uc', 'ai']) or (p[:1] in ['i', 'l', 'n']) or \
            p in ['ImageColumns', 'ImageLines', 'MeasUID', 'ReconMeasDependencies']:
        tag = 'ParamLong'
    elif (p[:3] in ['afl']) or (p[:2] in ['ad', 'fl']) or (p[:1] in ['d']) or \
            p in ['phaseOversampling']:
        tag = 'ParamDouble'
    elif (p[:1] in ['t']) or p in [
            'PatientID', 'PatientLOID', 'PatientBirthDay',
            'DeviceSerialNumber', 'StudyLOID', 'Manufacturer',
            'ManufacturersModelName', 'InstitutionName', 'Modality']:
        tag = 'ParamString'
    else:
        msg = '"%s" is not handled yet!' % p
        raise NotImplementedError(msg)

    idx0 = config.find('<' + tag + '."' + p + '">')
    idx0 -= len('<' + tag + '."')
    return(idx0, tag)

def find_matching_braces(s, lsym='{', rsym='}', qlsym='"', qrsym='"'):
    '''Given string s, find indices of matching braces.
    '''
    matches = {}
    pstack = []

    it = iter(enumerate(s))
    for ii, c in it:

        # Skip comments (denoted by qlsym COMMENT qrsym)
        if c == qlsym:
            idx = s[ii+1:].find(qrsym) + 1
            islice(it, idx+1, idx+1)

        if c == lsym:
            pstack.append(ii)
        elif c == rsym:
            if not pstack:
                raise IndexError('No matching closing parens at: ' + str(ii))
                # matches[0] = ii
                # break
            matches[pstack.pop()] = ii

    if pstack:
        raise IndexError('No matching opening parens at: ' + str(pstack.pop()))

    return matches


def xprot_get_val(config_buffer, val, p_to_buf_table=None, return_table=False):
    '''Get value from config buffer.

    config_buffer -- String containing the XProtocol innards.
    val -- Dot separated path to search for.
    p_to_buf_table --
    return_table --
    '''

    if p_to_buf_table is None:
        p_to_buf_table = dict()
    else:
        p_to_buf_table = p_to_buf_table.copy()

    # Split the path
    path = val.split('.')

    # See if there's already entries in the table to help you find the specific
    # region we're looking for.  We want to find the longest path in the table.
    lpath = len(path)
    for ii in range(lpath):
        if ii == 0:
            key = val
        else:
            key = '.'.join(path[:-ii])
        if key in p_to_buf_table:
             # truncate the buffer to what we don't know
            config_buffer = p_to_buf_table[key]

            # only need end elements of the path
            path = path[ii+1:]
            if not path:
                path = val.split('.')[ii:]

            # print(path)
            break


    # For each path element, thin the possible config region to look in
    cur_buf = config_buffer
    write_table = True
    for ii, p in enumerate(path):

        # Key for the lookup table
        key = '.'.join(path[:-ii-1])

        # I don't know how to deal with indices currently, so we're ignoring
        # them.  Think this may be pointing to the XProtocol section where they
        # assign <Default>s and then dump the actual values afterwards in an
        # ugly fashion:
        # { { { # } }, { # } }, etc...
        # We are missing dReadout, etc, so this may be the case.
        if p.isnumeric():
            write_table = False
            # print('SKIPPING NUMERIC %s' % p)
            # raise NotImplementedError()
            continue

        idx0, tag = findp(p, cur_buf)
        if idx0 < 0:
            # Update table -- this will never be a good answer
            if write_table:
                p_to_buf_table[key] = ''

            msg = '%s not found!' % p
            raise KeyError(msg)

        # Update the table
        if write_table and key not in p_to_buf_table:
            p_to_buf_table[key] = cur_buf

        # Match braces
        matches = find_matching_braces(cur_buf)

        # Find the first opening brace after this point
        idx1 = cur_buf[idx0:].find('{')
        idx2 = idx0 + idx1
        cur_buf = cur_buf[idx2:matches[idx2]+1]


    # Chop off front and end braces and then cast to correct value
    cur_buf = cur_buf[1:-1]
    if tag == 'ParamLong':
        val = np.fromstring(cur_buf, dtype=int, sep=' ')
    elif tag == 'ParamDouble':
        # There's a precision tag that needs to be removed
        cur_buf = cur_buf.replace('<Precision> 6', '')
        val = np.fromstring(cur_buf, dtype=float, sep=' ')
    elif tag == 'ParamString':
        # Take care of empty space and hone into quotiation marks
        idx0 = cur_buf.find('"')
        idx1 = cur_buf.rfind('"')
        cur_buf = cur_buf[idx0+1:idx1]
        val = cur_buf.strip()

    if return_table:
        # print('VAL:', val)
        return val, p_to_buf_table
    return val

if __name__ == '__main__':
    pass
