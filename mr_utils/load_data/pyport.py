'''Python port of siemens_to_ismrmrd.'''

import argparse
import os
import logging
import operator
from functools import reduce
# import json
import urllib.request
import xml.etree.ElementTree as ET
import lxml.etree as lET

import numpy as np
import xmltodict
from tqdm import tqdm
from ismrmrd import Dataset, Acquisition, xsd
from ismrmrd.constants import ACQ_IS_NOISE_MEASUREMENT, \
ACQ_IS_PARALLEL_CALIBRATION, ACQ_LAST_IN_MEASUREMENT, ACQ_IS_DUMMYSCAN_DATA, \
ACQ_IS_SURFACECOILCORRECTIONSCAN_DATA, ACQ_IS_HPFEEDBACK_DATA, \
ACQ_IS_RTFEEDBACK_DATA, ACQ_IS_NAVIGATION_DATA, ACQ_IS_PHASECORR_DATA, \
ACQ_IS_REVERSE, ACQ_IS_PARALLEL_CALIBRATION_AND_IMAGING, \
ACQ_LAST_IN_REPETITION, ACQ_LAST_IN_SLICE, ACQ_FIRST_IN_SLICE

# from mr_utils.load_data.xprot_parser import XProtParser
from mr_utils.load_data.xprot_parser_strsearch import xprot_get_val
# from mr_utils.load_data.parser.infoparser import InfoParser

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

SIEMENS_TO_ISMRMRD_VERSION_MAJOR = 1
SIEMENS_TO_ISMRMRD_VERSION_MINOR = 0
SIEMENS_TO_ISMRMRD_VERSION_PATCH = 1

ISMRMRD_VERSION_MAJOR = 0
ISMRMRD_VERSION_MINOR = 0
ISMRMRD_VERSION_PATCH = 0

MDH_DMA_LENGTH_MASK = 0x01FFFFFF
MDH_ENABLE_FLAGS_MASK = 0xFC000000
MYSTERY_BYTES_EXPECTED = 160

ERR_STATE = -1

class ChannelHeaderAndData(object):
    '''Struct to hold channel data.'''

    def __init__(self):
        self.header = sChannelHeader()
        # std::vector<complex_float_t> data;
        self.data = []

    def display(self):
        '''Show my contents.'''

        self.header.display()
        print('data:', self.data.shape)

class sChannelHeader(object):
    '''Struct to hold channel header data.'''

    @staticmethod
    def sizeof():
        '''Returns c size of struct.'''
        return 32

    def __init__(self):
        self.ulTypeAndChannelLength = 0
        self.lMeasUID = 0
        self.ulScanCounter = 0
        self.ulReserved1 = 0
        self.ulSequenceTime = 0
        self.ulUnused2 = 0
        self.ulChannelId = 0
        self.ulUnused3 = 0
        self.ulCRC = 0

    def display(self):
        '''Show my innards.'''

        print('tsChannelHeader:')
        print('\tsChannelHeader.ulTypeAndChannelLength',
              self.ulTypeAndChannelLength)
        print('\tsChannelHeader.lMeasUID', self.lMeasUID)
        print('\tsChannelHeader.ulScanCounter', self.ulScanCounter)
        print('\tsChannelHeader.ulReserved1', self.ulReserved1)
        print('\tsChannelHeader.ulSequenceTime', self.ulSequenceTime)
        print('\tsChannelHeader.ulUnused2', self.ulUnused2)
        print('\tsChannelHeader.ulChannelId', self.ulChannelId)
        print('\tsChannelHeader.ulUnused3', self.ulUnused3)
        print('\tsChannelHeader.ulCRC', self.ulCRC)

class mdhLC(object):
    '''Filler.'''
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
    '''Filler.'''
    def __init__(self):
        self.ushPre = 0
        self.ushPost = 0

class mdhSlicePosVec(object):
    '''Filler.'''
    def __init__(self):
        self.flCor = 0
        self.flSag = 0
        self.flTra = 0

class mdhSliceData(object):
    '''Filler.'''
    def __init__(self):
        self.sSlicePosVec = mdhSlicePosVec()
        self.aflQuaternion = np.zeros(4)

class sMDH(object):
    '''This is the VB line header'''

    @staticmethod
    def sizeof():
        '''Get the c size of this structure.'''
        return 128

    def __init__(self):
        self.ulFlagsAndDMALength = 0
        self.lMeasUID = 0
        self.ulScanCounter = 0
        self.ulTimeStamp = 0
        self.ulPMUTimeStamp = 0
        self.aulEvalInfoMask = np.zeros(2, dtype=int)
        self.ushSamplesInScan = 0
        self.ushUsedChannels = 0
        self.sLC = mdhLC()
        self.sCutOff = mdhCutOff()

        self.ushKSpaceCentreColumn = 0
        self.ushCoilSelect = 0
        self.fReadOutOffcentre = 0.0
        self.ulTimeSinceLastRF = 0
        self.ushKSpaceCentreLineNo = 0
        self.ushKSpaceCentrePartitionNo = 0
        self.aushIceProgramPara = np.zeros(24, dtype=int)
        self.aushFreePara = np.zeros(4, dtype=int)

        self.sSliceData = mdhSliceData()

        self.ushChannelId = 0
        self.ushPTABPosNeg = 0

    def display(self):
        '''Give a look into your soul.'''

        print('MDH:')
        print('\tmdh.ulFlagsAndDMALength', self.ulFlagsAndDMALength)
        print('\tmdh.lMeasUID', self.lMeasUID)

        print('\tmdh.ulScanCounter', self.ulScanCounter)

        print('\tmdh.ulTimeStamp', self.ulTimeStamp)

        print('\tmdh.ulPMUTimeStamp', self.ulPMUTimeStamp)
        print('\tmdh.aulEvalInfoMask', self.aulEvalInfoMask)
        print('\tmdh.ushSamplesInScan', self.ushSamplesInScan)
        print('\tmdh.ushUsedChannels', self.ushUsedChannels)

        print('\tmdh.sLC', self.sLC)
        print('\tmdh.sCutOff', self.sCutOff)
        print('\tmdh.ushKSpaceCentreColumn', self.ushKSpaceCentreColumn)
        print('\tmdh.ushCoilSelect', self.ushCoilSelect)

        print('\tmdh.fReadOutOffcentre', self.fReadOutOffcentre)
        print('\tmdh.ulTimeSinceLastRF', self.ulTimeSinceLastRF)
        print('\tmdh.ushKSpaceCentreLineNo', self.ushKSpaceCentreLineNo)
        print('\tmdh.ushKSpaceCentrePartitionNo',
              self.ushKSpaceCentrePartitionNo)
        print('\tmdh.aushIceProgramPara', self.aushIceProgramPara)
        print('\tmdh.aushFreePara', self.aushFreePara)
        print('\tmdh.sSliceData', self.sSliceData)
        print('\tmdh.ushChannelId', self.ushChannelId)

        print('\tmdh.ushPTABPosNeg', self.ushPTABPosNeg)


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

