'''ProcessParameterMap'''

import xml.etree.ElementTree as ET
import logging
import operator
from functools import reduce

import numpy as np
import xmltodict
from tqdm import tqdm

from mr_utils.load_data.s2i import xprot_get_val

def ProcessParameterMap(config_buffer, parammap_file_content):
    '''Fill in the headers of all parammap_file's fields.'''

    # Output document
    out_doc = {'siemens': {}}

    # Input document
    doc = xmltodict.parse(
        ET.tostring(parammap_file_content, encoding='utf8', method='xml'))
    if not ('siemens' in doc and 'parameters' in doc['siemens']):
        msg = 'Malformed parameter map (parameters section not found)'
        raise ValueError(msg)

    for p in tqdm(doc['siemens']['parameters']['p'], leave=False):

        if ('s' not in p) or ('d' not in p):
            logging.error('Malformed parameter map')
            continue

        source = p['s']
        destination = p['d']
        if source.split('.')[0].isnumeric():
            logging.warning('First element of path %s cannot be numeric',
                            source)
            continue

        # Not really sure what this is about
        if source.split('.')[-1].isnumeric():
            index = int(source.split('.')[-1])
        else:
            index = None

        # Go get the parameters!
        try:
            parameters = xprot_get_val(config_buffer, source)

            # We can't serialize numpy arrays, so make 'em into lists
            if isinstance(parameters, np.ndarray):
                parameters = parameters.tolist()

                # Doesn't seem to make a difference...
                # # Single parameters should be single
                # if len(parameters) == 1:
                #     parameters = parameters[0]

        except KeyError:
            tqdm.write('Search path: %s not found.' % source)

        # Again, not sure what index is about, but here you go...
        if index is not None:
            tqdm.write('index >=0 not implemented!')
        else:
            dest = destination.split('.')

            # If the key does not exist, then create it
            for ii, _val in enumerate(dest):
                kys = dest[:ii+1]
                if kys[-1] not in reduce(operator.getitem, kys[:-1], out_doc):
                    reduce(operator.getitem, kys[:-1], out_doc)[kys[-1]] = {}
            reduce(operator.getitem, dest[:-1], out_doc)[dest[-1]] = parameters

    # print(json.dumps(out_doc, indent=2))
    return out_doc
