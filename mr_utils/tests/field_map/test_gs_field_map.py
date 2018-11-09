import unittest
import numpy as np
from mr_utils.recon.field_map import gs_field_map
from mr_utils import view
from mr_utils.test_data.phantom import bssfp_2d_cylinder

class GSFMTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_simulated_phantom_2d(self):


        # Create the target field map
        dim = 64
        min_df,max_df = 0,500
        fx = np.linspace(min_df,max_df,dim)
        fy = np.zeros(dim)
        _,field_map = np.meshgrid(fx,fy)
        # field_map = np.random.normal(0,1,(dim,dim))
        # view(field_map)

        # Simulate phase-cycled bSSFP acquisitons
        args = {
            'TR': 5e-3,
            'alpha': np.pi/4,
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

        # Estimate field map
        recon = gs_field_map(*[ x.squeeze() for x in np.split(pcs,len(pc_vals)) ],TR=args['TR'])
        field_map[recon == 0] = 0
        # view(np.sqrt(np.abs(field_map**2) - np.abs(recon**2)))


        view(np.abs(field_map - recon))

if __name__ == '__main__':
    unittest.main()
