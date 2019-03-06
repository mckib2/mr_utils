'''All the XML related functions required by siemens_to_ismrmrd.'''

import os
import logging
import xml.etree.ElementTree as ET
import urllib.request

import lxml.etree as lET

def get_ismrmrd_schema(method='ET'):
    '''Download XSD file from ISMRMD git repo.'''
    # We do it this way so we always have the latest version of the schema
    url = ('https://raw.githubusercontent.com/ismrmrd/ismrmrd/master/'
           'schema/ismrmrd.xsd')
    with urllib.request.urlopen(url) as f:
        schema = f.read()

    if method == 'ET':
        return ET.fromstring(schema.decode('utf-8'))
    if method == 'lET':
        return lET.fromstring(schema) #pylint: disable=I1101
    raise ValueError('method not implemented for parsing schema!')

def get_list_of_embedded_files():
    '''List of files to go try to find from the git repo.'''

    # Probably better to pull from repo and cache then have a static list...
    files = ['IsmrmrdParameterMap.xml',
             'IsmrmrdParameterMap.xsl',
             'IsmrmrdParameterMap_Siemens.xml',
             'IsmrmrdParameterMap_Siemens.xsl',
             'IsmrmrdParameterMap_Siemens_EPI.xsl',
             'IsmrmrdParameterMap_Siemens_EPI_FLASHREF.xsl',
             'IsmrmrdParameterMap_Siemens_PreZeros.xsl',
             'IsmrmrdParameterMap_Siemens_T1Mapping_SASHA.xsl',
             'IsmrmrdParameterMap_Siemens_VB17.xml']
    return files

def get_embedded_file(file):
    '''Retrieve embedded file from github.

    file -- Name of embedded file to get.
    '''
    files = get_list_of_embedded_files()
    if file not in files:
        msg = '"%s" is not a valid embedded file.' % file
        raise ValueError(msg)
    # else...
    url = ('https://raw.githubusercontent.com/ismrmrd/siemens_to_ismrmrd/'
           'master/parameter_maps/%s' % file)
    with urllib.request.urlopen(url) as f:
        contents = ET.fromstring(f.read().decode('utf-8'))
    return contents

def getparammap_file_content(parammap_file, usermap_file, VBFILE):
    '''Filler.'''

    if VBFILE:
        if parammap_file is None:
            # If the user did not specify any parameter map file
            if usermap_file is None:
                parammap_file_content = get_embedded_file(
                    'IsmrmrdParameterMap_Siemens_VB17.xml') # this is XML
                logging.info(('Parameter map file is: '
                              'IsmrmrdParameterMap_Siemens_VB17.xml'))

            # If the user specified only a user-supplied parameter map file
            else:
                if not os.path.isfile(usermap_file):
                    msg = ('Parameter map file: %s does not exist.'
                           '' % usermap_file)
                    raise ValueError(msg)

                logging.info('Parameter map file is: %s', usermap_file)
                parammap_file_content = ET.parse(usermap_file)
        else:
            # If the user specified both an embedded and user-supplied
            # parameter map file
            if usermap_file is not None:
                logging.error(('Cannot specify a user-supplied parameter map'
                               ' XML file AND embedded XML file'))
                raise RuntimeError()

            # The user specified an embedded parameter map file only
            parammap_file_content = get_embedded_file(parammap_file) # XML
            logging.info('Parameter map file is: %s', parammap_file)
    else:
        if parammap_file is None:
            # If the user did not specify any parameter map file
            if usermap_file is None:
                parammap_file_content = get_embedded_file(
                    'IsmrmrdParameterMap_Siemens.xml')
                logging.info(
                    'Parameter map file is: IsmrmrdParameterMap_Siemens.xml')

            # If the user specified only a user-supplied parameter map file
            else:
                if not os.path.isfile(usermap_file):
                    logging.error(
                        'Parameter map file: %s does not exist.', usermap_file)
                    raise RuntimeError()

                logging.info('Parameter map file is: %s', usermap_file)
                parammap_file_content = ET.parse(usermap_file)

        else:
            # If the user specified both an embedded and user-supplied
            # parameter map file
            if usermap_file is not None:
                logging.error(('Cannot specify a user-supplied parameter map'
                               ' XML file AND embedded XML file'))
                raise RuntimeError()

            # The user specified an embedded parameter map file only
            parammap_file_content = get_embedded_file(parammap_file)
            logging.info('Parameter map file is: %s', parammap_file)

    return parammap_file_content
