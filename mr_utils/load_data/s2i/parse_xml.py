'''parseXML'''

import xml.etree.ElementTree as ET

import lxml.etree as lET

from mr_utils.load_data.s2i.xml_fun import get_ismrmrd_schema

def parseXML(debug_xml, parammap_xsl_content, _schema_file_name_content,
             xml_config):
    '''Apply XSLT.'''

    xml_doc = parammap_xsl_content

    if xml_doc is None:
        msg = 'Error when parsing xsl parameter stylesheet...'
        raise RuntimeError(msg)

    cur = lET.XSLT(lET.fromstring(ET.tostring(xml_doc))) #pylint: disable=I1101
    doc = lET.fromstring(xml_config.encode()) #pylint: disable=I1101
    res = cur(doc)
    xml_result = lET.tostring(res) #pylint: disable=I1101

    # xmlschema_doc = lET.fromstring(ET.tostring(schema_file_name_content)) #pylint: disable=I1101
    # xmlschema_doc = lET.parse('mr_utils/load_data/parameter_maps/schema.xsd')
    # Doing tostring() from an ET object removes some of the namespace info
    # and makes lET yell about making it an xmlSchema, so just download it
    # again and parse it as an lET for now...
    xmlschema = lET.XMLSchema(get_ismrmrd_schema(method='lET')) #pylint: disable=I1101
    if not xmlschema.validate(res):
        if debug_xml:
            with open('processed.xml', 'w') as f:
                f.write(xml_result)
        msg = 'Generated XML is not valid according to the ISMRMRD schema'
        raise RuntimeError(msg)

    return xml_result
