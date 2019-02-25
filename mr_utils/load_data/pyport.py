'''Python port of siemens_to_ismrmrd.'''

import argparse
import os
import logging
import operator
from functools import reduce
import json
import urllib.request
import xml.etree.ElementTree as ET

import numpy as np
import xmltodict

from mr_utils.load_data.xprot_parser import XProtParser
# from mr_utils.load_data.parser.infoparser import InfoParser

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

SIEMENS_TO_ISMRMRD_VERSION_MAJOR = 1
SIEMENS_TO_ISMRMRD_VERSION_MINOR = 0
SIEMENS_TO_ISMRMRD_VERSION_PATCH = 1

ISMRMRD_VERSION_MAJOR = 0
ISMRMRD_VERSION_MINOR = 0
ISMRMRD_VERSION_PATCH = 0

ERR_STATE = -1

class mdhLC(object):
    def __init__(self):
        self.ushLine = 0
        self.ushAcquisition = 0
        self.ushSlice = 0
        self.ushPartition = 0
        self.ushEcho = 0
        self.ushPhase = 0
        self.ushRepetition = 0
        self.ushSet = 0
        self.ushSeg = 0
        self.ushIda = 0
        self.ushIdb = 0
        self.ushIdc = 0
        self.ushIdd = 0
        self.ushIde = 0

class mdhCutOff(object):
    def __init__(self):
        self.ushPre = 0
        self.ushPost = 0

class mdhSlicePosVec(object):
    def __init__(self):
        self.flCor = 0
        self.flSag = 0
        self.flTra = 0

class mdhSliceData(object):
    def __init__(self):
        self.sSlicePosVec = mdhSlicePosVec()
        self.aflQuaternion = np.zeros(4)

class sScanHeader(object):
    '''This is the VD line header'''

    @staticmethod
    def sizeof():
        '''Get the c size of this structure.'''
        return 192

    def __init__(self):
        self.ulFlagsAndDMALength = 0
        self.lMeasUID = 0
        self.ulScanCounter = 0
        self.ulTimeStamp = 0
        self.ulPMUTimeStamp = 0
        self.ushSystemType = 0
        self.ulPTABPosDelay = 0
        self.lPTABPosX = 0
        self.lPTABPosY = 0
        self.lPTABPosZ = 0
        self.ulReserved1 = 0
        self.aulEvalInfoMask = np.zeros(2, dtype=int)
        self.ushSamplesInScan = 0
        self.ushUsedChannels = 0
        self.sLC = mdhLC()
        self.sCutOff = mdhCutOff()
        self.ushKSpaceCentreColumn = 0
        self.ushCoilSelect = 0
        self.fReadOutOffcentre = 0
        self.ulTimeSinceLastRF = 0
        self.ushKSpaceCentreLineNo = 0
        self.ushKSpaceCentrePartitionNo = 0
        self.sSliceData = mdhSliceData()
        self.aushIceProgramPara = np.zeros(24)
        self.aushReservedPara = np.zeros(4)
        self.ushApplicationCounter = 0
        self.ushApplicationMask = 0
        self.ulCRC = 0

def get_ismrmrd_schema():
    '''Download XSD file from ISMRMD git repo.'''
    # We do it this way so we always have the latest version of the schema
    url = ('https://raw.githubusercontent.com/ismrmrd/ismrmrd/master/'
           'schema/ismrmrd.xsd')
    with urllib.request.urlopen(url) as f:
        schema = f.read().decode('utf-8')
    return ET.fromstring(schema)

def get_list_of_embedded_files():
    '''List of files to go try to find from the git repo.'''
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
    files = get_list_of_embedded_files()
    if file not in files:
        logging.error('%s is not a valid embedded file.', file)
        return ERR_STATE
    # else...
    url = ('https://raw.githubusercontent.com/ismrmrd/siemens_to_ismrmrd/'
           'master/parameter_maps/%s' % file)
    with urllib.request.urlopen(url) as f:
        contents = ET.fromstring(f.read().decode('utf-8'))
    return contents

def check_positive(value):
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError(
            "%s is an invalid positive int value" % value)
    return ivalue