def check_positive(value):
    '''Filler.'''
    ivalue = int(value)
    if ivalue < 1:
        raise argparse.ArgumentTypeError(
            "%s is an invalid positive int value" % value)
    return ivalue

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
                siemens_dat, dtype=np.uint32, count=2) #pylint: disable=E1101
            entry['off_'], entry['len_'] = np.fromfile(
                siemens_dat, dtype=np.uint64, count=2) #pylint: disable=E1101
            entry['patName_'], entry['protName_'] = np.fromfile(
                siemens_dat, dtype='U64', count=2) # could be S64?

            ParcFileEntries.append(entry)

            if ii < ParcRaidHead['count_']:
                logging.info(
                    'Protocol name: %s', ParcFileEntries[ii]['protName_'])

    return ParcFileEntries

def readMeasurementHeaderBuffers(siemens_dat, num_buffers):
    '''Filler.'''
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
        buflen = np.fromfile(siemens_dat, dtype=np.uint32, count=1)[0] #pylint: disable=E1101
        bytebuf = siemens_dat.read(buflen)
        buf['buf'] = bytebuf.decode(
            'utf-8', errors='replace').replace('\uFFFD', 'X')
        # print('Size of buf:',len(buf['buf']))

        buffers.append(buf)

    return buffers

def readXmlConfig(debug_xml, parammap_file_content, num_buffers, buffers,
                  wip_double, trajectory, dwell_time_0, max_channels,
                  radial_views, baseLineString, protocol_name):
    '''Read in and format header from raw data file.'''

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
            # print(config_buffer)

            # Write out the raw header if we asked for it
            if debug_xml:
                with open('config_buffer.xprot', 'w') as f:
                    f.write(config_buffer)

            # Get some parameters - wip long
            try:
                wip_long = xprot_get_val(
                    config_buffer, 'MEAS.sWiPMemBlock.alFree')
                if wip_long.size == 0:
                    # If we found it but have no entries, then something is
                    # wrong
                    raise RuntimeError('Failed to find WIP long parameters')
            except KeyError:
                msg = 'Search path: MEAS.sWipMemBlock.alFree not found.'
                logging.warning(msg)

            # Get some parameters - wip double
            try:
                wip_double = xprot_get_val(
                    config_buffer, 'MEAS.sWiPMemBlock.adFree')
                if wip_double.size == 0:
                    raise RuntimeError('Failed to find WIP double parameters')
            except KeyError:
                msg = 'Search path: MEAS.sWipMemBlock.adFree not found.'
                logging.warning(msg)

            # Get some parameters - dwell times
            try:
                dwell_time_0 = xprot_get_val(
                    config_buffer, 'MEAS.sRXSPEC.alDwellTime')
                if dwell_time_0.size == 0:
                    raise RuntimeError('Failed to find dwell times')
                dwell_time_0 = dwell_time_0[0]
            except KeyError:
                msg = 'Search path: MEAS.sWipMemBlock.alDwellTime not found.'
                logging.warning(msg)

            # Get some parameters - trajectory
            try:
                traj = xprot_get_val(
                    config_buffer, 'MEAS.sKSpace.ucTrajectory')
                if traj.size != 1:
                    raise RuntimeError(
                        'Failed to find appropriate trajectory array')
                # Convert into enum:
                trajectory = {
                    1: 'TRAJECTORY_CARTESIAN',
                    2: 'TRAJECTORY_RADIAL',
                    4: 'TRAJECTORY_SPIRAL',
                    8: 'TRAJECTORY_BLADE'
                }[traj[0]]
                logging.info('Trajectory is: %d (%s)', traj, trajectory)
            except KeyError:
                msg = 'Search path: MEAS.sKSpace.ucTrajectory not found.'
                logging.warning(msg)

            # Get some parameters - max channels
            try:
                max_channels = xprot_get_val(
                    config_buffer, 'YAPS.iMaxNoOfRxChannels')
                if max_channels.size == 0:
                    raise RuntimeError(
                        'Failed to find YAPS.iMaxNoOfRxChannels array')
                max_channels = max_channels[0]
            except KeyError:
                msg = 'Search path: YAPS.iMaxNoOfRxChannels not found'
                logging.warning(msg)

            # Get some parameters - cartesian encoding bits
            try:
                tmp = xprot_get_val(config_buffer,
                                    'MEAS.sKSpace.lPhaseEncodingLines')
                if tmp.size == 0:
                    msg = 'Failed to find MEAS.sKSpace.lPhaseEncodingLines'
                    raise RuntimeError(msg)
                lPhaseEncodingLines = tmp[0]
            except KeyError:
                msg = 'Search path: MEAS.sKSpace.lPhaseEncodingLines not found'
                logging.warning(msg)

            try:
                iNoOfFourierLines = xprot_get_val(
                    config_buffer, 'YAPS.iNoOfFourierLines')
                if iNoOfFourierLines.size == 0:
                    msg = 'Failed to find YAPS.iNoOfFourierLines array'
                    raise RuntimeError(msg)
                iNoOfFourierLines = iNoOfFourierLines[0]
            except KeyError:
                msg = 'Search path: YAPS.iNoOfFourierLines not found'
                logging.warning(msg)

            has_FirstFourierLine = False
            try:
                lFirstFourierLine = xprot_get_val(
                    config_buffer, 'YAPS.lFirstFourierLine')
                if lFirstFourierLine.size == 0:
                    msg = 'Failed to find YAPS.lFirstFourierLine array'
                    logging.warning(msg)
                    has_FirstFourierLine = False
                else:
                    lFirstFourierLine = lFirstFourierLine[0]
                    has_FirstFourierLine = True
            except KeyError:
                msg = 'Search path: YAPS.lFirstFourierLine not found'
                logging.warning(msg)

            # get the center partition parameters
            try:
                lPartitions = xprot_get_val(
                    config_buffer, 'MEAS.sKSpace.lPartitions')
                if lPartitions.size == 0:
                    msg = 'Failed to find MEAS.sKSpace.lPartitions array'
                    raise RuntimeError(msg)
                lPartitions = lPartitions[0]
            except KeyError:
                msg = 'Search path: MEAS.sKSpace.lPartitions not found'
                logging.warning(msg)

            # Note: iNoOfFourierPartitions is sometimes absent for 2D sequences
            try:
                iNoOfFourierPartitions = xprot_get_val(
                    config_buffer, 'YAPS.iNoOfFourierPartitions')
                if iNoOfFourierPartitions.size == 0:
                    iNoOfFourierPartitions = 1
                else:
                    iNoOfFourierPartitions = iNoOfFourierPartitions[0]
            except KeyError:
                iNoOfFourierPartitions = 1

            has_FirstFourierPartition = False
            try:
                lFirstFourierPartition = xprot_get_val(
                    config_buffer, 'YAPS.lFirstFourierPartition')
                if lFirstFourierPartition.size == 0:
                    msg = 'Failed to find encYAPS.lFirstFourierPartition array'
                    logging.warning(msg)
                    has_FirstFourierPartition = False
                else:
                    lFirstFourierPartition = lFirstFourierPartition[0]
                    has_FirstFourierPartition = True
            except KeyError:
                msg = 'Search path: YAPS.lFirstFourierPartition not found'
                logging.warning(msg)


            # set the values
            if has_FirstFourierLine: # bottom half for partial fourier
                center_line = lPhaseEncodingLines/2 - (
                    lPhaseEncodingLines - iNoOfFourierLines)
            else:
                center_line = lPhaseEncodingLines/2

            if iNoOfFourierPartitions > 1:
                # 3D
                if has_FirstFourierPartition: # bottom half for partial fourier
                    center_partition = lPartitions/2 - (
                        lPartitions - iNoOfFourierPartitions)
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
            try:
                radial_views = xprot_get_val(
                    config_buffer, 'MEAS.sKSpace.lRadialViews')
                if radial_views.size == 0:
                    msg = 'Failed to find MEAS.sKSpace.lRadialViews array'
                    raise RuntimeError(msg)
                radial_views = radial_views[0]
            except KeyError:
                msg = 'Search path: MEAS.sKSpace.lRadialViews not found'
                logging.warning(msg)

            # Get some parameters - protocol name
            try:
                protocol_name = xprot_get_val(
                    config_buffer, 'HEADER.tProtocolName')
                if not protocol_name:
                    msg = 'Failed to find HEADER.tProtocolName'
                    raise RuntimeError(msg)
            except KeyError:
                msg = 'Search path: HEADER.tProtocolName not found'
                logging.warning(msg)

            # Get some parameters - base line
            try:
                baseLineString = xprot_get_val(
                    config_buffer, 'MEAS.sProtConsistencyInfo.tBaselineString')
                if not baseLineString:
                    raise KeyError()
            except KeyError:
                try:
                    baseLineString = xprot_get_val(
                        config_buffer,
                        'MEAS.sProtConsistencyInfo.tBaselineString')
                    if not baseLineString:
                        raise KeyError()
                except KeyError:
                    msg = ('Failed to find MEAS.sProtConsistencyInfo.'
                           'tMeasuredBaselineString.tBaselineString/'
                           'tMeasuredBaselineString')
                    logging.warning(msg)

            return(ProcessParameterMap(config_buffer, parammap_file_content),
                   protocol_name, baseLineString)

    # We'll never hit this, here for linting
    return None

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


