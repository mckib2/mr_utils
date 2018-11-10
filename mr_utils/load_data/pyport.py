import argparse
import os
import logging
import xml.etree.ElementTree as ET
import urllib.request
import numpy as np
from mr_utils.load_data.xprot import XProtParser

logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.DEBUG)

SIEMENS_TO_ISMRMRD_VERSION_MAJOR = 1
SIEMENS_TO_ISMRMRD_VERSION_MINOR = 0
SIEMENS_TO_ISMRMRD_VERSION_PATCH = 1

ISMRMRD_VERSION_MAJOR = 0
ISMRMRD_VERSION_MINOR = 0
ISMRMRD_VERSION_PATCH = 0

ERR_STATE = -1

def get_ismrmrd_schema():
    '''Download XSD file from ISMRMD git repo.'''
    # We do it this way so we always have the latest version of the schema
    with urllib.request.urlopen('https://raw.githubusercontent.com/ismrmrd/ismrmrd/master/schema/ismrmrd.xsd') as f:
        schema = f.read().decode('utf-8')
    return(ET.fromstring(schema))

def get_list_of_embedded_files():
    '''List of files to go try to find from the git repo.'''
    files = [
        'IsmrmrdParameterMap.xml',
    	'IsmrmrdParameterMap.xsl',
    	'IsmrmrdParameterMap_Siemens.xml',
    	'IsmrmrdParameterMap_Siemens.xsl',
    	'IsmrmrdParameterMap_Siemens_EPI.xsl',
    	'IsmrmrdParameterMap_Siemens_EPI_FLASHREF.xsl',
    	'IsmrmrdParameterMap_Siemens_PreZeros.xsl',
    	'IsmrmrdParameterMap_Siemens_T1Mapping_SASHA.xsl',
    	'IsmrmrdParameterMap_Siemens_VB17.xml'
    ]
    return(files)

def get_embedded_file(file):
    files = get_list_of_embedded_files()
    if file not in files:
        logging.error('%s is not a valid embedded file.' % file)
        return(ERR_STATE)
    else:
        with urllib.request.urlopen('https://raw.githubusercontent.com/ismrmrd/siemens_to_ismrmrd/master/parameter_maps/%s' % file) as f:
            contents = ET.fromstring(f.read().decode('utf-8'))
        return(contents)

def check_positive(value):
    ivalue = int(value)
    if ivalue < 1:
         raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return(ivalue)

def getparammap_file_content(parammap_file,usermap_file,VBFILE):

    if VBFILE:
        if parammap_file is None:
            # If the user did not specify any parameter map file
            if usermap_file is None:
                parammap_file_content = get_embedded_file('IsmrmrdParameterMap_Siemens_VB17.xml')
                logging.info('Parameter map file is: IsmrmrdParameterMap_Siemens_VB17.xml')

            # If the user specified only a user-supplied parameter map file
            else:
                if not os.path.isfile(usermap_file):
                    logging.error('Parameter map file: %s does not exist.' % usermap_file)
                    raise RuntimeError()

                logging.info('Parameter map file is: %s' % usermap_file)
                parammap_file_content = ET.parse(usermap_file)
        else:
            # If the user specified both an embedded and user-supplied parameter map file
            if usermap_file is not None:
                logging.error('Cannot specify a user-supplied parameter map XML file AND embedded XML file')
                raise RuntimeError()

            # The user specified an embedded parameter map file only
            parammap_file_content = get_embedded_file(parammap_file)
            logging.info('Parameter map file is: %s' % parammap_file)
    else:
        if parammap_file is None:
            # If the user did not specify any parameter map file
            if usermap_file is None:
                parammap_file_content = get_embedded_file('IsmrmrdParameterMap_Siemens.xml')
                logging.info('Parameter map file is: IsmrmrdParameterMap_Siemens.xml')

            # If the user specified only a user-supplied parameter map file
            else:
                if not os.path.isfile(usermap_file):
                    logging.error('Parameter map file: %s does not exist.' % usermap_file)
                    raise RuntimeError()

                logging.info('Parameter map file is: %s' % usermap_file)
                parammap_file_content = ET.parse(usermap_file)

        else:
            # If the user specified both an embedded and user-supplied parameter map file
            if usermap_file is not None:
                logging.error('Cannot specify a user-supplied parameter map XML file AND embedded XML file')
                raise RuntimeError()

            # The user specified an embedded parameter map file only
            parammap_file_content = get_embedded_file(parammap_file)
            logging.info('Parameter map file is: %s' % parammap_file)

    return(parammap_file_content)

