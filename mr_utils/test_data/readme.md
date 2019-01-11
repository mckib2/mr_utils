
## mr_utils.test_data.test_data

[Source](../master/mr_utils/test_data/test_data.py)

```
NAME
    mr_utils.test_data.test_data

CLASSES
    builtins.object
        BARTReordering
        BSSFPGrappa
        EllipticalSignal
        GRAPPA
        GadgetronClient
        GadgetronTestConfig
        SCGROG
        SCRReordering
        SSFPMultiphase
        ViewTestData
        XProtParserTest
    
    class BARTReordering(builtins.object)
     |  # For BART reordering recon
     |  
     |  Static methods defined here:
     |  
     |  ksp_sim()
     |  
     |  lowres_img()
     |  
     |  lowres_ksp()
     |  
     |  reco1()
     |  
     |  reco2()
     |  
     |  sens()
     |  
     |  traj_rad2()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class BSSFPGrappa(builtins.object)
     |  # For Gadgetron GRAPPA Examples
     |  
     |  Static methods defined here:
     |  
     |  pc0_r2()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class EllipticalSignal(builtins.object)
     |  # For elliptical signal model:
     |  
     |  Static methods defined here:
     |  
     |  CS()
     |  
     |  I()
     |  
     |  I1()
     |  
     |  I2()
     |  
     |  I3()
     |  
     |  I4()
     |  
     |  I_max_mag()
     |  
     |  Id()
     |  
     |  w13()
     |  
     |  w24()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class GRAPPA(builtins.object)
     |  # For GRAPPA Recon
     |  
     |  Static methods defined here:
     |  
     |  Im_Recon()
     |  
     |  S()
     |  
     |  S_ch()
     |  
     |  S_ch_new()
     |  
     |  S_ch_new_temp()
     |  
     |  S_ch_temp()
     |  
     |  S_new()
     |  
     |  T()
     |  
     |  T_ch_new_M()
     |  
     |  T_new()
     |  
     |  W()
     |  
     |  csm()
     |  
     |  phantom_ch()
     |  
     |  phantom_ch_k()
     |  
     |  phantom_ch_k_acl()
     |  
     |  phantom_ch_k_u()
     |  
     |  phantom_shl()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class GadgetronClient(builtins.object)
     |  ## HDF5 FILES
     |  # For gadgetron
     |  
     |  Static methods defined here:
     |  
     |  epi_input_filename()
     |      Gadgetron test data.
     |      http://gadgetrondata.blob.core.windows.net/gadgetrontestdata/epi/epi_2d_out_20161020_pjv.h5
     |  
     |  generic_cartesian_grappa_filename()
     |      Gadgetron test data.
     |      http://gadgetrondata.blob.core.windows.net/gadgetrontestdata/tse/meas_MID00450_FID76726_SAX_TE62_DIR_TSE/ref_20160319.dat
     |  
     |  grappa_input_filename()
     |  
     |  input_filename()
     |  
     |  input_h5()
     |  
     |  raw_input_filename()
     |  
     |  true_output_data()
     |  
     |  true_output_data_grappa_cpu()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class GadgetronTestConfig(builtins.object)
     |  ## XML FILES
     |  # For gadgetron
     |  
     |  Static methods defined here:
     |  
     |  default_config()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class SCGROG(builtins.object)
     |  ## MAT FILES
     |  # For SC-GROG:
     |  
     |  Static methods defined here:
     |  
     |  grog_result()
     |  
     |  gx_gy_results()
     |  
     |  test_gridder_data_4D()
     |  
     |  test_grog_data_4D()
     |  
     |  test_gx_gy_data()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class SCRReordering(builtins.object)
     |  # For scr_reordering_adluru:
     |  
     |  Static methods defined here:
     |  
     |  Coil1_data()
     |  
     |  TV_re_order()
     |  
     |  TV_term_update()
     |  
     |  fidelity_update()
     |  
     |  mask()
     |  
     |  recon()
     |  
     |  recon_at_iter_1()
     |  
     |  recon_at_iter_10()
     |  
     |  recon_at_iter_100()
     |  
     |  recon_at_iter_2()
     |  
     |  recon_at_iter_50()
     |  
     |  true_orderings()
     |  
     |  tv_prior()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class SSFPMultiphase(builtins.object)
     |  ## NPY FILES
     |  # For ssfp multiphase:
     |  
     |  Methods defined here:
     |  
     |  ssfp_ankle_te_6_pc_180()
     |  
     |  ssfp_ankle_te_6_pc_90()
     |  
     |  ----------------------------------------------------------------------
     |  Static methods defined here:
     |  
     |  ssfp_ankle_te_6_pc_0()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class ViewTestData(builtins.object)
     |  # For VIEW testing:
     |  
     |  Static methods defined here:
     |  
     |  ssfp_ankle_te_6_pc_0()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    class XProtParserTest(builtins.object)
     |  ## XPROT FILES
     |  # For xprot_parser
     |  
     |  Static methods defined here:
     |  
     |  full_sample_xprot()
     |  
     |  sample_xprot()
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

```

