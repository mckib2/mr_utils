import unittest
import numpy as np
from mr_utils.recon.field_map import gs_field_map,dual_echo_gre
from mr_utils import view
from mr_utils.test_data.phantom import bssfp_2d_cylinder,spoiled_gre_2d_cylinder,cylinder_2d
from mr_utils.sim.gre import gre_sim

class GSFMTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_simulated_phantom_2d(self):

        # Create the target field map
        dim = 64
        min_df,max_df = -500,500
        fx = np.linspace(min_df,max_df,dim)
        fy = np.zeros(dim)
        field_map,_ = np.meshgrid(fx,fy)
        # field_map = 100*np.random.normal(0,1,(dim,dim))
        # view(field_map)

        # Simulate phase-cycled bSSFP acquisitons
        # Seems to be better with higher flip angle!
        # For some reason worse with higher TR
        args = {
            'TR': 5e-3,
            'alpha': np.pi/6,
            'dims': (dim,dim),
            'FOV': ((-1,1),(-1,1)),
            'radius': .75,
            'field_map': field_map
        }
        pc_vals = [ 0,np.pi/2,np.pi,3*np.pi/2 ]
        pcs = np.zeros((len(pc_vals),dim,dim),dtype='complex')
        for ii,pc in enumerate(pc_vals):
            pcs[ii,...] = bssfp_2d_cylinder(**args,phase_cyc=pc)
        # view(pcs)

        # Estimate field map using GS to ESM
        gsfm = gs_field_map(*[ x.squeeze() for x in np.split(pcs,len(pc_vals)) ],TR=args['TR'])

        # Now do sims for GRE
        TE1,TE2 = 0.003,0.007
        PD,T1s,T2s = cylinder_2d(dims=args['dims'],FOV=args['FOV'],radius=args['radius'])
        m1 = gre_sim(T1s,T2s,TR=args['TR'],TE=TE1,alpha=args['alpha'],field_map=args['field_map'],dphi=np.pi,M0=PD,iter=50)
        m2 = gre_sim(T1s,T2s,TR=args['TR'],TE=TE2,alpha=args['alpha'],field_map=args['field_map'],dphi=np.pi,M0=PD,iter=50)
        grefm = dual_echo_gre(m1,m2,TE1,TE2)

        view(np.concatenate((grefm,gsfm)))

        # field_map_pw = np.mod(field_map*2*np.pi,2*np.pi) - np.pi
        # view(field_map_pw)
        # view(np.concatenate((gsfm,field_map_pw)))

if __name__ == '__main__':
    unittest.main()