def readParcFileEntries(siemens_dat,ParcRaidHead,VBFILE):
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

        # In case of VB file, we are just going to fill these with zeros. It doesn't exist.
        for ii in range(NUM_ENTRIES):
            ParcFileEntries.append({ 'measId_':0, 'fileId_':0, 'off_':0, 'len_':0, 'patName_':'','protName_':'' })

        ParcFileEntries[0]['off_'] = 0
        siemens_dat.seek(0,os.SEEK_END) # Rewind a bit, we have no raid file header.
        ParcFileEntries[0]['len_'] = siemens_dat.tell() # This is the whole size of the dat file
        siemens_dat.seek(0,os.SEEK_SET) # Rewind a bit, we have no raid file header.
        logging.info('Protocol name: %s' % ParcFileEntries[0]['protName_']) # blank

    else:
        logging.info('VD line file detected.')

        for ii in range(NUM_ENTRIES):
            entry = {}
            entry['measId_'],entry['fileId_'] = np.fromfile(siemens_dat,dtype=np.uint32,count=2)
            entry['off_'],entry['len_'] = np.fromfile(siemens_dat,dtype=np.uint64,count=2)
            entry['patName_'],entry['protName_'] = np.fromfile(siemens_dat,dtype='U64',count=2) # could be S64?

            ParcFileEntries.append(entry)

            if ii < ParcRaidHead['count_']:
                logging.info('Protocol name: %s' % ParcFileEntries[ii]['protName_'])

    return(ParcFileEntries)

def readMeasurementHeaderBuffers(siemens_dat,num_buffers):
    buffers = []
    logging.info('Number of parameter buffers: %s' % num_buffers)
    for b in range(num_buffers):

        buf = {}
        start = siemens_dat.tell()
        tmp_bufname = siemens_dat.readline().decode(errors='replace')

        idx = tmp_bufname.find('\0')
        if idx > -1:
            siemens_dat.seek(start + idx+1,os.SEEK_SET)
            tmp_bufname = tmp_bufname[:idx]

        logging.info('Buffer Name: %s' % tmp_bufname)
        buf['name'] = tmp_bufname
        buflen = np.fromfile(siemens_dat,dtype=np.uint32,count=1)[0]
        bytebuf = siemens_dat.read(buflen)
        buf['buf'] = bytebuf.decode('utf-8',errors='replace').replace('\uFFFD','X')
        # print('Size of buf:',len(buf['buf']))

        buffers.append(buf)

    return(buffers)