def readScanHeader(siemens_dat, VBFILE):
    '''Read the header from the scan.'''

    # Make the things we're going to fill up
    scanhead = sScanHeader()
    mdh = sMDH()

    scanhead.ulFlagsAndDMALength = np.fromfile(
        siemens_dat, dtype=np.uint32, count=1)  #pylint: disable=E1101

    # If we're VB, then we have an MDH to deal with
    if VBFILE:

        # Read everything in to the MDH skipping the first field -- you know,
        # cause we just read it up above
        # siemens_dat.read(reinterpret_cast<char *>(&mdh) + sizeof(uint32_t),
        #     sizeof(sMDH) - sizeof(uint32_t));

        mdh.lMeasUID = np.fromfile(
            siemens_dat, dtype=np.int32, count=1)

        (mdh.ulScanCounter, mdh.ulTimeStamp,
         mdh.ulPMUTimeStamp) = np.fromfile(
             siemens_dat, dtype=np.uint32, count=3)

        mdh.aulEvalInfoMask = np.fromfile(
            siemens_dat, dtype=np.uint32, count=2)

        mdh.ushSamplesInScan, mdh.ushUsedChannels = np.fromfile(
            siemens_dat, dtype=np.uint16, count=2)

        (mdh.sLC.ushLine, mdh.sLC.ushAcquisition, mdh.sLC.ushSlice,
         mdh.sLC.ushPartition, mdh.sLC.ushEcho, mdh.sLC.ushPhase,
         mdh.sLC.ushRepetition, mdh.sLC.ushSet, mdh.sLC.ushSeg, mdh.sLC.ushIda,
         mdh.sLC.ushIdb, mdh.sLC.ushIdc, mdh.sLC.ushIdd,
         mdh.sLC.ushIde) = np.fromfile(siemens_dat, dtype=np.uint16, count=14)

        mdh.sCutOff.ushPre, mdh.sCutOff.ushPost = np.fromfile(
            siemens_dat, dtype=np.uint16, count=2)

        mdh.ushKSpaceCentreColumn, mdh.ushCoilSelect = np.fromfile(
            siemens_dat, dtype=np.uint16, count=2)

        mdh.fReadOutOffcentre = np.fromfile(
            siemens_dat, dtype=np.float32, count=1)

        mdh.ulTimeSinceLastRF = np.fromfile(
            siemens_dat, dtype=np.uint32, count=1)

        (mdh.ushKSpaceCentreLineNo,
         mdh.ushKSpaceCentrePartitionNo) = np.fromfile(
             siemens_dat, dtype=np.uint16, count=2)

        mdh.aushIceProgramPara = np.fromfile(
            siemens_dat, dtype=np.uint16, count=4)

        mdh.aushFreePara = np.fromfile(siemens_dat, dtype=np.uint16, count=4)

        (mdh.sSliceData.sSlicePosVec.flSag,
         mdh.sSliceData.sSlicePosVec.flCor,
         mdh.sSliceData.sSlicePosVec.flTra) = np.fromfile(
             siemens_dat, dtype=np.float32, count=3)

        mdh.sSliceData.aflQuaternion = np.fromfile(
            siemens_dat, dtype=np.float32, count=4)

        mdh.ushChannelId, mdh.ushPTABPosNeg = np.fromfile(
            siemens_dat, dtype=np.uint16, count=2)


        scanhead.lMeasUID = mdh.lMeasUID
        scanhead.ulScanCounter = mdh.ulScanCounter
        scanhead.ulTimeStamp = mdh.ulTimeStamp
        scanhead.ulPMUTimeStamp = mdh.ulPMUTimeStamp
        scanhead.ushSystemType = 0
        scanhead.ulPTABPosDelay = 0
        scanhead.lPTABPosX = 0
        scanhead.lPTABPosY = 0
        scanhead.lPTABPosZ = mdh.ushPTABPosNeg #TODO: Modify calculation
        scanhead.ulReserved1 = 0
        scanhead.aulEvalInfoMask[0] = mdh.aulEvalInfoMask[0]
        scanhead.aulEvalInfoMask[1] = mdh.aulEvalInfoMask[1]
        scanhead.ushSamplesInScan = mdh.ushSamplesInScan
        scanhead.ushUsedChannels = mdh.ushUsedChannels
        scanhead.sLC = mdh.sLC
        scanhead.sCutOff = mdh.sCutOff
        scanhead.ushKSpaceCentreColumn = mdh.ushKSpaceCentreColumn
        scanhead.ushCoilSelect = mdh.ushCoilSelect
        scanhead.fReadOutOffcentre = mdh.fReadOutOffcentre
        scanhead.ulTimeSinceLastRF = mdh.ulTimeSinceLastRF
        scanhead.ushKSpaceCentreLineNo = mdh.ushKSpaceCentreLineNo
        scanhead.ushKSpaceCentrePartitionNo = mdh.ushKSpaceCentrePartitionNo
        scanhead.sSliceData = mdh.sSliceData
        # memcpy(scanhead.aushIceProgramPara, mdh.aushIceProgramPara,
        #     8 * sizeof(uint16_t))
        scanhead.aushIceProgramPara[:8] = np.concatenate(
            (mdh.aushIceProgramPara, mdh.aushFreePara))
        scanhead.ushApplicationCounter = 0
        scanhead.ushApplicationMask = 0
        scanhead.ulCRC = 0

    else:
        # siemens_dat.read(reinterpret_cast<char*>(&scanhead)+sizeof(uint32_t),
        #                  sizeof(sScanHeader) - sizeof(uint32_t));
        raise NotImplementedError()

    return(scanhead, mdh)


