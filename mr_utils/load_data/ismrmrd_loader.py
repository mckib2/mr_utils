'''A sane ISMRMRD raw data file loader.'''

import numpy as np
import h5py
import xmltodict

def load_ismrmrd(filename, dataset='dataset'):
    '''Load data from ISMRM raw data format.

    Parameters
    ==========
    filename : str
        Path to raw data file.
    dataset : str, optional
        Name of the hdf5 dataset where ISMRM raw data is stored.

    Returns
    =======
    all_data : array_like
        Complex raw data in a numpy array for your pleasure.

    Raises
    ======
    NotImplementedError
        When a non-cartesian dataset is asked for.

    Notes
    =====
    Dimensions of returned data are:

        (navgs, nreps, ncontrasts, nslices, ncoils, eNz, eNy, eNx)

    Currently only Cartesian datasets are able to be unpacked.
    '''

    with h5py.File(filename, 'r') as f:
        # Let's pull out the header
        try:
            xmldict = xmltodict.parse(f[dataset]['xml'][0].decode())
        except AttributeError:
            # AttributeError: 'str' object has no attribute 'decode'
            xmldict = xmltodict.parse(f[dataset]['xml'][0])

        header = xmldict['ismrmrdHeader']

        # Make sure we can deal with the trajectory
        if header['encoding']['trajectory'] not in ['cartesian']:
            raise NotImplementedError('Only Cartesian datasets are supported!')

        # Grab all the necessary header information
        try:
            ncoils = int(header['acquisitionSystemInformation'][
                'receiverChannels'])
        except KeyError:
            ncoils = 1

        try:
            nslices = int(header['encoding']['encodingLimits']['slice'][
                'maximum']) + 1
        except KeyError:
            nslices = 1

        try:
            navgs = int(header['encoding']['encodingLimits']['average'][
                'maximum']) + 1
        except KeyError:
            navgs = 1

        try:
            nreps = int(header['encoding']['encodingLimits']['repetition'][
                'maximum']) + 1
        except KeyError:
            nreps = 1

        try:
            ncontrasts = int(header['encoding']['encodingLimits']['contrasts'][
                'maximum']) + 1
        except KeyError:
            ncontrasts = 1

        # Now grab the data
        keys = [
            'version', 'flags', 'measurement_uid', 'scan_counter',
            'acquisition_time_stamp', 'physiology_time_stamp',
            'number_of_samples', 'available_channels', 'active_channels',
            'channel_mask', 'discard_pre', 'discard_post', 'center_sample',
            'encoding_space_ref', 'trajectory_dimensions', 'sample_time_us',
            'position', 'read_dir', 'phase_dir', 'slice_dir',
            'patient_table_position', 'idx', 'user_int', 'user_float'
        ]
        data = f[dataset]['data']['data'][:]
        dhead = f[dataset]['data']['head'][:].squeeze()
        eNx = int(header['encoding']['encodedSpace']['matrixSize']['x'])
        eNy = int(header['encoding']['encodedSpace']['matrixSize']['y'])
        eNz = int(header['encoding']['encodedSpace']['matrixSize']['z'])
        all_data = np.zeros((navgs, nreps, ncontrasts, nslices, ncoils, eNz,
                             eNy, eNx), dtype=np.complex64)
        for ii, acq in np.ndenumerate(data):

            # Get params for this acq
            dhead0 = dict(zip(keys, list(dhead[ii])))
            avg = dhead0['idx']['average']
            rep = dhead0['idx']['repetition']
            contrast = dhead0['idx']['contrast']
            sl = dhead0['idx']['slice']
            y = dhead0['idx']['kspace_encode_step_1']
            z = dhead0['idx']['kspace_encode_step_2']
            a_chan = dhead0['active_channels']

            # Let's resize the acquisiton to fit into buffer
            acq0 = (acq[::2] + 1j*acq[1::2]).reshape((a_chan, eNx))

            # Stuff into the buffer
            all_data[avg, rep, contrast, sl, :, z, y, :] = acq0

        # Hand back the data the user
        return all_data

if __name__ == '__main__':
    pass