def readXmlConfig(debug_xml,parammap_file_content,num_buffers,buffers,wip_double,trajectory,dwell_time_0,max_channels,radial_views,baseLineString,protocol_name):

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

            config_buffer = buffers[b]['buf'][:-2]
            # print(config_buffer)

            if debug_xml:
                ## TODO
                # std::ofstream o("config_buffer.xprot");
                # o.write(config_buffer.c_str(), config_buffer.size());
                pass

            parser = XProtParser()
            n = parser.raw2xml(config_buffer)
            if (type(n) is not ET.Element):
                logging.error('Failed to parse XProtocol for buffer %s' % buffers[0]['name'])
                raise RuntimeError()

            # Get some parameters - wip long
            n2 = n.find('ParamMap[@name="sWiPMemBlock"]/ParamLong[@name="alFree"]')
            if n2 is not None:
                for child in n2:
                    wip_long.append(child.text)
            else:
                logging.warning('Search path: MEAS.sWipMemBlock.alFree not found.')

            if len(wip_long) == 0:
                logging.error('Failed to find WIP long parameters')
                raise RuntimeError()

            #Get some parameters - wip double
            n2 = n.find('ParamMap[@name="sWiPMemBlock"]/ParamDouble[@name="adFree"]')
            if n2 is not None:
                for child in n2:
                    wip_double.append(child.text)
            else:
                logging.warning('Search path: MEAS.sWipMemBlock.adFree not found')

            if len(wip_double) == 0:
                logging.error('Failed to find WIP double parameters')
                raise RuntimeError()

            # Get some parameters - dwell times
            n2 = None
            for el in n:
                if len(el) and el[0].text == '"MEAS.sRXSPEC.alDwellTime"':
                    n2 = el
                    break
            if (n2):
                temp = [ el.text for el in n2 ]
                temp = temp[1:]
            else:
                logging.warning('Search path: MEAS.sRXSPEC.alDwellTime not found.')

            if len(temp) == 0:
                logging.error('Failed to find dwell times')
                raise RuntimeError()
            # else:
            #     dwell_time_0 = atoi(temp[0].c_str())

            # # Get some parameters - trajectory
            # const XProtocol::XNode* n2 = apply_visitor(XProtocol::getChildNodeByName("MEAS.sKSpace.ucTrajectory"), n);
            # std::vector<std::string> temp;
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2);
            # else:
            #     logging.warning('Search path: MEAS.sKSpace.ucTrajectory not found.')
            #
            # if (temp.size() != 1):
            #     logging.error('Failed to find appropriate trajectory array')
            #     raise RuntimeError()
            # else:
            #     traj = atoi(temp[0].c_str());
            #     trajectory = Trajectory(traj);
            #     logging.info('Trajectory is: %d' << traj)
            #
            # #Get some parameters - max channels
            # const XProtocol::XNode* n2 = apply_visitor(XProtocol::getChildNodeByName("YAPS.iMaxNoOfRxChannels"), n);
            # std::vector<std::string> temp;
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2);
            # else:
            #     logging.info('YAPS.iMaxNoOfRxChannels')
            #
            # if (temp.size() != 1):
            #     logging.error('Failed to find YAPS.iMaxNoOfRxChannels array')
            #     raise RuntimeError()
            # else:
            #     max_channels = atoi(temp[0].c_str());
            #
            # # Get some parameters - cartesian encoding bits
            # # get the center line parameters
            # const XProtocol::XNode* n2 = apply_visitor(
            #         XProtocol::getChildNodeByName("MEAS.sKSpace.lPhaseEncodingLines"), n);
            # std::vector<std::string> temp;
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2)
            # else:
            #     logging.warning('MEAS.sKSpace.lPhaseEncodingLines not found')
            #
            # if (temp.size() != 1):
            #     logging.error('Failed to find MEAS.sKSpace.lPhaseEncodingLines array')
            #     raise RuntimeError()
            # else:
            #     lPhaseEncodingLines = atoi(temp[0].c_str())
            #
            # n2 = apply_visitor(XProtocol::getChildNodeByName("YAPS.iNoOfFourierLines"), n);
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2)
            # else:
            #     logging.warning('YAPS.iNoOfFourierLines not found')
            #
            # if (temp.size() != 1):
            #     logging.error('Failed to find YAPS.iNoOfFourierLines array')
            #     raise RuntimeError()
            # else:
            #     iNoOfFourierLines = atoi(temp[0].c_str())
            #
            # has_FirstFourierLine = False
            # n2 = apply_visitor(XProtocol::getChildNodeByName("YAPS.lFirstFourierLine"), n);
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2)
            # else:
            #     logging.warning('YAPS.lFirstFourierLine not found')
            #
            # if (temp.size() != 1):
            #     logging.warning('Failed to find YAPS.lFirstFourierLine array')
            #     has_FirstFourierLine = False
            # else:
            #     lFirstFourierLine = atoi(temp[0].c_str())
            #     has_FirstFourierLine = True
            #
            # # get the center partition parameters
            # n2 = apply_visitor(XProtocol::getChildNodeByName("MEAS.sKSpace.lPartitions"), n);
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2)
            # else
            #     logging.warning('MEAS.sKSpace.lPartitions not found')
            #
            # if (temp.size() != 1):
            #     logging.error('Failed to find MEAS.sKSpace.lPartitions array')
            #     raise RuntimeError()
            # else:
            #     lPartitions = atoi(temp[0].c_str())
            #
            # # Note: iNoOfFourierPartitions is sometimes absent for 2D sequences
            # n2 = apply_visitor(XProtocol::getChildNodeByName("YAPS.iNoOfFourierPartitions"), n);
            # if n2:
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2);
            #     if (temp.size() != 1):
            #         iNoOfFourierPartitions = 1
            #     else:
            #         iNoOfFourierPartitions = atoi(temp[0].c_str());
            # else:
            #     iNoOfFourierPartitions = 1
            #
            # has_FirstFourierPartition = False
            # n2 = apply_visitor(XProtocol::getChildNodeByName("YAPS.lFirstFourierPartition"), n);
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2)
            # else:
            #     logging.warning('YAPS.lFirstFourierPartition not found')
            #
            # if (temp.size() != 1):
            #     logging.warning('Failed to find encYAPS.lFirstFourierPartition array')
            #     has_FirstFourierPartition = False
            # else:
            #     lFirstFourierPartition = atoi(temp[0].c_str());
            #     has_FirstFourierPartition = True
            #
            # # set the values
            # if has_FirstFourierLine: # bottom half for partial fourier
            #     center_line = lPhaseEncodingLines/2 - ( lPhaseEncodingLines - iNoOfFourierLines )
            # else:
            #     center_line = lPhaseEncodingLines/2
            #
            # if iNoOfFourierPartitions > 1:
            #     # 3D
            #     if has_FirstFourierPartition: # bottom half for partial fourier
            #         center_partition = lPartitions/2 - ( lPartitions - iNoOfFourierPartitions )
            #     else:
            #         center_partition = lPartitions/2
            # else :
            #     # 2D
            #     center_partition = 0
            #
            # # for spiral sequences the center_line and center_partition are zero
            # if trajectory == Trajectory::TRAJECTORY_SPIRAL:
            #     center_line = 0
            #     center_partition = 0
            #
            # logging.info('center_line = %d' % center_line)
            # loggin.info('center_partition = %d' % center_partition)
            #
            #
            # #Get some parameters - radial views
            # const XProtocol::XNode* n2 = apply_visitor(XProtocol::getChildNodeByName("MEAS.sKSpace.lRadialViews"), n);
            # std::vector<std::string> temp;
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2);
            # else:
            #     logging.warning('MEAS.sKSpace.lRadialViews not found')
            #
            # if (temp.size() != 1):
            #     logging.error('Failed to find YAPS.MEAS.sKSpace.lRadialViews array')
            #     raise RuntimeError()
            # else:
            #     radial_views = atoi(temp[0].c_str())
            #
            #
            # # Get some parameters - protocol name
            # const XProtocol::XNode* n2 = apply_visitor(XProtocol::getChildNodeByName("HEADER.tProtocolName"), n);
            # std::vector<std::string> temp;
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2)
            # else:
            #     logging.warning('HEADER.tProtocolName not found')
            #
            # if (temp.size() != 1):
            #     logging.error('Failed to find HEADER.tProtocolName')
            #     raise RuntimeError()
            #
            # else:
            #     protocol_name = temp[0]
            #
            #
            # # Get some parameters - base line
            # const XProtocol::XNode* n2 = apply_visitor(
            #         XProtocol::getChildNodeByName("MEAS.sProtConsistencyInfo.tBaselineString"), n);
            # std::vector<std::string> temp;
            # if (n2):
            #     temp = apply_visitor(XProtocol::getStringValueArray(), *n2)
            # if (temp.size() > 0):
            #     baseLineString = temp[0]
            #
            # if baseLineString.empty():
            #     const XProtocol::XNode* n2 = apply_visitor(
            #             XProtocol::getChildNodeByName("MEAS.sProtConsistencyInfo.tMeasuredBaselineString"), n);
            #     std::vector<std::string> temp;
            #     if (n2):
            #         temp = apply_visitor(XProtocol::getStringValueArray(), *n2);
            #     if (temp.size() > 0):
            #         baseLineString = temp[0]
            #
            #
            # if baseLineString.empty():
            #     logging.warning('Failed to find MEAS.sProtConsistencyInfo.tBaselineString/tMeasuredBaselineString')
            #
            # # xml_config = ProcessParameterMap(n, parammap_file);
            # return(ProcessParameterMap(n, parammap_file_content.c_str()))


