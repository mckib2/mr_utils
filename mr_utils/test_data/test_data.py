from pathlib import Path
from mr_utils.load_data import load_mat
import numpy as np
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import h5py
    import ismrmrd

## DAT FILES
bssfp_phantom = str(Path('mr_utils/test_data/raw/bssfp_phantom.dat').resolve())

# For Single Voxel Simulation
single_voxel_512 = str(Path('mr_utils/test_data/tests/sim/single_voxel/single_voxel_512.dat').resolve())
single_voxel_256_0 = str(Path('mr_utils/test_data/tests/sim/single_voxel/single_voxel_256_0.dat').resolve())
single_voxel_256_1 = str(Path('mr_utils/test_data/tests/sim/single_voxel/single_voxel_256_1.dat').resolve())

## XPROT FILES
# For xprot_parser
class XProtParserTest(object):

    @staticmethod
    def sample_xprot():
        path = str(Path('mr_utils/test_data/tests/load_data/sample.xprot').resolve())
        with open(path,'r') as f:
            data = f.read()
        return(data)

    @staticmethod
    def full_sample_xprot():
        path = str(Path('mr_utils/test_data/tests/load_data/full_sample.xprot').resolve())
        with open(path,'r') as f:
            data = f.read()
        return(data)

## XML FILES
# For gadgetron
class GadgetronTestConfig(object):

    @staticmethod
    def default_config():
        path = str(Path('mr_utils/test_data/tests/gadgetron/config/default.xml').resolve())
        with open(path,'r') as f:
            data = f.read()
        return(data)

## HDF5 FILES
# For gadgetron
class GadgetronClient(object):

    @staticmethod
    def true_output_data():
        path = str(Path('mr_utils/test_data/tests/gadgetron/client/true_output').resolve())
        with h5py.File(path,'r') as f:
            data = f['2018-11-02 20:35:19.785688']['image_0']['data'][:]
        return(data)

    @staticmethod
    def input_filename():
        path = str(Path('mr_utils/test_data/tests/gadgetron/client/input.h5').resolve())
        return(path)

    @staticmethod
    def input_h5():
        path = GadgetronClient.input_filename()
        data = ismrmrd.Dataset(path,'dataset',False)
        return(data)

    @staticmethod
    def raw_input_filename():
        path = str(Path('mr_utils/test_data/tests/gadgetron/client/input.dat').resolve())
        return(path)

## NPY FILES
# For ssfp multiphase:
class SSFPMultiphase(object):

    @staticmethod
    def ssfp_ankle_te_6_pc_0():
        path_0 = str(Path('mr_utils/test_data/tests/recon/ssfp/ssfp_ankle_te_6_pc_0.npy').resolve())
        data = np.load(path_0)
        return(data)

    def ssfp_ankle_te_6_pc_90():
        path_90 = str(Path('mr_utils/test_data/tests/recon/ssfp/ssfp_ankle_te_6_pc_90.npy').resolve())
        data = np.load(path_90)
        return(data)

    def ssfp_ankle_te_6_pc_180():
        path_180 = str(Path('mr_utils/test_data/tests/recon/ssfp/ssfp_ankle_te_6_pc_180.npy').resolve())
        data = np.load(path_180)
        return(data)

