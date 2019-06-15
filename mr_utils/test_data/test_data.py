'''Provide an interface to load test data for unit tests.
'''

import shutil
import os
from pathlib import Path

import numpy as np
import requests

from mr_utils.definitions import TEST_DATA_HOST, ROOT_DIR

def load_test_data(path, files, do_return=True):
    '''Load test data, download if necessary.

    Parameters
    ----------
    path : str
        Location of directory where the test files live.
    files : list
        Specific files to return.
    do_return : bool
        Whether or not to return loaded files as a list.

    Returns
    -------
    returnVals : list
        List of files loaded using np.load.
    None, optional
        Files are downloaded to disk, but not loaded.

    Notes
    -----
    files should be a list.  If no extension is given, .npy will be
    assumed. do_return=True assumes .npy file will be loaded (uses
    numpy.load).
    '''

    returnVals = []
    for file in files:
        # What's the extension?
        if not Path(file).suffix:
            # assume we're looking for the default .npy file
            file += '.npy'

        # Make sure we're starting from where we want to
        if not os.path.isfile(
                '%s/%s' % (path, file)) and not os.path.isabs(path):
            path0 = '%s/%s' % (ROOT_DIR, path)
        else:
            path0 = path

        try:
            if do_return:
                localpath = '%s/%s' % (path0, file)
                returnVals.append(do_return_fun(localpath))
            else:
                # We just need to make sure that it exists
                with open('%s/%s' % (path0, file), 'rb') as f:
                    pass
        except IOError as _e:
            # Try downloading the file, doesn't exist locally
            url = '%s/%s/%s' % (TEST_DATA_HOST, path, file)
            filename = '%s/%s' % (path0, file)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with requests.get(url, stream=True) as r:
                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            if do_return:
                localpath = '%s/%s' % (path0, file)
                returnVals.append(do_return_fun(localpath))
    if do_return:
        return returnVals[:]
    return None

def do_return_fun(localpath):
    '''Get file to return.'''

    if Path(localpath).suffix == '.dcm':
        from mr_utils.load_data import load_dicom
        return load_dicom(localpath)
    return np.load(localpath)

# ## XPROT FILES
# # For xprot_parser
# class XProtParserTest(object):
#
#     @staticmethod
#     def sample_xprot():
#         path = str(Path('mr_utils/test_data/tests/load_data/sample.xprot').resolve())
#         with open(path,'r') as f:
#             data = f.read()
#         return(data)
#
#     @staticmethod
#     def full_sample_xprot():
#         path = str(Path('mr_utils/test_data/tests/load_data/full_sample.xprot').resolve())
#         with open(path,'r') as f:
#             data = f.read()
#         return(data)