def readChannelHeaders(siemens_dat, VBFILE, scanhead):
    '''Read the headers for the channels.'''

    nchannels = scanhead.ushUsedChannels
    nsamples = scanhead.ushSamplesInScan
    # channels = np.zeros((nchannels, scanhead.ushSamplesInScan))
    channels = np.empty(nchannels, dtype=object)
    for c in range(nchannels):

        if VBFILE:
            # siemens_dat.read(reinterpret_cast<char *>(&mdh), sizeof(sMDH));
            mdh = sMDH()

            if c > 0:
                mdh.ulFlagsAndDMALength = np.fromfile(
                    siemens_dat, dtype=np.uint32, count=1)

                mdh.lMeasUID = np.fromfile(
                    siemens_dat, dtype=np.int32, count=1)

                (mdh.ulScanCounter, mdh.ulTimeStamp,
                 mdh.ulPMUTimeStamp) = np.fromfile(
                     siemens_dat, dtype=np.uint32, count=3)

                mdh.aulEvalInfoMask = np.fromfile(
                    siemens_dat, dtype=np.uint32, count=2)

                mdh.ushSamplesInScan, mdh.ushUsedChannels = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2)

                (mdh.sLC.ushLine, mdh.sLC.ushAcquisition, mdh.sLC.ushSlice,
                 mdh.sLC.ushPartition, mdh.sLC.ushEcho, mdh.sLC.ushPhase,
                 mdh.sLC.ushRepetition, mdh.sLC.ushSet, mdh.sLC.ushSeg,
                 mdh.sLC.ushIda, mdh.sLC.ushIdb, mdh.sLC.ushIdc,
                 mdh.sLC.ushIdd, mdh.sLC.ushIde) = np.fromfile(
                     siemens_dat, dtype=np.uint16, count=14)

                mdh.sCutOff.ushPre, mdh.sCutOff.ushPost = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2)

                mdh.ushKSpaceCentreColumn, mdh.ushCoilSelect = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2)

                mdh.fReadOutOffcentre = np.fromfile(
                    siemens_dat, dtype=np.float32, count=1)

                mdh.ulTimeSinceLastRF = np.fromfile(
                    siemens_dat, dtype=np.uint32, count=1)

                (mdh.ushKSpaceCentreLineNo,
                 mdh.ushKSpaceCentrePartitionNo) = np.fromfile(
                     siemens_dat, dtype=np.uint16, count=2)

                mdh.aushIceProgramPara = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=4)

                mdh.aushFreePara = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=4)

                (mdh.sSliceData.sSlicePosVec.flSag,
                 mdh.sSliceData.sSlicePosVec.flCor,
                 mdh.sSliceData.sSlicePosVec.flTra) = np.fromfile(
                     siemens_dat, dtype=np.float32, count=3)

                mdh.sSliceData.aflQuaternion = np.fromfile(
                    siemens_dat, dtype=np.float32, count=4)

                mdh.ushChannelId, mdh.ushPTABPosNeg = np.fromfile(
                    siemens_dat, dtype=np.uint16, count=2)

            # Now put all required fields from MDH into channel header
            channels[c] = ChannelHeaderAndData()
            channels[c].header.ulTypeAndChannelLength = 0
            channels[c].header.lMeasUID = mdh.lMeasUID
            channels[c].header.ulScanCounter = mdh.ulScanCounter
            channels[c].header.ulReserved1 = 0
            channels[c].header.ulSequenceTime = 0
            channels[c].header.ulUnused2 = 0
            channels[c].header.ulChannelId = mdh.ushChannelId
            channels[c].header.ulUnused3 = 0
            channels[c].header.ulCRC = 0

        else:
            # siemens_dat.read(reinterpret_cast<char *>(&channels[c].header),
            #     sizeof(sChannelHeader));
            raise NotImplementedError()

        channels[c].data = np.fromfile(
            siemens_dat, dtype=np.complex64, count=nsamples)

    return channels