def main(args):

    # If we only wanted the version, that's all we're gonna do
    if args['version']:
        print('Converter version is: %s.%s.%s' % (SIEMENS_TO_ISMRMRD_VERSION_MAJOR,SIEMENS_TO_ISMRMRD_VERSION_MINOR,SIEMENS_TO_ISMRMRD_VERSION_PATCH))
        print('Built against ISMRMRD version: %s.%s.%s' % (ISMRMRD_VERSION_MAJOR,ISMRMRD_VERSION_MINOR,ISMRMRD_VERSION_PATCH))
        return(ERR_STATE)

    # Embedded files are parameter maps and stylesheets included with this program
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
        return(ERR_STATE)

    # Check if Siemens file can be opened, if not, we're in trouble
    if not os.path.isfile(args['file']):
        logging.error('Provided Siemens file (%s) can not be opened or does not exist.' % args['file'])
        return(ERR_STATE)
    else:
        logging.info('Siemens file is: %s' % args['file'])


    # Deal with loading in either embedded or user-supplied param maps and
    # stylesheets
    if args['pMapStyle'] is None:
        # No user specified stylesheet
        if args['user_stylesheet'] is None:
            parammap_xsl_content = get_embedded_file('IsmrmrdParameterMap_Siemens.xsl')
        else:
            if os.path.isfile(args['user_stylesheet']):
                parammap_xsl_content = get_embedded_file(args['user_stylesheet'])
            else:
                logging.error('Parameter XSL stylesheet (%s) does not exist.' % args['user_stylesheet'])
                return(ERR_STATE)
    else:
        # If the user specified both an embedded and user-supplied stylesheet
        if args['user_stylesheet'] is not None:
            logging.error('Cannot specify a user-supplied parameter map XSL stylesheet AND embedded stylesheet')
            return(ERR_STATE)
        else:
            # The user specified an embedded stylesheet only
            parammap_xsl_content = ET.parse(args['pMapStyle']);
            logging.info('Parameter XSL stylesheet is: %s' % args['pMapStyle'])


    # Grab the ISMRMRD schema
    schema_file_name_content = get_ismrmrd_schema()

    # Now let's get to the dirty work...
    with open(args['file'],'br') as siemens_dat:

        VBFILE = False
        ParcRaidHead = {}
        ParcRaidHead['hdSize_'],ParcRaidHead['count_'] = np.fromfile(siemens_dat,dtype=np.uint32,count=2)

        if (ParcRaidHead['hdSize_'] > 32):
            VBFILE = True
            # Rewind, we have no raid file header.
            siemens_dat.seek(0,os.SEEK_CUR);
            ParcRaidHead['hdSize_'] = ParcRaidHead['count_']
            ParcRaidHead['count_'] = 1

        elif (ParcRaidHead['hdSize_'] != 0):
            # This is a VB line data file
            logging.error('Only VD line files with MrParcRaidFileHeader.hdSize_ == 0 (MR_PARC_RAID_ALLDATA) supported.')
            return(ERR_STATE)

        if (not VBFILE) and (args['measNum'] > ParcRaidHead['count_']):
            logging.error('The file you are trying to convert has only %d measurements.' % ParcRaidHead['count_'])
            logging.error('You are trying to convert measurement number: %d' % args['measNum'])
            return(ERR_STATE)

        # if it is a VB scan
        if (VBFILE and (args['measNum'] != 1)):
            logging.error('The file you are trying to convert is a VB file and it has only one measurement.')
            logging.error('You tried to convert measurement number: %d' % args['measNum'])
            return(ERR_STATE)


        parammap_file_content = getparammap_file_content(args['pMap'],args['user_map'],VBFILE)

        logging.info('This file contains %d measurement(s). ' % ParcRaidHead['count_'])

        ParcFileEntries = readParcFileEntries(siemens_dat,ParcRaidHead,VBFILE)

        # find the beginning of the desired measurement
        siemens_dat.seek(ParcFileEntries[args['measNum'] - 1]['off_'],os.SEEK_SET)

        dma_length,num_buffers = np.fromfile(siemens_dat,dtype=np.uint32,count=2)

        buffers = readMeasurementHeaderBuffers(siemens_dat,num_buffers)

        # We need to be on a 32 byte boundary after reading the buffers
        position_in_meas = siemens_dat.tell() - ParcFileEntries[args['measNum'] - 1]['off_']
        if np.mod(position_in_meas,32) != 0:
            siemens_dat.seek(32 - np.mod(position_in_meas,32),os.SEEK_CUR)

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

        # print(parammap_file_content)
        xml_config = readXmlConfig(args['debug'],parammap_file_content,num_buffers,buffers,wip_double,trajectory,dwell_time_0,max_channels,radial_views,baseLineString,protocol_name)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert Siemens raw data format to ISMRMRD format.')
    parser.add_argument('-v',dest='version',action='store_true',help='Prints converter version and ISMRMRD version')
    parser.add_argument('-f',dest='file',help='<SIEMENS dat file>')
    parser.add_argument('-z',dest='measNum',help='<Measurement number>',default=1,type=check_positive)
    parser.add_argument('-m',dest='pMap',help='<Parameter map XML file>')
    parser.add_argument('-x',dest='pMapStyle',help='<Parameter stylesheet XSL file>')
    parser.add_argument('--user-map',help='<Provide a parameter map XML file>')
    parser.add_argument('--user-stylesheet',help='<Provide a parameter stylesheet XSL file>')
    parser.add_argument('-o',dest='output',help='<ISMRMRD output file>',default='output.h5')
    parser.add_argument('-g',dest='outputGroup',help='<ISMRMRD output group>',default='dataset')
    parser.add_argument('-l',dest='list',action='store_true',help='<List embedded files>',default=True)
    parser.add_argument('-e',dest='extract',help='<Extract embedded file>')
    parser.add_argument('-X',dest='debug',help='<Debug XML flag>',default=True)
    parser.add_argument('-F',dest='flashPatRef',help='<FLASH PAT REF flag>',default=True)
    parser.add_argument('-H',dest='headerOnly',help='<HEADER ONLY flag (create xml header only)>',default=True)
    parser.add_argument('-B',dest='bufferAppend',help='<Append Siemens protocol buffers (bas64) to user parameters>',default=True)
    parser.add_argument('--studyDate',help='<User can supply study date, in the format of yyyy-mm-dd>')

    args = parser.parse_args()
    print(args)
    status = main(vars(args))
    if status == ERR_STATE:
        pass