# ## HDF5 FILES
# # For gadgetron
# class GadgetronClient(object):
#
#     @staticmethod
#     def true_output_data():
#         path = str(Path('mr_utils/test_data/tests/gadgetron/client/true_output').resolve())
#         with h5py.File(path,'r') as f:
#             data = f['2018-11-02 20:35:19.785688']['image_0']['data'][:]
#         return(data)
#
#     @staticmethod
#     def input_filename():
#         path = str(Path('mr_utils/test_data/tests/gadgetron/client/input.h5').resolve())
#         return(path)
#
#     @staticmethod
#     def input_h5():
#         path = GadgetronClient.input_filename()
#         data = ismrmrd.Dataset(path,'dataset',False)
#         return(data)
#
#     @staticmethod
#     def raw_input_filename():
#         path = str(Path('mr_utils/test_data/tests/gadgetron/client/input.dat').resolve())
#         return(path)
#
#     @staticmethod
#     def grappa_input_filename():
#         path = str(Path('mr_utils/test_data/tests/gadgetron/client/grappa_test_data.h5').resolve())
#         return(path)
#
#     @staticmethod
#     def true_output_data_grappa_cpu():
#         path = str(Path('mr_utils/test_data/tests/gadgetron/client/true_output_data_grappa_cpu.npy').resolve())
#         data = np.load(path)
#         return(data)
#
#     @staticmethod
#     def epi_input_filename():
#         '''Gadgetron test data.
#         http://gadgetrondata.blob.core.windows.net/gadgetrontestdata/epi/epi_2d_out_20161020_pjv.h5
#         '''
#         path = str(Path('mr_utils/test_data/tests/gadgetron/client/epi_2d_out_20161020_pjv.h5').resolve())
#         return(path)
#
#     @staticmethod
#     def generic_cartesian_grappa_filename():
#         '''Gadgetron test data.
#         http://gadgetrondata.blob.core.windows.net/gadgetrontestdata/tse/meas_MID00450_FID76726_SAX_TE62_DIR_TSE/ref_20160319.dat
#         '''
#         path = str(Path('mr_utils/test_data/tests/gadgetron/client/meas_MID00450_FID76726_SAX_TE62_DIR_TSE.dat').resolve())
#         return(path)
#
#
#     # @staticmethod
#     # def epi_raw_input_filename():
#     #     '''Gadgetron test data.
#     #     http://gadgetrondata.blob.core.windows.net/gadgetrontestdata/epi_ave/meas_MID01349_FID12150_amri_ep2d_bold_96x72x5_R2_16avg_gadgetron.dat
#     #     '''
#     #     path = str(Path('mr_utils/test_data/tests/gadgetron/client/meas_MID01349_FID12150_amri_ep2d_bold_96x72x5_R2_16avg_gadgetron.dat').resolve())
#     #     return(path)
#
# ## NPY FILES
# # For ssfp multiphase:
# class SSFPMultiphase(object):
#
#     @staticmethod
#     def ssfp_ankle_te_6_pc_0():
#         path_0 = str(Path('mr_utils/test_data/tests/recon/ssfp/ssfp_ankle_te_6_pc_0.npy').resolve())
#         data = np.load(path_0)
#         return(data)
#
#     def ssfp_ankle_te_6_pc_90():
#         path_90 = str(Path('mr_utils/test_data/tests/recon/ssfp/ssfp_ankle_te_6_pc_90.npy').resolve())
#         data = np.load(path_90)
#         return(data)
#
#     def ssfp_ankle_te_6_pc_180():
#         path_180 = str(Path('mr_utils/test_data/tests/recon/ssfp/ssfp_ankle_te_6_pc_180.npy').resolve())
#         data = np.load(path_180)
#         return(data)
#
# # For VIEW testing:
# class ViewTestData(object):
#
#     @staticmethod
#     def ssfp_ankle_te_6_pc_0():
#         path = str(Path('mr_utils/test_data/tests/recon/ssfp/ssfp_ankle_te_6_pc_0.npy').resolve())
#         return(path)
#
# # For BART reordering recon
# class BARTReordering(object):
#
#     @staticmethod
#     def ksp_sim():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/bart/ksp_sim.npy').resolve())
#         data = np.load(path)
#         return(data)
#
#     @staticmethod
#     def lowres_img():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/bart/lowres_img.npy').resolve())
#         data = np.load(path)
#         return(data)
#
#     @staticmethod
#     def lowres_ksp():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/bart/lowres_ksp.npy').resolve())
#         data = np.load(path)
#         return(data)
#
#     @staticmethod
#     def reco1():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/bart/reco1.npy').resolve())
#         data = np.load(path)
#         return(data)
#
#     @staticmethod
#     def reco2():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/bart/reco2.npy').resolve())
#         data = np.load(path)
#         return(data)
#
#     @staticmethod
#     def sens():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/bart/sens.npy').resolve())
#         data = np.load(path)
#         return(data)
#
#     @staticmethod
#     def traj_rad2():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/bart/traj_rad2.npy').resolve())
#         data = np.load(path)
#         return(data)
#
# ## MAT FILES

