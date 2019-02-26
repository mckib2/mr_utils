'''Unit tests for python port of siemens_to_ismrmrd.'''

import unittest
import unittest.mock
import io

from mr_utils.load_data import pyport
from mr_utils.test_data import bssfp_phantom

class PyPortTestCase(unittest.TestCase):
    '''Sanity check test cases.'''

    def setUp(self):
        self.sample = bssfp_phantom

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout(self, fun, args, expected_output, mock_stdout=None):
        '''Assertion function for writing to stdout.

        fun -- Function to run.
        args -- Arguments to pass to fun (dictionary).
        expected_output -- (string) What you hope to see from stdout.
        mock_stdout -- Used by @unittest.mock.patch, do not provide.
        '''
        fun(args)
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_display_version(self):
        '''Make sure we're displaying versions of stuffs.'''
        self.assert_stdout(pyport.main, {'version': True},
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
        self.assert_stdout(pyport.main, {'list': True}, out)

    def test_require_filename(self):
        '''If we don't have a filename, we need to stop!'''
        with self.assertRaises(ValueError):
            pyport.main({})
        with self.assertRaises(ValueError):
            pyport.main({'file': None})

    def test_is_filename_a_file(self):
        '''Make sure we can get to the file if given filename.'''
        with self.assertRaises(IOError):
            pyport.main({'file': 'this.is.a.fake.file.dat'})

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
