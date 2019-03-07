'''readXmlConfig'''

import logging

from mr_utils.load_data.s2i import xprot_get_val, ProcessParameterMap

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
