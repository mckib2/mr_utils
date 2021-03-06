'''Example showing how to generate a field map using gs_field_map().'''

import numpy as np
from skimage.restoration import unwrap_phase

from mr_utils.recon.field_map import gs_field_map, dual_echo_gre
from mr_utils.sim.gre import gre_sim
from mr_utils.test_data.phantom import bssfp_2d_cylinder, cylinder_2d
from mr_utils import view

if __name__ == '__main__':

    # Create the target field map
    dim = 64
    min_df, max_df = -500, 500
    fx = np.linspace(min_df, max_df, dim)
    fy = np.zeros(dim)
    field_map, _ = np.meshgrid(fx, fy)
    # field_map = 100*np.random.normal(0,1,(dim,dim))
    view(field_map)

    # Simulate phase-cycled bSSFP acquisitons
    # Seems to be better with higher flip angle!
    # For some reason worse with higher TR
    args = {
        'TR': 5e-3,
        'alpha': np.pi/3,
        'dims': (dim, dim),
        'FOV': ((-1, 1), (-1, 1)),
        'radius': .75,
        'field_map': field_map
    }
    pc_vals = [0, np.pi/2, np.pi, 3*np.pi/2]
    pcs = np.zeros((len(pc_vals), dim, dim), dtype='complex')
    for ii, pc in enumerate(pc_vals):
        pcs[ii, ...] = bssfp_2d_cylinder(**args, phase_cyc=pc)
    view(pcs)

    # Estimate field map using GS to ESM
    gsfm = gs_field_map(*[x.squeeze() for x in np.split(
        pcs, len(pc_vals))], \
        TR=args['TR'], gs_recon_opts={'second_pass': False})
    # TODO: Interestingly, the second pass solution fails... Why is this?
    view(gsfm)

    # Now do sims for GRE for a sanity check
    TE1 = args['TR']/2
    TE2 = TE1 - args['TR']/2
    PD, T1s, T2s = cylinder_2d(dims=args['dims'], FOV=args['FOV'],
                               radius=args['radius'])
    m1 = gre_sim(T1s, T2s, TR=args['TR'], TE=TE1, alpha=args['alpha'],
                 field_map=args['field_map'], dphi=0, M0=PD, tol=1e-4)
    m2 = gre_sim(T1s, T2s, TR=args['TR'], TE=TE2, alpha=args['alpha'],
                 field_map=args['field_map'], dphi=0, M0=PD, tol=1e-4)
    grefm = dual_echo_gre(m1, m2, TE1, TE2)
    view(grefm)

    # Phase wrap the real field map so we prove equivalence up to phase
    # unwrapping...
    dTE = np.abs(TE1 - TE2)
    field_map_pw = np.mod(field_map - 1/(2*dTE), 1/dTE) - 1/(2*dTE)

    # Just for fun, try phase unwrapping...
    mask = np.zeros(gsfm.shape).astype(bool)
    idx = np.where(np.abs(gsfm) > 0)
    mask[idx] = True

    # scale between [-pi,pi], do unwrap, scale back up
    scale_fac = np.pi/np.max(np.abs(gsfm))*np.sign(np.max(gsfm))
    val = unwrap_phase(mask*gsfm*scale_fac)/scale_fac
    view(val)

    # For some reason the edges are off by about pi, so let's clip it...
    val = val[:, 19:-19]
    field_map_clipped = field_map[:, 19:-19]
    view(field_map_clipped)