def getparammap_file_content(parammap_file, usermap_file, VBFILE):

    if VBFILE:
        if parammap_file is None:
            # If the user did not specify any parameter map file
            if usermap_file is None:
                parammap_file_content = get_embedded_file(
                    'IsmrmrdParameterMap_Siemens_VB17.xml')
                logging.info(('Parameter map file is: '
                              'IsmrmrdParameterMap_Siemens_VB17.xml'))

            # If the user specified only a user-supplied parameter map file
            else:
                if not os.path.isfile(usermap_file):
                    logging.error('Parameter map file: %s does not exist.',
                                  usermap_file)
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

def readParcFileEntries(siemens_dat, ParcRaidHead, VBFILE):
    '''
    struct MrParcRaidFileEntry
    {
      uint32_t measId_;
      uint32_t fileId_;
      uint64_t off_;
      uint64_t len_;
      char patName_[64];
      char protName_[64];
    };
    '''

    #TODO: Using a list right now, structured np array would probably be better
    NUM_ENTRIES = 64
    ParcFileEntries = []

    if VBFILE:
        logging.info('VB line file detected.')

        # In case of VB file, we are just going to fill these with zeros.
        # It doesn't exist.
        for ii in range(NUM_ENTRIES):
            ParcFileEntries.append({
                'measId_':0,
                'fileId_':0,
                'off_':0,
                'len_':0,
                'patName_':'',
                'protName_':''})

        ParcFileEntries[0]['off_'] = 0

        # Rewind a bit, we have no raid file header.
        siemens_dat.seek(0, os.SEEK_END)

        # This is the whole size of the dat file
        ParcFileEntries[0]['len_'] = siemens_dat.tell()

        # Rewind a bit, we have no raid file header.
        siemens_dat.seek(0, os.SEEK_SET)

        # blank
        logging.info('Protocol name: %s', ParcFileEntries[0]['protName_'])

    else:
        logging.info('VD line file detected.')

        for ii in range(NUM_ENTRIES):
            entry = {}
            entry['measId_'], entry['fileId_'] = np.fromfile(
                siemens_dat, dtype=np.uint32, count=2)
            entry['off_'], entry['len_'] = np.fromfile(
                siemens_dat, dtype=np.uint64, count=2)
            entry['patName_'], entry['protName_'] = np.fromfile(
                siemens_dat, dtype='U64', count=2) # could be S64?

            ParcFileEntries.append(entry)

            if ii < ParcRaidHead['count_']:
                logging.info(
                    'Protocol name: %s', ParcFileEntries[ii]['protName_'])

    return ParcFileEntries

def readMeasurementHeaderBuffers(siemens_dat, num_buffers):
    buffers = []
    logging.info('Number of parameter buffers: %s', str(num_buffers))
    for _b in range(num_buffers):

        buf = {}
        start = siemens_dat.tell()
        tmp_bufname = siemens_dat.readline().decode(errors='replace')

        idx = tmp_bufname.find('\0')
        if idx > -1:
            siemens_dat.seek(start + idx+1, os.SEEK_SET)
            tmp_bufname = tmp_bufname[:idx]

        logging.info('Buffer Name: %s', tmp_bufname)
        buf['name'] = tmp_bufname
        buflen = np.fromfile(siemens_dat, dtype=np.uint32, count=1)[0]
        bytebuf = siemens_dat.read(buflen)
        buf['buf'] = bytebuf.decode(
            'utf-8', errors='replace').replace('\uFFFD', 'X')
        # print('Size of buf:',len(buf['buf']))

        buffers.append(buf)

    return buffers