def getAcquisition(flash_pat_ref_scan, trajectory, dwell_time_0, max_channels,
                   _isAdjustCoilSens, _isAdjQuietCoilSens, _isVB, traj,
                   scanhead, channels):
    '''Create ISMRMRD acqusition object for the current channel data.'''

    ismrmrd_acq = Acquisition()
    # The number of samples, channels and trajectory dimensions is set below

    # Acquisition header values are zero by default
    ismrmrd_acq.measurement_uid = scanhead.lMeasUID
    ismrmrd_acq.scan_counter = scanhead.ulScanCounter
    ismrmrd_acq.acquisition_time_stamp = scanhead.ulTimeStamp
    ismrmrd_acq.physiology_time_stamp[0] = scanhead.ulPMUTimeStamp #pylint: disable=E1101
    ismrmrd_acq.available_channels = max_channels
    # Mask to indicate which channels are active. Support for 1024 channels
    # uint64_t channel_mask[16];
    ismrmrd_acq.discard_pre = scanhead.sCutOff.ushPre
    ismrmrd_acq.discard_post = scanhead.sCutOff.ushPost
    ismrmrd_acq.center_sample = scanhead.ushKSpaceCentreColumn

    # std::cout << "isAdjustCoilSens, isVB : " << isAdjustCoilSens << " "
    #           << isVB << std::endl;

    # Is this is noise?
    if scanhead.aulEvalInfoMask[0] & (1 << 25):
        raise NotImplementedError()
        # ismrmrd_acq.sample_time_us() = compute_noise_sample_in_us(
        #     scanhead.ushSamplesInScan, isAdjustCoilSens, isAdjQuietCoilSens,
        #     isVB)
    else:
        ismrmrd_acq.sample_time_us = dwell_time_0 / 1000.0

    # std::cout << "ismrmrd_acq.sample_time_us(): "
    #           << ismrmrd_acq.sample_time_us() << std::endl;

    ismrmrd_acq.position[0] = scanhead.sSliceData.sSlicePosVec.flSag #pylint: disable=E1101
    ismrmrd_acq.position[1] = scanhead.sSliceData.sSlicePosVec.flCor #pylint: disable=E1101
    ismrmrd_acq.position[2] = scanhead.sSliceData.sSlicePosVec.flTra #pylint: disable=E1101

    # Convert Siemens quaternions to direction cosines.
    # In the Siemens convention the quaternion corresponds to a rotation
    # matrix with columns P R S
    # Siemens stores the quaternion as (W,X,Y,Z)
    quat = np.zeros(4)
    quat[0] = scanhead.sSliceData.aflQuaternion[1] # X
    quat[1] = scanhead.sSliceData.aflQuaternion[2] # Y
    quat[2] = scanhead.sSliceData.aflQuaternion[3] # Z
    quat[3] = scanhead.sSliceData.aflQuaternion[0] # W
    # ISMRMRD::ismrmrd_quaternion_to_directions(quat,
    #                                           ismrmrd_acq.phase_dir(),
    #                                           ismrmrd_acq.read_dir(),
    #                                           ismrmrd_acq.slice_dir());


    ismrmrd_acq.patient_table_position[0] = scanhead.lPTABPosX #pylint: disable=E1101
    ismrmrd_acq.patient_table_position[1] = scanhead.lPTABPosY #pylint: disable=E1101
    ismrmrd_acq.patient_table_position[2] = scanhead.lPTABPosZ #pylint: disable=E1101

    # This doesn't seem to get used...
    # fixedE1E2 = True
    # if scanhead.aulEvalInfoMask[0] & (1 << 25):
    #     fixedE1E2 = False # noise
    # if scanhead.aulEvalInfoMask[0] & (1 << 1):
    #     fixedE1E2 = False # navigator, rt feedback
    # if scanhead.aulEvalInfoMask[0] & (1 << 2):
    #     fixedE1E2 = False # hp feedback
    # if scanhead.aulEvalInfoMask[0] & (1 << 51):
    #     fixedE1E2 = False # dummy
    # if scanhead.aulEvalInfoMask[0] & (1 << 5):
    #     fixedE1E2 = False # synch data

    ismrmrd_acq.idx.average = scanhead.sLC.ushAcquisition #pylint: disable=E1101
    ismrmrd_acq.idx.contrast = scanhead.sLC.ushEcho #pylint: disable=E1101
    ismrmrd_acq.idx.kspace_encode_step_1 = scanhead.sLC.ushLine #pylint: disable=E1101
    ismrmrd_acq.idx.kspace_encode_step_2 = scanhead.sLC.ushPartition #pylint: disable=E1101
    ismrmrd_acq.idx.phase = scanhead.sLC.ushPhase #pylint: disable=E1101
    ismrmrd_acq.idx.repetition = scanhead.sLC.ushRepetition #pylint: disable=E1101
    ismrmrd_acq.idx.segment = scanhead.sLC.ushSeg #pylint: disable=E1101
    ismrmrd_acq.idx.set = scanhead.sLC.ushSet #pylint: disable=E1101
    ismrmrd_acq.idx.slice = scanhead.sLC.ushSlice #pylint: disable=E1101
    ismrmrd_acq.idx.user[0] = scanhead.sLC.ushIda #pylint: disable=E1101
    ismrmrd_acq.idx.user[1] = scanhead.sLC.ushIdb #pylint: disable=E1101
    ismrmrd_acq.idx.user[2] = scanhead.sLC.ushIdc #pylint: disable=E1101
    ismrmrd_acq.idx.user[3] = scanhead.sLC.ushIdd #pylint: disable=E1101
    ismrmrd_acq.idx.user[4] = scanhead.sLC.ushIde #pylint: disable=E1101
    # TODO: remove this once the GTPlus can properly autodetect partial fourier
    ismrmrd_acq.idx.user[5] = scanhead.ushKSpaceCentreLineNo #pylint: disable=E1101
    ismrmrd_acq.idx.user[6] = scanhead.ushKSpaceCentrePartitionNo #pylint: disable=E1101

    # *************************************************************************
    # the user_int[0] and user_int[1] are used to store user defined parameters
    # *************************************************************************
    ismrmrd_acq.user_int[0] = int(scanhead.aushIceProgramPara[0]) #pylint: disable=E1101
    ismrmrd_acq.user_int[1] = int(scanhead.aushIceProgramPara[1]) #pylint: disable=E1101
    ismrmrd_acq.user_int[2] = int(scanhead.aushIceProgramPara[2]) #pylint: disable=E1101
    ismrmrd_acq.user_int[3] = int(scanhead.aushIceProgramPara[3]) #pylint: disable=E1101
    ismrmrd_acq.user_int[4] = int(scanhead.aushIceProgramPara[4]) #pylint: disable=E1101
    ismrmrd_acq.user_int[5] = int(scanhead.aushIceProgramPara[5]) #pylint: disable=E1101
    ismrmrd_acq.user_int[6] = int(scanhead.aushIceProgramPara[6]) #pylint: disable=E1101
    # TODO: in the newer version of ismrmrd, add field to store
    # time_since_perp_pulse
    ismrmrd_acq.user_int[7] = int(scanhead.ulTimeSinceLastRF) #pylint: disable=E1101

    ismrmrd_acq.user_float[0] = float(scanhead.aushIceProgramPara[8]) #pylint: disable=E1101
    ismrmrd_acq.user_float[1] = float(scanhead.aushIceProgramPara[9]) #pylint: disable=E1101
    ismrmrd_acq.user_float[2] = float(scanhead.aushIceProgramPara[10]) #pylint: disable=E1101
    ismrmrd_acq.user_float[3] = float(scanhead.aushIceProgramPara[11]) #pylint: disable=E1101
    ismrmrd_acq.user_float[4] = float(scanhead.aushIceProgramPara[12]) #pylint: disable=E1101
    ismrmrd_acq.user_float[5] = float(scanhead.aushIceProgramPara[13]) #pylint: disable=E1101
    ismrmrd_acq.user_float[6] = float(scanhead.aushIceProgramPara[14]) #pylint: disable=E1101
    ismrmrd_acq.user_float[7] = float(scanhead.aushIceProgramPara[15]) #pylint: disable=E1101

    if scanhead.aulEvalInfoMask[0] & (1 << 25):
        ismrmrd_acq.setFlag(ACQ_IS_NOISE_MEASUREMENT)
    if scanhead.aulEvalInfoMask[0] & (1 << 28):
        ismrmrd_acq.setFlag(ACQ_FIRST_IN_SLICE)
    if scanhead.aulEvalInfoMask[0] & (1 << 29):
        ismrmrd_acq.setFlag(ACQ_LAST_IN_SLICE)
    if scanhead.aulEvalInfoMask[0] & (1 << 11):
        ismrmrd_acq.setFlag(ACQ_LAST_IN_REPETITION)

    # if a line is both image and ref, then do not set the ref flag
    if scanhead.aulEvalInfoMask[0] & (1 << 23):
        ismrmrd_acq.setFlag(ACQ_IS_PARALLEL_CALIBRATION_AND_IMAGING)
    else:
        if scanhead.aulEvalInfoMask[0] & (1 << 22):
            ismrmrd_acq.setFlag(ACQ_IS_PARALLEL_CALIBRATION)


    if scanhead.aulEvalInfoMask[0] & (1 << 24):
        ismrmrd_acq.setFlag(ACQ_IS_REVERSE)
    if scanhead.aulEvalInfoMask[0] & (1 << 11):
        ismrmrd_acq.setFlag(ACQ_LAST_IN_MEASUREMENT)
    if scanhead.aulEvalInfoMask[0] & (1 << 21):
        ismrmrd_acq.setFlag(ACQ_IS_PHASECORR_DATA)
    if scanhead.aulEvalInfoMask[0] & (1 << 1):
        ismrmrd_acq.setFlag(ACQ_IS_NAVIGATION_DATA)
    if scanhead.aulEvalInfoMask[0] & (1 << 1):
        ismrmrd_acq.setFlag(ACQ_IS_RTFEEDBACK_DATA)
    if scanhead.aulEvalInfoMask[0] & (1 << 2):
        ismrmrd_acq.setFlag(ACQ_IS_HPFEEDBACK_DATA)
    if scanhead.aulEvalInfoMask[0] & (1 << 51):
        ismrmrd_acq.setFlag(ACQ_IS_DUMMYSCAN_DATA)
    if scanhead.aulEvalInfoMask[0] & (1 << 10):
        ismrmrd_acq.setFlag(ACQ_IS_SURFACECOILCORRECTIONSCAN_DATA)
    if scanhead.aulEvalInfoMask[0] & (1 << 5):
        ismrmrd_acq.setFlag(ACQ_IS_DUMMYSCAN_DATA)
    # if scanhead.aulEvalInfoMask[0] & (1ULL << 1):
    #     ismrmrd_acq.setFlag(ISMRMRD_ACQ_LAST_IN_REPETITION)

    if scanhead.aulEvalInfoMask[0] & (1 << 46):
        ismrmrd_acq.setFlag(ACQ_LAST_IN_MEASUREMENT)

    if flash_pat_ref_scan and ismrmrd_acq.isFlagSet(
            ACQ_IS_PARALLEL_CALIBRATION):
        # For some sequences the PAT Reference data is collected using
        # a different encoding space, e.g. EPI scans with FLASH PAT Reference
        # enabled by command line option
        # TODO: it is likely that the dwell time is not set properly for this
        # type of acquisition
        ismrmrd_acq.encoding_space_ref = 1

    # Spiral and not noise, we will add the trajectory to the data
    if trajectory == 'TRAJECTORY_SPIRAL' and not ismrmrd_acq.isFlagSet(
            ACQ_IS_NOISE_MEASUREMENT):


        # from above we have the following
        # traj_dim[0] = dimensionality (2)
        # traj_dim[1] = ngrad i.e. points per interleaf
        # traj_dim[2] = no. of interleaves
        # and
        # traj.getData() is a float * pointer to the trajectory stored
        # kspace_encode_step_1 is the interleaf number

        # Set the acquisition number of samples, channels and trajectory
        # dimensions this reallocates the memory
        traj_dim = traj.getDims()
        ismrmrd_acq.resize(scanhead.ushSamplesInScan, scanhead.ushUsedChannels,
                           traj_dim[0])

        traj_samples_to_copy = ismrmrd_acq.number_of_samples() #pylint: disable=E1101
        if traj_dim[1] < traj_samples_to_copy:
            traj_samples_to_copy = traj_dim[1]
            ismrmrd_acq.discard_post = \
                ismrmrd_acq.number_of_samples() - traj_samples_to_copy #pylint: disable=E1101

        # NEED TO DO THESE LINES:
        # float *t_ptr = &traj.getDataPtr()[traj_dim[0] * traj_dim[1]
        # * ismrmrd_acq.idx().kspace_encode_step_1];
        # memcpy((void *) ismrmrd_acq.getTrajPtr(), t_ptr, sizeof(float)
        # * traj_dim[0] * traj_samples_to_copy);
        raise NotImplementedError()
    else: # No trajectory
        # Set the acquisition number of samples, channels and trajectory
        # dimensions; this reallocates the memory
        ismrmrd_acq.resize(scanhead.ushSamplesInScan, scanhead.ushUsedChannels)

    for c in range(ismrmrd_acq.active_channels): #pylint: disable=E1101
        ismrmrd_acq.data[:] = channels[c].data
        # memcpy((complex_float_t *) &(ismrmrd_acq.getDataPtr()[c
        #  ismrmrd_acq.number_of_samples()]),
        #        &channels[c].data[0], ismrmrd_acq.number_of_samples()
        # * sizeof(complex_float_t))


    if np.mod(scanhead.ulScanCounter, 1000) == 0:
        logging.info('wrote scan: %d', scanhead.ulScanCounter)

    return ismrmrd_acq

