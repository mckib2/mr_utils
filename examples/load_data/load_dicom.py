'''Example of how to load dicom files.

Requirements
------------
- python3 (I haven't tested python2.7)
- numpy
- matplotlib
- requests
- pydicom
- nibabel
- Internet connection

Notes
-----
This example uses two methods from two different libraries:
- pydicom
- nibabel

These are the easiest ways I know of, could be better ways.  Docs for
both of these libraries are easy use, go take a look!

I will mention the warning on nibabel's dicom reader utilities --
they say they are still "highly experimental" -- so probably stick
with pydicom unless you need nifti for any pre-/postprocessing.
'''

import shutil
import os

import numpy as np
import matplotlib.pyplot as plt
import requests
import pydicom
from nibabel.nicom.dicomwrappers import wrapper_from_file

if __name__ == '__main__':

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_DATA_HOST = 'https://birly.groups.et.byu.net/'

    # First grab the dicom.  It could be any dicom, but for this example we'll
    # grab on a server somewhere deep in the heart of Utah...
    web_path = 'mr_utils/test_data/examples/load_data/'
    file = 'IM-0013-0148.dcm'
    filename = '%s/%s' % (ROOT_DIR, file)
    print('Looking for %s...' % filename)
    if not os.path.isfile(filename):
        # If the dicom file doesn't exist locally, then download it
        print('Couldn\'t find it, looking on the server!')
        url = '%s/%s/%s' % (TEST_DATA_HOST, web_path, file)
        try:
            with requests.get(url, stream=True) as r:
                print('Starting download...')
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            print('Done downloading file!')
        except OSError:
            raise OSError('Whoops! Network problems, try again!')
    print('%s exists!' % filename)

    # Now we have a dicom we can work with.  Let's try loading it with
    # pydicom, the obvious choice
    pydicom_dataset = pydicom.dcmread(filename)
    im0 = pydicom_dataset.pixel_array

    # prove it's numpy array
    assert isinstance(im0, np.ndarray), 'I should be a numpy array!'

    # Let's visually inspect it -- looks good!
    plt.imshow(im0, cmap='gray')
    plt.title('Look at me! I\'m a numpy array!')
    plt.show()

    # Now let's try it a little different -- use nibabel!
    nibabel_dataset = wrapper_from_file(filename)
    im1 = nibabel_dataset.get_pixel_array()

    # Prove it's a numpy array
    assert isinstance(im1, np.ndarray), 'I should be a numpy array!'

    # Again, take a look:
    plt.imshow(im1, cmap='gray')
    plt.title('Look at me! I came from a nifti library!')
    plt.show()

    # Prove that we get the same data either way:
    assert np.all(im0 == im1), (
        'I should have loaded the same data both times!')