## MAT FILES
# For SC-GROG:
class SCGROG(object):

    @staticmethod
    def test_grog_data_4D():
        path = str(Path('mr_utils/test_data/tests/gridding/scgrog/test_grog_data_4D.mat').resolve())
        data = load_mat(path)
        traj = data['testTrajectory3D']
        kspace = data['testData4D']
        return(kspace,traj)

    @staticmethod
    def gx_gy_results():
        path = str(Path('mr_utils/test_data/tests/gridding/scgrog/gx_gy_results.mat').resolve())
        data = load_mat(path)
        Gxm = data['officialGx']
        Gym = data['officialGy']
        return(Gxm,Gym)

    @staticmethod
    def test_gridder_data_4D():
        path = str(Path('mr_utils/test_data/tests/gridding/scgrog/test_gridder_data_4D.mat').resolve())
        data = load_mat(path,'KSpaceData')
        kspace = data['kSpace'][0][0]
        traj = data['trajectory'][0][0]
        cartdims = tuple(list(data['cartesianSize'][0][0][0]))
        return(kspace,traj,cartdims)

    @staticmethod
    def test_gx_gy_data():
        path = str(Path('mr_utils/test_data/tests/gridding/scgrog/test_gx_gy_data.mat').resolve())
        data = load_mat(path)
        Gxm = data['Gx']
        Gym = data['Gy']
        return(Gxm,Gym)

    @staticmethod
    def grog_result():
        path = str(Path('mr_utils/test_data/tests/gridding/scgrog/grog_result.mat').resolve())
        data = load_mat(path)
        kspacem = data['officialCartesianKSpace']
        maskm = data['officialKMask']
        return(kspacem,maskm)

# For scr_reordering_adluru:
class SCRReordering(object):

    @staticmethod
    def Coil1_data():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/Coil1_data.mat').resolve())
        return(load_mat(path,'Coil1'))

    @staticmethod
    def mask():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/mask.mat').resolve())
        return(load_mat(path,'mask'))

    @staticmethod
    def tv_prior():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/tv_prior.mat').resolve())
        return(load_mat(path,'tv_prior'))

    @staticmethod
    def recon():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/recon.mat').resolve())
        return(load_mat(path,'img_est'))

    @staticmethod
    def true_orderings():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/true_orderings.mat').resolve())

        # offset by 1 since MATLAB is 1-based indexing
        orderings = load_mat(path)
        sort_order_real_x = orderings['sort_order_real_x'] - 1
        sort_order_imag_x = orderings['sort_order_imag_x'] - 1
        sort_order_real_y = orderings['sort_order_real_y'] - 1
        sort_order_imag_y = orderings['sort_order_imag_y'] - 1

        return(sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y)

    @staticmethod
    def TV_re_order():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/TV_re_order.mat').resolve())
        data = load_mat(path)
        a = data['TV_term_reorder_update_real']
        b = data['TV_term_reorder_update_imag']
        return(a,b)

    @staticmethod
    def TV_term_update():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/TV_term_update.mat').resolve())
        return(load_mat(path,'TV_term_update'))

    @staticmethod
    def fidelity_update():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/fidelity_update.mat').resolve())
        return(load_mat(path,'fidelity_update'))

    @staticmethod
    def recon_at_iter_100():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_100.mat').resolve())
        return(load_mat(path,'img_est'))

    @staticmethod
    def recon_at_iter_1():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_1.mat').resolve())
        return(load_mat(path,'img_est'))

    @staticmethod
    def recon_at_iter_2():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_2.mat').resolve())
        return(load_mat(path,'img_est'))

    @staticmethod
    def recon_at_iter_10():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_10.mat').resolve())
        return(load_mat(path,'img_est'))

    @staticmethod
    def recon_at_iter_50():
        path = str(Path('mr_utils/test_data/tests/recon/reordering/recon_at_iter_50.mat').resolve())
        return(load_mat(path,'img_est'))

# For elliptical signal model:
class EllipticalSignal(object):
    @staticmethod
    def I1():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/I1.mat').resolve())
        return(load_mat(path,key='I1'))

    @staticmethod
    def I2():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/I2.mat').resolve())
        return(load_mat(path,key='I2'))

    @staticmethod
    def I3():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/I3.mat').resolve())
        return(load_mat(path,key='I3'))

    @staticmethod
    def I4():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/I4.mat').resolve())
        return(load_mat(path,key='I4'))

    @staticmethod
    def Id():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/Id.mat').resolve())
        return(load_mat(path,key='M'))

    @staticmethod
    def I():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/I.mat').resolve())
        return(load_mat(path,key='I'))

    @staticmethod
    def I_max_mag():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/I_max_mag.mat').resolve())
        return(load_mat(path,key='maximum'))

    @staticmethod
    def CS():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/CS.mat').resolve())
        return(load_mat(path,key='CS'))

    @staticmethod
    def w13():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/w13.mat').resolve())
        return(load_mat(path,key='w1'))

    @staticmethod
    def w24():
        path = str(Path('mr_utils/test_data/tests/recon/ssfp/w24.mat').resolve())
        return(load_mat(path,key='w2'))

