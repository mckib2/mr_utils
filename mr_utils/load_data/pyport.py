'''Python port of siemens_to_ismrmrd.

Notes:
    The XProtocol parser (xprot_get_val) is a string-search based
    implementation, not an actual parser, so it's really slow, but does get
    the job done very well.  Next steps would be to figure out how to speed
    this up or rewrite the parser to work with everything.  I was working on a
    parser but was stuck on how to handle some of Siemens' very strange
    syntax.

    There are several different XML libraries being used.  xml.etree was my
    preference, so that's what I started with.  I needed to use xmltodict to
    convert between dictionaries and xml, because it's quicker/easier to have
    a dictionary hold the config information as we move along.  It turns out
    that schema verification is not supported by xml.etree, so that's when I
    pulled in lxml.etree -- so there's some weirdness trying to get xml.etree
    and lxml.etree to play together nicely.  The last  one is pybx -- a
    bizarrely complicated library that the ismrmrd python library uses.  I hate
    the thing and think it's overly complicated for what we need to use it for.

    One of the ideas I had was to pull down the schema/parammaps from the
    interwebs so it would always be current.  While this is a neat feature that
    probably no one will use, it would speed up the raw data conversion to use
    a local copy instead, even if that means pulling it down the first time and
    keeping it.

    The script to read in an ismrmrd dset provided in ismrmrd-python-tools is
    great at illustrating how to do it, but is incredibly slow, especiailly if
    you want to remove oversampling in readout direction.  Next steps are to
    figure out how to quickly read in and process these datasets.  I'm kind of
    put off from using this data format because of how unweildy it is, but I
    suppose it's better to be an open standards player...

    The only datasets I have are cartesian VB17.  So there's currently little
    support for anything else.

    Command-line interface has not been looked at in a long time, might not be
    working still.
'''

import argparse
import os
import logging
import warnings
import xml.etree.ElementTree as ET
from ctypes import c_uint32

import numpy as np
import xmltodict
with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=FutureWarning)
    from ismrmrd import Dataset, xsd

from mr_utils.load_data.s2i import defs, sScanHeader, fill_ismrmrd_header
from mr_utils.load_data.s2i import readParcFileEntries, readScanHeader
from mr_utils.load_data.s2i import readMeasurementHeaderBuffers, parseXML
from mr_utils.load_data.s2i import readChannelHeaders, getAcquisition
from mr_utils.load_data.s2i import xml_fun, readXmlConfig