def readXmlConfig(debug_xml, parammap_file_content, num_buffers, buffers,
                  wip_double, trajectory, dwell_time_0, max_channels,
                  radial_views, baseLineString, protocol_name):

    dwell_time_0 = 0
    max_channels = 0
    radial_views = 0
    protocol_name = ''
    wip_long = []
    center_line = 0
    center_partition = 0
    lPhaseEncodingLines = 0
    iNoOfFourierLines = 0
    lPartitions = 0
    iNoOfFourierPartitions = 0

    for b in range(num_buffers):
        if buffers[b]['name'] == 'Meas':

            # Grab the header from the .dat file
            config_buffer = buffers[b]['buf'][:-2]

            # Write out the raw header if we asked for it
            if debug_xml:
                with open('config_buffer.xprot', 'w') as f:
                    f.write(config_buffer)

            # Let's parse this sucker
            parser = XProtParser()
            parser.parse(config_buffer)
            doc_root = parser.structure['XProtocol']['Params']['']
            # parser = InfoParser()
            # doc_root = xmltodict.parse(
            #    parser.raw2xml(config_buffer))['doc_root']

            # Get some parameters - wip long
            # const XProtocol::XNode* n2 = apply_visitor(
            #    XProtocol::getChildNodeByName("MEAS.sWipMemBlock.alFree"), n);
            try:
                wip_long = [int(x) for x in doc_root['MEAS']['sWiPMemBlock']['alFree']]
            except:
                logging.warning(
                    'Search path: MEAS.sWipMemBlock.alFree not found.')
            if wip_long:
                logging.error('Failed to find WIP long parameters')
                raise RuntimeError()

            # Get some parameters - wip double
            # const XProtocol::XNode* n2 = apply_visitor(
            #    XProtocol::getChildNodeByName("MEAS.sWipMemBlock.adFree"), n);
            try:
                wip_double = [float(x) for x in doc_root['MEAS']['sWiPMemBlock']['adFree'][1:]]
            except:
                logging.warning(
                    'Search path: MEAS.sWipMemBlock.adFree not found.')
            if wip_double:
                logging.error('Failed to find WIP double parameters')
                raise RuntimeError()

            # Get some parameters - dwell times
            # const XProtocol::XNode* n2 = apply_visitor(
            #   XProtocol::getChildNodeByName("MEAS.sRXSPEC.alDwellTime"), n);
            try:
                temp = [int(x) for x in doc_root['MEAS']['sRXSPEC']['alDwellTime']]
            except:
                logging.warning(
                    'Search path: MEAS.sWipMemBlock.alDwellTime not found.')
            if temp:
                logging.error('Failed to find dwell times')
                raise RuntimeError()
            else:
                dwell_time_0 = temp[0]

            # Get some parameters - trajectory
            # const XProtocol::XNode* n2 = apply_visitor(
            #    XProtocol::getChildNodeByName("MEAS.sKSpace.ucTrajectory"), n)
            try:
                temp = [int(doc_root['MEAS']['sKSpace']['ucTrajectory'][0])]
            except:
                logging.warning(
                    'Search path: MEAS.sKSpace.ucTrajectory not found.')
            if len(temp) != 1:
                logging.error('Failed to find appropriate trajectory array')
                raise RuntimeError()
            else:
                # enum class Trajectory {
                #   TRAJECTORY_CARTESIAN = 0x01,
                #   TRAJECTORY_RADIAL    = 0x02,
                #   TRAJECTORY_SPIRAL    = 0x04,
                #   TRAJECTORY_BLADE     = 0x08
                # };
                traj = temp[0]
                trajectory = {
                    1: 'TRAJECTORY_CARTESIAN',
                    2: 'TRAJECTORY_RADIAL',
                    4: 'TRAJECTORY_SPIRAL',
                    8: 'TRAJECTORY_BLADE'
                }[traj]
                logging.info('Trajectory is: %d (%s)', (traj, trajectory))

            # Get some parameters - max channels
            # const XProtocol::XNode* n2 = apply_visitor(
            #    XProtocol::getChildNodeByName("YAPS.iMaxNoOfRxChannels"), n);
            try:
                temp = [int(doc_root['YAPS']['iMaxNoOfRxChannels'][0])]
            except:
                logging.warning(
                    'Search path: YAPS.iMaxNoOfRxChannels not found')
            if len(temp) != 1:
                logging.error('Failed to find YAPS.iMaxNoOfRxChannels array')
                raise RuntimeError()
            else:
                max_channels = temp[0]

            # Get some parameters - cartesian encoding bits
            # get the center line parameters
            # const XProtocol::XNode* n2 = apply_visitor(
            #         XProtocol::getChildNodeByName(
            #            "MEAS.sKSpace.lPhaseEncodingLines"), n);
            try:
                temp = [int(doc_root['MEAS']['sKSpace']['lPhaseEncodingLines'][0])]
            except:
                logging.warning('MEAS.sKSpace.lPhaseEncodingLines not found')
            if len(temp) != 1:
                logging.error(
                    'Failed to find MEAS.sKSpace.lPhaseEncodingLines array')
                raise RuntimeError()
            else:
                lPhaseEncodingLines = temp[0]

            # n2 = apply_visitor(XProtocol::getChildNodeByName(
            #    "YAPS.iNoOfFourierLines"), n);
            try:
                temp = [int(doc_root['YAPS']['iNoOfFourierLines'][0])]
            except:
                logging.warning('YAPS.iNoOfFourierLines not found')

            if len(temp) != 1:
                logging.error('Failed to find YAPS.iNoOfFourierLines array')
                raise RuntimeError()
            else:
                iNoOfFourierLines = temp[0]

            has_FirstFourierLine = False
            # n2 = apply_visitor(XProtocol::getChildNodeByName(
            #    "YAPS.lFirstFourierLine"), n);
            try:
                temp = doc_root['YAPS']['lFirstFourierLine']
            except:
                logging.warning('YAPS.lFirstFourierLine not found')
            try:
                lFirstFourierLine = int(temp[0])
                has_FirstFourierLine = True
            except:
                logging.warning('Failed to find YAPS.lFirstFourierLine array')
                has_FirstFourierLine = False

            # get the center partition parameters
            # n2 = apply_visitor(XProtocol::getChildNodeByName(
            #    "MEAS.sKSpace.lPartitions"), n);
            try:
                temp = [int(doc_root['MEAS']['sKSpace']['lPartitions'][0])]
            except:
                logging.warning('MEAS.sKSpace.lPartitions not found')
            if len(temp) != 1:
                logging.error('Failed to find MEAS.sKSpace.lPartitions array')
                raise RuntimeError()
            else:
                lPartitions = temp[0]

            # Note: iNoOfFourierPartitions is sometimes absent for 2D sequences
            # n2 = apply_visitor(XProtocol::getChildNodeByName(
            #    "YAPS.iNoOfFourierPartitions"), n);
            try:
                temp = doc_root['YAPS']['iNoOfFourierPartitions']
                try:
                    iNoOfFourierPartitions = int(temp[0])
                except:
                    iNoOfFourierPartitions = 1
            except:
                iNoOfFourierPartitions = 1

            has_FirstFourierPartition = False
            # n2 = apply_visitor(XProtocol::getChildNodeByName(
            #    "YAPS.lFirstFourierPartition"), n);
            try:
                temp = doc_root['YAPS']['lFirstFourierPartition']
            except:
                logging.warning('YAPS.lFirstFourierPartition not found')
            try:
                lFirstFourierPartition = int(temp[0])
                has_FirstFourierPartition = True
            except:
                logging.warning(
                    'Failed to find encYAPS.lFirstFourierPartition array')
                has_FirstFourierPartition = False


            # set the values
            if has_FirstFourierLine: # bottom half for partial fourier
                center_line = lPhaseEncodingLines/2 - (lPhaseEncodingLines - iNoOfFourierLines)
            else:
                center_line = lPhaseEncodingLines/2

            if iNoOfFourierPartitions > 1:
                # 3D
                if has_FirstFourierPartition: # bottom half for partial fourier
                    center_partition = lPartitions/2 - (lPartitions - iNoOfFourierPartitions)
                else:
                    center_partition = lPartitions/2
            else:
                # 2D
                center_partition = 0

            # for spiral sequences, center_line and center_partition are zero
            if trajectory == 'TRAJECTORY_SPIRAL':
                center_line = 0
                center_partition = 0

            logging.info('center_line = %d', center_line)
            logging.info('center_partition = %d', center_partition)


            # Get some parameters - radial views
            # const XProtocol::XNode* n2 = apply_visitor(
            #    XProtocol::getChildNodeByName("MEAS.sKSpace.lRadialViews"), n)
            try:
                temp = doc_root['MEAS']['sKSpace']['lRadialViews']
            except:
                logging.warning('MEAS.sKSpace.lRadialViews not found')
            try:
                radial_views = int(temp[0])
            except:
                logging.error(
                    'Failed to find YAPS.MEAS.sKSpace.lRadialViews array')
                raise RuntimeError()



            # Get some parameters - protocol name
            # const XProtocol::XNode* n2 = apply_visitor(
            #    XProtocol::getChildNodeByName("HEADER.tProtocolName"), n);
            try:
                temp = doc_root['HEADER']['tProtocolName']
            except:
                logging.warning('HEADER.tProtocolName not found')
            try:
                protocol_name = temp
            except:
                logging.error('Failed to find HEADER.tProtocolName')
                raise RuntimeError()


            # Get some parameters - base line
            # const XProtocol::XNode* n2 = apply_visitor(
            #         XProtocol::getChildNodeByName(
            #            "MEAS.sProtConsistencyInfo.tBaselineString"), n);
            try:
                baseLineString = doc_root['MEAS']['sProtConsistencyInfo']['tBaselineString'][0]
            except:
                # const XProtocol::XNode* n2 = apply_visitor(
                #         XProtocol::getChildNodeByName(
                #    "MEAS.sProtConsistencyInfo.tMeasuredBaselineString"), n);
                try:
                    baseLineString = doc_root['MEAS']['sProtConsistencyInfo']['tMeasuredBaselineString'][0]
                except:
                    logging.warning(('Failed to find MEAS.sProtConsistencyInfo'
                                     '.tBaselineString/tMeasuredBaseline'
                                     'String'))

            return(ProcessParameterMap(doc_root, parammap_file_content),
                   protocol_name, baseLineString)

