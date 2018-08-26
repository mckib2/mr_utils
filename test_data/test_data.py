from pathlib import Path

## DAT FILES
bssfp_phantom = str(Path('test_data/raw/bssfp_phantom.dat').resolve())

## MAT FILES
# For SC-GROG:
test_grog_data_4D = str(Path('test_data/tests/gridding/scgrog/test_grog_data_4D.mat').resolve())
gx_gy_results = str(Path('test_data/tests/gridding/scgrog/gx_gy_results.mat').resolve())
test_gridder_data_4D = str(Path('test_data/tests/gridding/scgrog/test_gridder_data_4D.mat').resolve())
test_gx_gy_data = str(Path('test_data/tests/gridding/scgrog/test_gx_gy_data.mat').resolve())
grog_result = str(Path('test_data/tests/gridding/scgrog/grog_result.mat').resolve())

# For scr_reordering_adluru:
Coil1_data = str(Path('test_data/tests/recon/reordering/Coil1_data.mat').resolve())
mask = str(Path('test_data/tests/recon/reordering/mask.mat').resolve())
tv_prior = str(Path('test_data/tests/recon/reordering/tv_prior.mat').resolve())
recon = str(Path('test_data/tests/recon/reordering/recon.mat').resolve())
true_orderings = str(Path('test_data/tests/recon/reordering/true_orderings.mat').resolve())
TV_re_order = str(Path('test_data/tests/recon/reordering/TV_re_order.mat').resolve())
TV_term_update = str(Path('test_data/tests/recon/reordering/TV_term_update.mat').resolve())
fidelity_update = str(Path('test_data/tests/recon/reordering/fidelity_update.mat').resolve())
recon_at_iter_100 = str(Path('test_data/tests/recon/reordering/recon_at_iter_100.mat').resolve())
recon_at_iter_1 = str(Path('test_data/tests/recon/reordering/recon_at_iter_1.mat').resolve())
recon_at_iter_2 = str(Path('test_data/tests/recon/reordering/recon_at_iter_2.mat').resolve())
recon_at_iter_10 = str(Path('test_data/tests/recon/reordering/recon_at_iter_10.mat').resolve())
recon_at_iter_50 = str(Path('test_data/tests/recon/reordering/recon_at_iter_50.mat').resolve())
