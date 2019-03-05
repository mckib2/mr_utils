'''Unit tests for python port of siemens_to_ismrmrd.'''

import unittest
import unittest.mock
import io
import xml.etree.ElementTree as ET

from mr_utils.load_data import pyport
from mr_utils.load_data.pyport import get_embedded_file

class PyPortTestCase(unittest.TestCase):
    '''Sanity check test cases.'''

    def setUp(self):
        self.emptydat = 'mr_utils/tests/load_data/empty.dat'
        self.sample = 'mr_utils/tests/load_data/test.dat'

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, fun, args, expected_output, mock_stdout=None):
        '''Assertion function for writing to stdout.

        fun -- Function to run.
        args -- Arguments to pass to fun (dictionary).
        expected_output -- (string) What you hope to see from stdout.
        mock_stdout -- Used by @unittest.mock.patch, do not provide.
        '''
        fun(**args)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_display_version(self):
        '''Make sure we're displaying versions of stuffs.'''
        self.assert_stdout(pyport, {'version': True},
                           ('Converter version is: 1.0.1\nBuilt against '
                            'ISMRMRD version: 0.0.0\n'))

    def test_display_embedded_files(self):
        '''Make sure we display list of embedded files.'''
        out = ('Embedded Files:\n\t'
               'IsmrmrdParameterMap.xml\n\t'
               'IsmrmrdParameterMap.xsl\n\tIsmrmrdParameterMap_Siemens.xml\n\t'
               'IsmrmrdParameterMap_Siemens.xsl\n\t'
               'IsmrmrdParameterMap_Siemens_EPI.xsl\n\t'
               'IsmrmrdParameterMap_Siemens_EPI_FLASHREF.xsl\n\t'
               'IsmrmrdParameterMap_Siemens_PreZeros.xsl\n\t'
               'IsmrmrdParameterMap_Siemens_T1Mapping_SASHA.xsl\n\t'
               'IsmrmrdParameterMap_Siemens_VB17.xml\n')
        self.assert_stdout(pyport, {'list_embed': True}, out)

    def test_extract_single_file(self):
        '''Make sure we can save file if the user wants it.'''
        embedded_file = 'IsmrmrdParameterMap_Siemens.xml'
        xml = get_embedded_file(embedded_file)
        self.assert_stdout(pyport,
                           {'extract': embedded_file},
                           ET.tostring(xml).decode() + '\n')

    def test_extract_file_not_valid(self):
        '''Make sure we raise an error when embedded file is not valid.'''
        with self.assertRaises(ValueError):
            pyport(extract='myFile.xml')

    def test_extract_many_files(self):
        '''Make sure we can handle saving multiple files.'''
        embedded_files = ['IsmrmrdParameterMap.xml', 'IsmrmrdParameterMap.xsl']
        xml0 = ET.tostring(get_embedded_file(embedded_files[0])).decode()
        xml1 = ET.tostring(get_embedded_file(embedded_files[1])).decode()
        self.assert_stdout(
            pyport, {'extract': embedded_files},
            xml0 + '\n' + xml1 + '\n')

    def test_require_filename(self):
        '''If we don't have a filename, we need to stop!'''
        with self.assertRaises(ValueError):
            pyport()
        with self.assertRaises(ValueError):
            pyport(file=None)

    def test_invalid_user_style_sheet(self):
        '''Make sure we raise an exception if user stylesheet is not valud.'''
        with self.assertRaises(IOError):
            pyport(file=self.emptydat, user_stylesheet='myFile.xsl')

    def test_supplied_user_style_sheet_and_pMapStyle(self):
        '''Make sure we can't supply a param map AND an embedded file.'''
        with self.assertRaises(ValueError):
            pyport(file=self.emptydat, pMapStyle='file.xsl',
                   user_stylesheet='file.xml')

    def test_invalid_pmapstyle(self):
        '''Make sure we break on invalid pMapStyle.'''
        with self.assertRaises(IOError):
            pyport(file=self.emptydat, pMapStyle='invalidfile')

    def test_bssfp_data(self):
        '''Sample bSSFP data set.'''
        dset = pyport(file=self.sample, debug=False)

        import numpy as np
        import ismrmrd
        import ismrmrd.xsd

        from ismrmrdtools import show, transform

        header = ismrmrd.xsd.CreateFromDocument(dset.read_xml_header())
        enc = header.encoding[0]

        # Matrix size
        eNx = enc.encodedSpace.matrixSize.x
        eNy = enc.encodedSpace.matrixSize.y
        eNz = enc.encodedSpace.matrixSize.z
        rNx = enc.reconSpace.matrixSize.x
        _rNy = enc.reconSpace.matrixSize.y
        _rNz = enc.reconSpace.matrixSize.z

        # Field of View
        _eFOVx = enc.encodedSpace.fieldOfView_mm.x
        _eFOVy = enc.encodedSpace.fieldOfView_mm.y
        _eFOVz = enc.encodedSpace.fieldOfView_mm.z
        _rFOVx = enc.reconSpace.fieldOfView_mm.x
        _rFOVy = enc.reconSpace.fieldOfView_mm.y
        _rFOVz = enc.reconSpace.fieldOfView_mm.z

        # Number of Slices, Reps, Contrasts, etc.
        ncoils = header.acquisitionSystemInformation.receiverChannels
        if enc.encodingLimits.slice is not None:
            nslices = enc.encodingLimits.slice.maximum + 1
        else:
            nslices = 1

        if enc.encodingLimits.repetition is not None:
            nreps = enc.encodingLimits.repetition.maximum + 1
        else:
            nreps = 1

        if enc.encodingLimits.contrast is not None:
            ncontrasts = enc.encodingLimits.contrast.maximum + 1
        else:
            ncontrasts = 1

        # TODO loop through the acquisitions looking for noise scans
        firstacq = 0
        for acqnum in range(dset.number_of_acquisitions()):
            acq = dset.read_acquisition(acqnum)

            # TODO: Currently ignoring noise scans
            if acq.isFlagSet(ismrmrd.ACQ_IS_NOISE_MEASUREMENT):
                print("Found noise scan at acq ", acqnum)
                continue
            else:
                firstacq = acqnum
                print("Imaging acquisition starts acq ", acqnum)
                break


        # Initialiaze a storage array
        all_data = np.zeros(
            (nreps, ncontrasts, nslices, ncoils, eNz, eNy, rNx),
            dtype=np.complex64)

        # Loop through the rest of the acquisitions and stuff
        for acqnum in range(firstacq, dset.number_of_acquisitions()):
            acq = dset.read_acquisition(acqnum)

            # TODO: this is where we would apply noise pre-whitening

            # Remove oversampling if needed
            if eNx != rNx:
                xline = transform.transform_kspace_to_image(acq.data, [1])
                x0 = int((eNx - rNx) / 2)
                x1 = int((eNx - rNx) / 2 + rNx)
                xline = xline[:, x0:x1]
                acq.resize(rNx, acq.active_channels, acq.trajectory_dimensions)
                acq.center_sample = int(rNx/2)
                # need to use the [:] notation here to fill the data
                acq.data[:] = transform.transform_image_to_kspace(xline, [1])

            # Stuff into the buffer
            rep = acq.idx.repetition
            contrast = acq.idx.contrast
            slice = acq.idx.slice
            y = acq.idx.kspace_encode_step_1
            z = acq.idx.kspace_encode_step_2
            all_data[rep, contrast, slice, :, z, y, :] = acq.data

        # Reconstruct images
        images = np.zeros(
            (nreps, ncontrasts, nslices, eNz, eNy, rNx), dtype=np.float32)
        for rep in range(nreps):
            for contrast in range(ncontrasts):
                for slice in range(nslices):
                    # FFT
                    if eNz > 1:
                        #3D
                        im = transform.transform_kspace_to_image(
                            all_data[rep, contrast, slice, ...], [1, 2, 3])
                    else:
                        #2D
                        im = transform.transform_kspace_to_image(
                            all_data[rep, contrast, slice, :, 0, ...], [1, 2])

                    # Sum of squares
                    im = np.sqrt(np.sum(np.abs(im) ** 2, 0))

                    # Stuff into the output
                    if eNz > 1:
                        #3D
                        images[rep, contrast, slice, ...] = im
                    else:
                        #2D
                        images[rep, contrast, slice, 0, ...] = im

        # Show an image
        show.imshow(np.squeeze(images[0, 0, 0, ...]))


    # def test_pyport(self):
    #     '''Standard parameters with bSSFP data set.'''
    #
    #     args = {
    #         'version': False,
    #         'list': True,
    #         'extract': None,
    #         'user_stylesheet': None,
    #         'file': self.sample,
    #         'pMapStyle': None,
    #         'measNum': 1,
    #         'pMap': None,
    #         'user_map': None,
    #         'debug': False
    #     }
    #
    #     pyport.main(args)

if __name__ == '__main__':
    unittest.main()