# For GRAPPA Recon
class GRAPPA(object):

    @staticmethod
    def phantom_shl():
        path = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_shl.npy').resolve())
        return(np.load(path))

    @staticmethod
    def csm():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/ch_sensitivity_1.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/ch_sensitivity_2.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/ch_sensitivity_3.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/ch_sensitivity_4.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/ch_sensitivity_5.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/ch_sensitivity_6.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        channels = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(channels)

    @staticmethod
    def phantom_ch():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_1.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_2.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_3.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_4.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_5.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_6.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        coils = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(coils)

    @staticmethod
    def phantom_ch_k():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_1_k.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_2_k.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_3_k.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_4_k.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_5_k.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_6_k.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        kspace = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(kspace)

    @staticmethod
    def phantom_ch_k_u():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_1_k_u.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_2_k_u.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_3_k_u.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_4_k_u.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_5_k_u.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_6_k_u.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        kspace = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(kspace)

    @staticmethod
    def phantom_ch_k_acl():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_1_k_acl.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_2_k_acl.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_3_k_acl.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_4_k_acl.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_5_k_acl.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/phantom_ch_6_k_acl.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        kspace = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(kspace)

    @staticmethod
    def S_ch_temp():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1_temp.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2_temp.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3_temp.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4_temp.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5_temp.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6_temp.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(S0)

    @staticmethod
    def S_ch():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(S0)

    @staticmethod
    def S():
        path = str(Path('mr_utils/test_data/tests/recon/grappa/S.npy').resolve())
        S0 = np.load(path)
        return(S0)

    @staticmethod
    def T():
        path = str(Path('mr_utils/test_data/tests/recon/grappa/T.npy').resolve())
        T0 = np.load(path)
        return(T0)

    @staticmethod
    def W():
        path = str(Path('mr_utils/test_data/tests/recon/grappa/W.npy').resolve())
        W0 = np.load(path)
        return(W0)

    @staticmethod
    def S_ch_new_temp():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1_new_temp.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2_new_temp.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3_new_temp.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4_new_temp.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5_new_temp.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6_new_temp.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(S0)

    @staticmethod
    def S_ch_new():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_1_new.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_2_new.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_3_new.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_4_new.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_5_new.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/S_ch_6_new.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        S0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(S0)

    @staticmethod
    def S_new():
        path = str(Path('mr_utils/test_data/tests/recon/grappa/S_new.npy').resolve())
        S0 = np.load(path)
        return(S0)

    @staticmethod
    def T_new():
        path = str(Path('mr_utils/test_data/tests/recon/grappa/T_new.npy').resolve())
        T0 = np.load(path)
        return(T0)

    @staticmethod
    def T_ch_new_M():
        path1 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_1_new_M.npy').resolve())
        path2 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_2_new_M.npy').resolve())
        path3 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_3_new_M.npy').resolve())
        path4 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_4_new_M.npy').resolve())
        path5 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_5_new_M.npy').resolve())
        path6 = str(Path('mr_utils/test_data/tests/recon/grappa/T_ch_6_new_M.npy').resolve())
        ch1 = np.load(path1)
        ch2 = np.load(path2)
        ch3 = np.load(path3)
        ch4 = np.load(path4)
        ch5 = np.load(path5)
        ch6 = np.load(path6)
        T0 = np.stack((ch1,ch2,ch3,ch4,ch5,ch6))
        return(T0)

    @staticmethod
    def Im_Recon():
        path = str(Path('mr_utils/test_data/tests/recon/grappa/Im_Recon.npy').resolve())
        recon = np.load(path)
        return(recon)
