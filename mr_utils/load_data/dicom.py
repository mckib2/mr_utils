'''Load data from DICOM file.'''

import pydicom

def load_dicom(filename):
    '''Load DICOM data from file.

    Parameters
    ----------
    filename : str
        Path to DICOM file.
    '''

    return pydicom.dcmread(filename).pixel_array