def pyport(version=False, list_embed=False, extract=None, user_stylesheet=None,
           file=None, pMapStyle=None, measNum=1, pMap=None, user_map=None,
           debug=False, header_only=False, output='output.h5',
           flash_pat_ref_scan=False, append_buffers=False,
           study_date_user_supplied=''):
    '''Run the program with arguments.'''

    # If we only wanted the version, that's all we're gonna do
    if version:
        print('Converter version is: %s.%s.%s' % (
            defs.SIEMENS_TO_ISMRMRD_VERSION_MAJOR,
            defs.SIEMENS_TO_ISMRMRD_VERSION_MINOR,
            defs.SIEMENS_TO_ISMRMRD_VERSION_PATCH))
        print('Built against ISMRMRD version: %s.%s.%s' % (
            defs.ISMRMRD_VERSION_MAJOR,
            defs.ISMRMRD_VERSION_MINOR,
            defs.ISMRMRD_VERSION_PATCH))
        return None

    # Embedded files are parameter maps and stylesheets included with this
    # program
    if list_embed:
        print('Embedded Files:')
        for f in sorted(xml_fun.get_list_of_embedded_files()):
            print('\t%s' % f)
        return None

    # Extract specified parameter map if requested
    if extract is not None:
        # Make everything look like a list so we can iterate over it
        if not isinstance(extract, list):
            extract = [extract]

        # Save the files!
        for paramMap in extract:
            # will raise ValueError if file not valid!
            xml = xml_fun.get_embedded_file(paramMap)

            # For now just print it out
            print(ET.tostring(xml).decode())
        return None

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
            parammap_xsl_content = xml_fun.get_embedded_file(
                'IsmrmrdParameterMap_Siemens.xsl') # this is XML
        else:
            if os.path.isfile(user_stylesheet):
                parammap_xsl_content = xml_fun.get_embedded_file(
                    user_stylesheet)
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
    schema_file_name_content = xml_fun.get_ismrmrd_schema() # this is XML

    # Now let's get to the dirty work...
    with open(file, 'br') as siemens_dat:

        VBFILE = False
        ParcRaidHead = {}
        ParcRaidHead['hdSize_'], ParcRaidHead['count_'] = np.fromfile(
            siemens_dat, dtype=c_uint32, count=2)

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


        parammap_file_content = xml_fun.getparammap_file_content(
            pMap, user_map, VBFILE)

        logging.info('This file contains %d measurement(s). ',
                     ParcRaidHead['count_'])

        ParcFileEntries = readParcFileEntries(
            siemens_dat, ParcRaidHead, VBFILE)

        # find the beginning of the desired measurement
        siemens_dat.seek(ParcFileEntries[measNum - 1]['off_'], os.SEEK_SET)

        dma_length, num_buffers = np.fromfile(
            siemens_dat, dtype=c_uint32, count=2)

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

        # For debugging purposes, let's go ahead and kill it first instead of
        # appending - that led to some weirdness...
        if os.path.isfile('tmp.h5'):
            msg = 'TMP file already exists!  Removing and creating anew!'
            logging.warning(msg)
            os.remove('tmp.h5')
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
        sScanSize = sScanHeader.itemsize
        while (not last_mask & 1) and (((pfe['off_'] + pfe['len_']) \
                - siemens_dat.tell()) > sScanSize):


            position_in_meas = siemens_dat.tell()
            scanhead, _mdh = readScanHeader(siemens_dat, VBFILE)
            # mdh.display()

            if not siemens_dat:
                logging.error(
                    'Error reading header at acquisition %d.', acquisitions)
                break


            dma_length = \
                scanhead['ulFlagsAndDMALength'] & defs.MDH_DMA_LENGTH_MASK
            _mdh_enable_flags = \
                scanhead['ulFlagsAndDMALength'] & defs.MDH_ENABLE_FLAGS_MASK

            # Check if this is sync data, if so, it must be handled differently
            if scanhead['aulEvalInfoMask'][0] & (1 << 5):
                print('dma_length = %d' % dma_length)
                print('sync_data_packets = %d' % sync_data_packets)
                raise NotImplementedError()
                # last_scan_counter = acquisitions - 1
                # # TODO:
                # # auto waveforms = readSyncdata(siemens_dat, VBFILE,
                #  acquisitions, dma_length,scanhead,header,last_scan_counter);
                # # for (auto& w : waveforms)
                # #     ismrmrd_dataset->appendWaveform(w);
                # sync_data_packets += 1
                # continue

            if first_call:
                time_stamp = scanhead['ulTimeStamp']

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
                    return None
                ## Create an ISMRMRD dataset

            # This check only makes sense in VD line files.
            if not VBFILE and (scanhead['lMeasUID'] != pfe['measId_']):
                # Something must have gone terribly wrong. Bail out.
                if first_call:
                    msg = ('Corrupted or retro-recon dataset detected '
                           '(scanhead.lMeasUID != ParcFileEntries[%d].measId_'
                           'Fix the scanhead.lMeasUID...' % (measNum-1))
                    logging.error(msg)
                scanhead['lMeasUID'] = pfe['measId_']

            if first_call:
                first_call = False

            # Allocate data for channels
            channels = readChannelHeaders(siemens_dat, VBFILE, scanhead)

            if not siemens_dat:
                msg = 'Error reading data at acqusition %s' % acquisitions
                logging.error(msg)
                break

            acquisitions += 1
            last_mask = scanhead['aulEvalInfoMask'][0]
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

        # ismrmrd_dataset.write_xml_header(xmltodict.unparse(dict_config))
        # THIS IS THE WRONG HEADER!  Only doing this because we can't get
        # the ISMRMRD object to load it if we try to make our own.  Might be
        # some funkiness with pyxb vs letree vs etree...
        ismrmrd_dataset.write_xml_header(header.toxml())

        # Mystery bytes. There seems to be 160 mystery bytes at the end of the
        # data.
        mystery_bytes = (pfe['off_'] + pfe['len_']) - siemens_dat.tell()

        if mystery_bytes > 0:
            if mystery_bytes != defs.MYSTERY_BYTES_EXPECTED:
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
                        default=1)
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