def parseXML(debug_xml, parammap_xsl_content, schema_file_name_content,
             xml_config):
    '''Apply XSLT.'''

    # xsltStylesheetPtr cur = NULL;

    # xmlDocPtr doc, res, xml_doc;

    # const char *params[16 + 1];

    # nbparams = 0
    # params[nbparams] = NULL;

    # xmlSubstituteEntitiesDefault(1);

    # xmlLoadExtDtdDefaultValue = 1

    # xml_doc = xmlParseMemory(parammap_xsl_content.c_str(),
    #                          parammap_xsl_content.size());
    xml_doc = parammap_xsl_content

    if xml_doc is None:
        msg = 'Error when parsing xsl parameter stylesheet...'
        raise RuntimeError(msg)

    # cur = xsltParseStylesheetDoc(xml_doc);
    cur = lET.XSLT(lET.fromstring(ET.tostring(xml_doc))) #pylint: disable=I1101

    # doc = xmlParseMemory(xml_config.c_str(), xml_config.size());
    doc = lET.fromstring(xml_config.encode())

    # res = xsltApplyStylesheet(cur, doc, params);
    res = cur(doc)

    # xmlChar *out_ptr = NULL;
    # int xslt_length = 0;
    # int xslt_result = xsltSaveResultToString(&out_ptr, &xslt_length, res,
    #                                          cur);
    # if (xslt_result < 0) {
    #     std::cerr << "Failed to save converted doc to string" << std::endl;
    # }
    # std::string xml_result = std::string((char *) out_ptr, xslt_length);
    xml_result = lET.tostring(res) #pylint: disable=I1101

    # if (xml_file_is_valid(xml_result, schema_file_name_content) <= 0) {
    #     std::stringstream sstream;
    #     sstream <<
    #             "Generated XML is not valid according to the ISMRMRD schema";
    #     throw std::runtime_error(sstream.str());
    #     if (debug_xml) {
    #         std::ofstream o("processed.xml");
    #         o.write(xml_result.c_str(), xml_result.size());
    #     }
    # }

    ## Comment out for now
    # xmlschema = lET.XMLSchema(lET.fromstring(ET.tostring( #pylint: disable=I1101
    #     schema_file_name_content)))
    # if not xmlschema.validate(res):
    #     if debug_xml:
    #         with open('processed.xml', 'w') as f:
    #             f.write(xml_result)
    #     msg = 'Generated XML is not valid according to the ISMRMRD schema'
    #     raise RuntimeError(msg)

    return xml_result