def ProcessParameterMap(doc_root, parammap_file_content):

    # Output document
    out_doc = {'siemens': {}}

    # Input document
    doc = xmltodict.parse(ET.tostring(parammap_file_content, encoding='utf8',
                                      method='xml'))
    if not ('siemens' in doc and 'parameters' in doc['siemens']):
        logging.error('Malformed parameter map (parameters section not found)')
        raise ValueError()

    for p in doc['siemens']['parameters']['p']:

        if ('s' not in p) or ('d' not in p):
            logging.error('Malformed parameter map')
            continue

        source = p['s']
        destination = p['d']
        # split_path = source.split('.')
        if source.split('.')[0].isnumeric():
            logging.warning(
                'First element of path %s cannot be numeric', source)
            continue

        # This split_path thing is useless...
        # if len([ sp for sp in split_path[1:-1] if sp.isnumeric() ]):
        #     logging.warning(
        #   'Numeric index not supported inside path for source = %s' % source)
        # search_path = [ sp for sp in split_path[:-1] if ~sp.isnumeric() ]
        # search_path.append(split_path[-1])
        # search_path = '.'.join(search_path)
        search_path = source

        if source.split('.')[-1].isnumeric():
            index = int(source.split('.')[-1])
        else:
            # search_path = search_path + '.' + source.split('.')[-1]
            index = None
        # print(search_path)

        search_path = search_path.split('.')
        try:
            parameters = reduce(operator.getitem, search_path, doc_root)
        except:
            logging.warning('Search path: %s not found.', source)


        if index is not None:
            logging.error('index >=0 not implemented!')
        else:
            dest = destination.split('.')

            # If the key does not exist, then create it
            for ii, _val in enumerate(dest):
                kys = dest[:ii+1]
                # print(dest[:ii+1])
                if kys[-1] not in reduce(operator.getitem, kys[:-1], out_doc):
                    reduce(operator.getitem, kys[:-1], out_doc)[kys[-1]] = {}
            reduce(operator.getitem, dest[:-1], out_doc)[dest[-1]] = parameters

    print(json.dumps(out_doc, indent=2))
    return out_doc