# # For scr_reordering_adluru:
# class SCRReordering(object):
#
#     @staticmethod
#     def Coil1_data():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/Coil1_data.mat').resolve())
#         return(load_mat(path,'Coil1'))
#
#     @staticmethod
#     def mask():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/mask.mat').resolve())
#         return(load_mat(path,'mask'))
#
#     @staticmethod
#     def tv_prior():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/tv_prior.mat').resolve())
#         return(load_mat(path,'tv_prior'))
#
#     @staticmethod
#     def recon():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/recon.mat').resolve())
#         return(load_mat(path,'img_est'))
#
#     @staticmethod
#     def true_orderings():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/true_orderings.mat').resolve())
#
#         # offset by 1 since MATLAB is 1-based indexing
#         orderings = load_mat(path)
#         sort_order_real_x = orderings['sort_order_real_x'] - 1
#         sort_order_imag_x = orderings['sort_order_imag_x'] - 1
#         sort_order_real_y = orderings['sort_order_real_y'] - 1
#         sort_order_imag_y = orderings['sort_order_imag_y'] - 1
#
#         return(sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y)
#
#     @staticmethod
#     def TV_re_order():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/TV_re_order.mat').resolve())
#         data = load_mat(path)
#         a = data['TV_term_reorder_update_real']
#         b = data['TV_term_reorder_update_imag']
#         return(a,b)
#
#     @staticmethod
#     def TV_term_update():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/TV_term_update.mat').resolve())
#         return(load_mat(path,'TV_term_update'))
#
#     @staticmethod
#     def fidelity_update():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/fidelity_update.mat').resolve())
#         return(load_mat(path,'fidelity_update'))
#
#     @staticmethod
#     def recon_at_iter_100():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_100.mat').resolve())
#         return(load_mat(path,'img_est'))
#
#     @staticmethod
#     def recon_at_iter_1():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_1.mat').resolve())
#         return(load_mat(path,'img_est'))
#
#     @staticmethod
#     def recon_at_iter_2():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_2.mat').resolve())
#         return(load_mat(path,'img_est'))
#
#     @staticmethod
#     def recon_at_iter_10():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_10.mat').resolve())
#         return(load_mat(path,'img_est'))
#
#     @staticmethod
#     def recon_at_iter_50():
#         path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_50.mat').resolve())
#         return(load_mat(path,'img_est'))

# # For GRAPPA Recon
# class GRAPPA(object):

#     @staticmethod
#     def phantom_ch_k():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_1_k.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_2_k.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_3_k.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_4_k.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_5_k.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_6_k.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         kspace = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(kspace)
#
#     @staticmethod
#     def phantom_ch_k_u():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_1_k_u.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_2_k_u.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_3_k_u.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_4_k_u.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_5_k_u.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_6_k_u.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         kspace = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(kspace)
#
#     @staticmethod
#     def phantom_ch_k_acl():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_1_k_acl.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_2_k_acl.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_3_k_acl.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_4_k_acl.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_5_k_acl.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_6_k_acl.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         kspace = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(kspace)
#
#     @staticmethod
#     def S_ch_temp():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1_temp.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2_temp.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3_temp.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4_temp.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5_temp.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6_temp.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(S0)
#
#     @staticmethod
#     def S_ch():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(S0)
#
#     @staticmethod
#     def S():
#         path = str(Path('mr_utils/test_data/tests/recon/grappa/S.npy').resolve())
#         S0 = np.load(path)
#         return(S0)
#
#     @staticmethod
#     def T():
#         path = str(Path('mr_utils/test_data/tests/recon/grappa/T.npy').resolve())
#         T0 = np.load(path)
#         return(T0)
#
#     @staticmethod
#     def W():
#         path = str(Path('mr_utils/test_data/tests/recon/grappa/W.npy').resolve())
#         W0 = np.load(path)
#         return(W0)
#
#     @staticmethod
#     def S_ch_new_temp():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1_new_temp.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2_new_temp.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3_new_temp.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4_new_temp.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5_new_temp.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6_new_temp.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(S0)
#
#     @staticmethod
#     def S_ch_new():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1_new.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2_new.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3_new.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4_new.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5_new.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6_new.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(S0)
#
#     @staticmethod
#     def S_new():
#         path = str(Path('mr_utils/test_data/tests/recon/grappa/S_new.npy').resolve())
#         S0 = np.load(path)
#         return(S0)
#
#     @staticmethod
#     def T_new():
#         path = str(Path('mr_utils/test_data/tests/recon/grappa/T_new.npy').resolve())
#         T0 = np.load(path)
#         return(T0)
#
#     @staticmethod
#     def T_ch_new_M():
#         path1 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_1_new_M.npy').resolve())
#         path2 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_2_new_M.npy').resolve())
#         path3 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_3_new_M.npy').resolve())
#         path4 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_4_new_M.npy').resolve())
#         path5 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_5_new_M.npy').resolve())
#         path6 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_6_new_M.npy').resolve())
#         ch1 = np.load(path1)
#         ch2 = np.load(path2)
#         ch3 = np.load(path3)
#         ch4 = np.load(path4)
#         ch5 = np.load(path5)
#         ch6 = np.load(path6)
#         T0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
#         return(T0)
#
#     @staticmethod
#     def Im_Recon():
#         path = str(Path('mr_utils/test_data/tests/recon/grappa/Im_Recon.npy').resolve())
#         recon = np.load(path)
#         return(recon)