def fill_ismrmrd_header(h, study_date, study_time):
    '''Add dates/times to ISMRMRD header.'''
    try:

        # ---------------------------------
        # fill more info into the ismrmrd header
        # ---------------------------------
        # study
        study_date_needed = False
        study_time_needed = False

        if h.studyInformation:
            if not h.studyInformation.studyDate:
                study_date_needed = True

            if not h.studyInformation.studyTime:
                study_time_needed = True

        else:
            study_date_needed = True
            study_time_needed = True


        if study_date_needed or study_time_needed:
            # ISMRMRD::StudyInformation study;
            print(dir(h.studyInformation))

            if study_date_needed and study_date != '':
                # study.studyDate.set(study_date)
                setattr(h.studyInformation.studyDate, study_date)
                logging.info('Study date: %s', study_date)

            if study_time_needed and study_time != '':
                # study.studyTime.set(study_time)
                setattr(h.studyInformation.studyTime, study_time)
                logging.info('Study time: %s', study_time)


            # h.studyInformation.set(study)

        # ---------------------------------
        # go back to string
        # ---------------------------------

    except Exception as e:
        print(e)
        return False

    return h

def pyport(version=False, list_embed=False, extract=None, user_stylesheet=None,
           file=None, pMapStyle=None, measNum=1, pMap=None, user_map=None,
           debug=False, header_only=False, output='output.h5',
           flash_pat_ref_scan=False, append_buffers=False,
           study_date_user_supplied=''):
    '''Run the program with arguments.'''

    # If we only wanted the version, that's all we're gonna do
    if version:
        print('Converter version is: %s.%s.%s' % (
            SIEMENS_TO_ISMRMRD_VERSION_MAJOR,
            SIEMENS_TO_ISMRMRD_VERSION_MINOR,
            SIEMENS_TO_ISMRMRD_VERSION_PATCH))
        print('Built against ISMRMRD version: %s.%s.%s' % (
            ISMRMRD_VERSION_MAJOR,
            ISMRMRD_VERSION_MINOR,
            ISMRMRD_VERSION_PATCH))
        return

    # Embedded files are parameter maps and stylesheets included with this
    # program
    if list_embed:
        print('Embedded Files:')
        for f in sorted(get_list_of_embedded_files()):
            print('\t%s' % f)
        return

    # Extract specified parameter map if requested
    if extract is not None:
        # Make everything look like a list so we can iterate over it
        if not isinstance(extract, list):
            extract = [extract]

        # Save the files!
        for paramMap in extract:
            # will raise ValueError if file not valid!
            xml = get_embedded_file(paramMap)

            # For now just print it out
            print(ET.tostring(xml).decode())
        return

    # If we are going any further, we're going to need a file...
    if file is None:
        raise ValueError('Missing Siemens DAT filename')

    # Check if Siemens file can be opened, if not, we're in trouble
    if not os.path.isfile(file):
        msg = ('Provided Siemens file (%s) can not be opened or does not '
               'exist' % file)
        raise IOError(msg)
    # else...
    logging.info('Siemens file is: %s', file)


    # Deal with loading in either embedded or user-supplied param maps and
    # stylesheets
    if pMapStyle is None:
        # No user specified stylesheet
        if user_stylesheet is None:
            parammap_xsl_content = get_embedded_file(
                'IsmrmrdParameterMap_Siemens.xsl') # this is XML
        else:
            if os.path.isfile(user_stylesheet):
                parammap_xsl_content = get_embedded_file(user_stylesheet)
            else:
                msg = ('Parameter XSL stylesheet (%s) does not exist.'
                       '' % user_stylesheet)
                raise IOError(msg)

    else:
        # If the user specified both an embedded and user-supplied stylesheet
        if user_stylesheet is not None:
            msg = ('Cannot specify a user-supplied parameter map XSL '
                   'stylesheet AND embedded stylesheet')
            raise ValueError(msg)
        # else...
        # The user specified an embedded stylesheet only
        if os.path.isfile(pMapStyle):
            parammap_xsl_content = ET.parse(pMapStyle) # this is XML
            logging.info('Parameter XSL stylesheet is: %s', pMapStyle)
        else:
            msg = '%s does not exist or can\'t be opened!' % pMapStyle
            raise IOError(msg)


    # Grab the ISMRMRD schema
    schema_file_name_content = get_ismrmrd_schema() # this is XML

    # Now let's get to the dirty work...
    with open(file, 'br') as siemens_dat:

        VBFILE = False
        ParcRaidHead = {}
        ParcRaidHead['hdSize_'], ParcRaidHead['count_'] = np.fromfile(
            siemens_dat, dtype=np.uint32, count=2) #pylint: disable=E1101

        if ParcRaidHead['hdSize_'] > 32:
            VBFILE = True
            # Rewind, we have no raid file header.
            siemens_dat.seek(0, os.SEEK_CUR)
            ParcRaidHead['hdSize_'] = ParcRaidHead['count_']
            ParcRaidHead['count_'] = 1

        elif ParcRaidHead['hdSize_'] != 0:
            # This is a VB line data file
            msg = ('Only VD line files with MrParcRaidFileHeader.'
                   'hdSize_ == 0 (MR_PARC_RAID_ALLDATA) supported.')
            raise NotImplementedError(msg)

        if (not VBFILE) and (measNum > ParcRaidHead['count_']):
            logging.error(('The file you are trying to convert has only %d'
                           'measurements.', ParcRaidHead['count_']))
            logging.error('You are trying to convert measurement number: %d',
                          measNum)
            raise ValueError()

        # if it is a VB scan
        if (VBFILE and (measNum != 1)):
            logging.error(('The file you are trying to convert is a VB file'
                           ' and it has only one measurement.'))
            logging.error('You tried to convert measurement number: %d',
                          measNum)
            raise ValueError()


        parammap_file_content = getparammap_file_content(
            pMap, user_map, VBFILE)

        logging.info('This file contains %d measurement(s). ',
                     ParcRaidHead['count_'])

        ParcFileEntries = readParcFileEntries(
            siemens_dat, ParcRaidHead, VBFILE)

        # find the beginning of the desired measurement
        siemens_dat.seek(ParcFileEntries[measNum - 1]['off_'], os.SEEK_SET)

        dma_length, num_buffers = np.fromfile(
            siemens_dat, dtype=np.uint32, count=2) #pylint: disable=E1101

        buffers = readMeasurementHeaderBuffers(siemens_dat, num_buffers)

        # We need to be on a 32 byte boundary after reading the buffers
        position_in_meas = siemens_dat.tell() - ParcFileEntries[
            measNum-1]['off_']
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
        # dict_config is xml_config, but dict_config is a dictionary
        # and xml_config is a string in the c version
        dict_config, protocol_name, baseLineString = readXmlConfig(
            debug, parammap_file_content, num_buffers, buffers, wip_double,
            trajectory, dwell_time_0, max_channels, radial_views,
            baseLineString, protocol_name)

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

        if debug:
            with open('xml_raw.xml', 'w') as f:
                f.write(xmltodict.unparse(dict_config, pretty=True))


        # ISMRMRD::IsmrmrdHeader header;
        config = parseXML(debug, parammap_xsl_content,
                          schema_file_name_content,
                          xmltodict.unparse(dict_config))
        header = xsd.CreateFromDocument(config)

        # Append buffers to xml_config if requested
        if append_buffers:
            raise NotImplementedError()
            # append_buffers_to_xml_header(buffers, num_buffers, header)


        ismrmrd_dataset = Dataset('tmp.h5', 'dataset', create_if_needed=True)
        # # If this is a spiral acquisition, we will calculate the trajectory
        # # and add it to the individual profilesISMRMRD::NDArray<float> traj;
        # auto traj = getTrajectory(wip_double, trajectory, dwell_time_0,
        #                           radial_views);
        traj = None


        last_mask = 0
        acquisitions = 1
        sync_data_packets = 0
        first_call = True

        # Last scan not encountered AND not reached end of measurement without
        # acqend
        pfe = ParcFileEntries[measNum-1]
        sScanSize = sScanHeader.sizeof()
        while (not last_mask & 1) and (((pfe['off_'] + pfe['len_']) \
                - siemens_dat.tell()) > sScanSize):


            position_in_meas = siemens_dat.tell()
            scanhead, mdh = readScanHeader(siemens_dat, VBFILE)
            # mdh.display()

            if not siemens_dat:
                logging.error(
                    'Error reading header at acquisition %d.', acquisitions)
                break


            dma_length = scanhead.ulFlagsAndDMALength[0] & MDH_DMA_LENGTH_MASK
            mdh_enable_flags = scanhead.ulFlagsAndDMALength[0] \
                & MDH_ENABLE_FLAGS_MASK

            # Check if this is sync data, if so, it must be handled differently
            if scanhead.aulEvalInfoMask[0] & (1 << 5):
                raise NotImplementedError()
                last_scan_counter = acquisitions - 1
                # TODO:
                # auto waveforms = readSyncdata(siemens_dat, VBFILE,
                #  acquisitions, dma_length,scanhead,header,last_scan_counter);
                # for (auto& w : waveforms)
                #     ismrmrd_dataset->appendWaveform(w);
                sync_data_packets += 1
                continue

            if first_call:
                time_stamp = scanhead.ulTimeStamp

                # convert to acqusition date and time
                timeInSeconds = time_stamp*2.5/1e3
                mins, secs = divmod(timeInSeconds, 60)
                hours, mins = divmod(mins, 60)
                study_time = '%d:%02d:%02d' % (hours, mins, secs)
                print('STUDY TIME IS:', study_time)

                # If some of the ismrmrd header fields are not filled, here
                # is a place to take some further actions
                tmp = fill_ismrmrd_header(
                    header, study_date_user_supplied, study_time)
                if tmp is False:
                    logging.error('Failed to further fill XML header')
                else:
                    header = tmp

                # std::stringstream sstream;
                # ISMRMRD::serialize(header,sstream);
                # xml_config = sstream.str();
                # if xml_file_is_valid(
                #     xml_config, schema_file_name_content) <= 0:
                #     msg = ('Generated XML is not valid according to the
                #            'ISMRMRD schema')
                #     raise ValueError(msg)

                if debug:
                    with open('processed.xml', 'w') as f:
                        f.write(xmltodict.unparse(dict_config, pretty=True))

                # This means we should only create XML header and exit
                if header_only:
                    with open(output, 'w') as f:
                        f.write(xmltodict.unparse(dict_config, pretty=True))
                    return
                ## Create an ISMRMRD dataset

            # This check only makes sense in VD line files.
            if not VBFILE and (scanhead.lMeasUID != pfe['measId_']):
                # Something must have gone terribly wrong. Bail out.
                if first_call:
                    msg = ('Corrupted or retro-recon dataset detected '
                           '(scanhead.lMeasUID != ParcFileEntries[%d].measId_'
                           'Fix the scanhead.lMeasUID...' % (measNum-1))
                    logging.error(msg)
                scanhead.lMeasUID = pfe['measId_']

            if first_call:
                first_call = False

            # Allocate data for channels
            channels = readChannelHeaders(siemens_dat, VBFILE, scanhead)

            if not siemens_dat:
                msg = 'Error reading data at acqusition %s' % acquisitions
                logging.error(msg)
                break

            acquisitions += 1
            last_mask = scanhead.aulEvalInfoMask[0]
            if last_mask & 1:
                logging.info('Last scan reached...')
                break


            # dataset.append(channels)
            ismrmrd_dataset.append_acquisition(getAcquisition(
                flash_pat_ref_scan, trajectory, dwell_time_0, max_channels,
                isAdjustCoilSens, isAdjQuietCoilSens, isVB, traj, scanhead,
                channels))

        # End of the while loop

        if not siemens_dat:
            msg = 'WARNING: Unexpected error.  Please check the result.'
            raise SystemError(msg)

        # ismrmrd_dataset.write_xml_header(
        #     xmltodict.unparse(dict_config, pretty=True))
        ismrmrd_dataset.write_xml_header(header.toxml())

        # Mystery bytes. There seems to be 160 mystery bytes at the end of the
        # data.
        mystery_bytes = (pfe['off_'] + pfe['len_']) - siemens_dat.tell()

        if mystery_bytes > 0:
            if mystery_bytes != MYSTERY_BYTES_EXPECTED:
                # Something in not quite right
                msg = 'WARNING: Unexpected number of mystery bytes detected: '
                logging.error('%s%d', msg, mystery_bytes)
                msg = 'ParcFileEntries[%d].off_ = %d' %(measNum-1, pfe['off_'])
                logging.error(msg)
                msg = 'ParcFileEntries[%d].len_ = %d' %(measNum-1, pfe['len_'])
                logging.error(msg)
                msg = 'siemens_dat.tellg() = %d' % siemens_dat.tell()
                logging.error(msg)
                logging.error('Please check the result.')

            else:
                # Read the mystery bytes
                _mystery_data = np.fromfile(siemens_dat, count=mystery_bytes)
                # After this we have to be on a 512 byte boundary
                offset = np.mod(siemens_dat.tell(), 512)
                if offset:
                    siemens_dat.seek(512 - offset, os.SEEK_CUR)


        end_position = siemens_dat.tell()
        siemens_dat.seek(0, os.SEEK_END)
        eof_position = siemens_dat.tell()
        if end_position != eof_position and ParcRaidHead['count_'] == measNum:
            additional_bytes = eof_position - end_position
            msg = ('WARNING: End of file was not reached during conversion. '
                   'There are %d additional bytes at the end of file.'
                   '' % additional_bytes)
            logging.warning(msg)

        return ismrmrd_dataset


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
    parser.add_argument('-l', dest='list_embed', action='store_true',
                        help='<List embedded files>', default=True)
    parser.add_argument('-e', dest='extract', help='<Extract embedded file>')
    parser.add_argument('-X', dest='debug', help='<Debug XML flag>',
                        default=True)
    parser.add_argument('-F', dest='flash_pat_ref_scan',
                        help='<FLASH PAT REF flag>', default=True)
    parser.add_argument('-H', dest='headerOnly',
                        help='<HEADER ONLY flag (create xml header only)>',
                        default=True)
    parser.add_argument('-B', dest='append_buffers',
                        help=('<Append Siemens protocol buffers (base64) to '
                              'user parameters>'), default=True)
    parser.add_argument('--studyDate', dest='study_date_user_supplied',
                        help=('<User can supply study date, in the format of '
                              'yyyy-mm-dd>'), default='')

    args = parser.parse_args()
    print(args)
    status = pyport(vars(args))
    if status == ERR_STATE:
        pass