def main(args):
    '''Run the program with arguments.'''

    # If we only wanted the version, that's all we're gonna do
    if args['version']:
        print('Converter version is: %s.%s.%s' % (
            SIEMENS_TO_ISMRMRD_VERSION_MAJOR,
            SIEMENS_TO_ISMRMRD_VERSION_MINOR,
            SIEMENS_TO_ISMRMRD_VERSION_PATCH))
        print('Built against ISMRMRD version: %s.%s.%s' % (
            ISMRMRD_VERSION_MAJOR,
            ISMRMRD_VERSION_MINOR,
            ISMRMRD_VERSION_PATCH))
        return ERR_STATE

    # Embedded files are parameter maps and stylesheets included with this
    # program
    if args['list']:
        print('Embedded Files:')
        for file in sorted(get_list_of_embedded_files()):
            print('\t%s' % file)

    # Extract specified parameter map if requested
    if args['extract'] is not None:
        logging.info('Extract specified parameter map if we asked for it...')
        raise NotImplementedError()

    # If we are going any further, we're going to need a file...
    if args['file'] is None:
        logging.error('Missing Siemens DAT filename')
        return ERR_STATE

    # Check if Siemens file can be opened, if not, we're in trouble
    if not os.path.isfile(args['file']):
        logging.error(('Provided Siemens file (%s) can not be opened or does'
                       ' not exist.', args['file']))
        return ERR_STATE
    # else...
    logging.info('Siemens file is: %s', args['file'])


    # Deal with loading in either embedded or user-supplied param maps and
    # stylesheets
    if args['pMapStyle'] is None:
        # No user specified stylesheet
        if args['user_stylesheet'] is None:
            parammap_xsl_content = get_embedded_file(
                'IsmrmrdParameterMap_Siemens.xsl')
        else:
            if os.path.isfile(args['user_stylesheet']):
                parammap_xsl_content = get_embedded_file(
                    args['user_stylesheet'])
            else:
                logging.error('Parameter XSL stylesheet (%s) does not exist.',
                              args['user_stylesheet'])
                return ERR_STATE
    else:
        # If the user specified both an embedded and user-supplied stylesheet
        if args['user_stylesheet'] is not None:
            logging.error(('Cannot specify a user-supplied parameter map XSL'
                           ' stylesheet AND embedded stylesheet'))
            return ERR_STATE
        # else...
        # The user specified an embedded stylesheet only
        parammap_xsl_content = ET.parse(args['pMapStyle'])
        logging.info('Parameter XSL stylesheet is: %s', args['pMapStyle'])


    # Grab the ISMRMRD schema
    schema_file_name_content = get_ismrmrd_schema()

    # Now let's get to the dirty work...
    with open(args['file'], 'br') as siemens_dat:

        VBFILE = False
        ParcRaidHead = {}
        ParcRaidHead['hdSize_'], ParcRaidHead['count_'] = np.fromfile(
            siemens_dat, dtype=np.uint32, count=2)

        if ParcRaidHead['hdSize_'] > 32:
            VBFILE = True
            # Rewind, we have no raid file header.
            siemens_dat.seek(0, os.SEEK_CUR)
            ParcRaidHead['hdSize_'] = ParcRaidHead['count_']
            ParcRaidHead['count_'] = 1

        elif ParcRaidHead['hdSize_'] != 0:
            # This is a VB line data file
            logging.error(('Only VD line files with MrParcRaidFileHeader.'
                           'hdSize_ == 0 (MR_PARC_RAID_ALLDATA) supported.'))
            return ERR_STATE

        if (not VBFILE) and (args['measNum'] > ParcRaidHead['count_']):
            logging.error(('The file you are trying to convert has only %d'
                           'measurements.', ParcRaidHead['count_']))
            logging.error('You are trying to convert measurement number: %d',
                          args['measNum'])
            return ERR_STATE

        # if it is a VB scan
        if (VBFILE and (args['measNum'] != 1)):
            logging.error(('The file you are trying to convert is a VB file'
                           ' and it has only one measurement.'))
            logging.error('You tried to convert measurement number: %d',
                          args['measNum'])
            return ERR_STATE


        parammap_file_content = getparammap_file_content(
            args['pMap'], args['user_map'], VBFILE)

        logging.info('This file contains %d measurement(s). ',
                     ParcRaidHead['count_'])

        ParcFileEntries = readParcFileEntries(siemens_dat, ParcRaidHead,
                                              VBFILE)

        # find the beginning of the desired measurement
        siemens_dat.seek(ParcFileEntries[args['measNum'] - 1]['off_'],
                         os.SEEK_SET)

        dma_length, num_buffers = np.fromfile(
            siemens_dat, dtype=np.uint32, count=2)

        buffers = readMeasurementHeaderBuffers(siemens_dat, num_buffers)

        # We need to be on a 32 byte boundary after reading the buffers
        position_in_meas = siemens_dat.tell() - ParcFileEntries[args['measNum'] - 1]['off_']
        if np.mod(position_in_meas, 32) != 0:
            siemens_dat.seek(32 - np.mod(position_in_meas, 32), os.SEEK_CUR)

        # Measurement header done!
        # Now we should have the measurement headers, so let's use the Meas
        # header to create the XML parametersstd::string xml_config;
        wip_double = []
        trajectory = {
            'TRAJECTORY_CARTESIAN': 0x01,
            'TRAJECTORY_RADIAL': 0x02,
            'TRAJECTORY_SPIRAL': 0x04,
            'TRAJECTORY_BLADE': 0x08
        }
        # Trajectory trajectory;
        dwell_time_0 = 0
        max_channels = 0
        radial_views = 0
        baseLineString = ''
        protocol_name = ''

        # print(ET.tostring(parammap_file_content).decode())
        xml_config, protocol_name, baseLineString = readXmlConfig(
            args['debug'], parammap_file_content, num_buffers,
            buffers, wip_double, trajectory, dwell_time_0, max_channels,
            radial_views, baseLineString, protocol_name)

        # whether this scan is a adjustment scan
        isAdjustCoilSens = False
        if protocol_name == 'AdjCoilSens':
            isAdjustCoilSens = True

        isAdjQuietCoilSens = False
        if protocol_name == 'AdjQuietCoilSens':
            isAdjQuietCoilSens = True

        # whether this scan is from VB line
        isVB = False
        if any(ext in baseLineString for ext in [
                'VB17', 'VB15', 'VB13', 'VB11']):
            isVB = True

        logging.info('Baseline: %s', baseLineString)

        if args['debug']:
            with open('xml_raw.xml', 'w') as f:
                f.write(xml_config)

        # TODO
        # ISMRMRD::IsmrmrdHeader header;
        # {
        #     std::string config = parseXML(debug_xml, parammap_xsl_content, schema_file_name_content, xml_config);
        #     ISMRMRD::deserialize(config.c_str(), header);
        # }
        # //Append buffers to xml_config if requested
        # if (append_buffers) {
        #     append_buffers_to_xml_header(buffers, num_buffers, header);
        # }
        #
        # // Free memory used for MeasurementHeaderBuffers
        #
        # auto ismrmrd_dataset = boost::make_shared<ISMRMRD::Dataset>(ismrmrd_file.c_str(), ismrmrd_group.c_str(), true);
        # //If this is a spiral acquisition, we will calculate the trajectory and add it to the individual profilesISMRMRD::NDArray<float> traj;
        # auto traj = getTrajectory(wip_double, trajectory, dwell_time_0, radial_views);

        last_mask = 0
        acquisitions = 1
        sync_data_packets = 0
        # mdh # For VB lin
        first_call = True

        # Last scan not encountered AND not reached end of measurement without
        # acqend
        while (~(last_mask & 1) and (((ParcFileEntries[args['measNum'] - 1]['off_'] + ParcFileEntries[args['measNum'] - 1]['len_']) - siemens_dat.tell()) > sScanHeader.sizeof())):

            position_in_meas = siemens_dat.tell()
            scanhead = sScanHeader()

            # TODO
            # readScanHeader(siemens_dat, VBFILE, mdh, scanhead);
            #
            if not siemens_dat:
                logging.error('Error reading header at acquisition %d.' % acquisitions)
                break

            # TODO
            # dma_length = scanhead.ulFlagsAndDMALength & MDH_DMA_LENGTH_MASK
            # mdh_enable_flags = scanhead.ulFlagsAndDMALength & MDH_ENABLE_FLAGS_MASK


            # Check if this is sync data, if so, it must be handled differently
            if scanhead.aulEvalInfoMask[0] & (1 << 5):
                last_scan_counter = acquisitions - 1

                # TODO
            #     auto waveforms = readSyncdata(siemens_dat, VBFILE,acquisitions, dma_length,scanhead,header,last_scan_counter);
            #     for (auto& w : waveforms)
            #         ismrmrd_dataset->appendWaveform(w);
                sync_data_packets += 1
                continue

            if first_call:
                time_stamp = scanhead.ulTimeStamp

                # convert to acqusition date and time
                timeInSeconds = time_stamp*2.5/1e3

                # TODO
                # hours = (size_t)(timeInSeconds/3600)
                # mins =  (size_t)((timeInSeconds - hours*3600) / 60);
                # secs =  (size_t)(timeInSeconds- hours*3600 - mins*60);
                # std::string study_time = get_time_string(hours, mins, secs);

                # # if some of the ismrmrd header fields are not filled, here is a place to take some further actions
                # if (not fill_ismrmrd_header(header, study_date_user_supplied, study_time) ):
                #     logging.error('Failed to further fill XML header')

            #
            #     std::stringstream sstream;
            #     ISMRMRD::serialize(header,sstream);
            #     xml_config = sstream.str();
            #
            #     if xml_file_is_valid(xml_config, schema_file_name_content) <= 0:
            #     {
            #         std::cerr << "Generated XML is not valid according to the ISMRMRD schema" << std::endl;
            #         return -1;
            #     }
            #
            #     if (debug_xml)
            #     {
            #         std::ofstream o("processed.xml");
            #         o.write(xml_config.c_str(), xml_config.size());
            #     }
            #
            #     //This means we should only create XML header and exit
            #     if (header_only) {
            #         std::ofstream header_out_file(ismrmrd_file.c_str());
            #         header_out_file << xml_config;
            #         return -1;
            #     }

            # // Create an ISMRMRD dataset


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Convert Siemens raw data format to ISMRMRD format.')
    parser.add_argument('-v', dest='version', action='store_true',
                        help='Prints converter version and ISMRMRD version')
    parser.add_argument('-f', dest='file', help='<SIEMENS dat file>')
    parser.add_argument('-z', dest='measNum', help='<Measurement number>',
                        default=1, type=check_positive)
    parser.add_argument('-m', dest='pMap', help='<Parameter map XML file>')
    parser.add_argument('-x', dest='pMapStyle',
                        help='<Parameter stylesheet XSL file>')
    parser.add_argument('--user-map',
                        help='<Provide a parameter map XML file>')
    parser.add_argument('--user-stylesheet',
                        help='<Provide a parameter stylesheet XSL file>')
    parser.add_argument('-o', dest='output', help='<ISMRMRD output file>',
                        default='output.h5')
    parser.add_argument('-g', dest='outputGroup',
                        help='<ISMRMRD output group>', default='dataset')
    parser.add_argument('-l', dest='list', action='store_true',
                        help='<List embedded files>', default=True)
    parser.add_argument('-e', dest='extract', help='<Extract embedded file>')
    parser.add_argument('-X', dest='debug', help='<Debug XML flag>',
                        default=True)
    parser.add_argument('-F', dest='flashPatRef', help='<FLASH PAT REF flag>',
                        default=True)
    parser.add_argument('-H', dest='headerOnly',
                        help='<HEADER ONLY flag (create xml header only)>',
                        default=True)
    parser.add_argument('-B', dest='bufferAppend', help='<Append Siemens protocol buffers (bas64) to user parameters>', default=True)
    parser.add_argument('--studyDate', help='<User can supply study date, in the format of yyyy-mm-dd>')

    args = parser.parse_args()
    print(args)
    status = main(vars(args))
    if status == ERR_STATE:
        pass
