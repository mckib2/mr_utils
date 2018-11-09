import numpy as np
from skimage.restoration import unwrap_phase
from mr_utils import view
from mr_utils.recon.ssfp import gs_recon
# from mrr.unwrapping.functions import unwrap_array

def gs_field_map(I0,I1,I2,I3,TR):
    '''Use the elliptical signal model to estimate the field map.

    I0,I1 -- First phase-cycle pair, separated by 180 degrees.
    I1,I3 -- Second phase-cycle pair, separated by 180 degrees.
    TR -- Repetition time of acquisitons in ms.

    Implements field map estimation given in:
        Taylor, Meredith, et al. "MRI Field Mapping using bSSFP Elliptical
        Signal model." Proceedings of the ISMRM Annual Conference (2017).
    '''

    # view(np.concatenate((I0,I1,I2,I3)))

    # First find the geometric solution to the elliptical signal model
    gs_sol = gs_recon(I0,I1,I2,I3)
    view(gs_sol)

    # The complex estimate of the GS has a phase that is half the angular free
    # precession per repetition time (TR)
    gsfm = 2*np.angle(gs_sol)/np.pi
    # view(gsfm)

    # First phase unwrap
    gsfm[np.isnan(gsfm)] = False

    assert (np.min(gsfm) > -np.pi) and (np.max(gsfm) < np.pi)
    gsfm = unwrap_phase(gsfm)

    # mask = np.logical_not(np.isnan(gsfm))
    # gsfm[np.isnan(gsfm)] = 0
    #
    # # Normalize
    # gsfm0 = gsfm - np.min(gsfm)
    # gsfm0 = gsfm0/np.max(gsfm0)
    # fac = (gsfm - np.min(gsfm))/gsfm0
    #
    # gsfm0 = gsfm/(4*np.pi) + 1
    # gsfm0 = unwrap_array(gsfm0,mask)
    # gsfm = 4*np.pi*gsfm0 - 1
    # view(gsfm0)
    # # gsfm = gsfm0*fac
    # gsfm = gsfm0


    # IM = gsfm.copy()
    # IM_mag = np.abs(IM) # Magnitude image
    # IM_phase = IM.copy() # angle(IM); %Phase image
    # tryagain = True # this really only makes sense if phaseUnwrapDebug is on . . .
    # while tryagain:
    #     residue_charge = PhaseResidues(IM_phase, IM_mask) # Calculate phase residues
    #     branch_cuts = BranchCuts(residue_charge, max_box_radius, IM_mask) # Place branch cuts
    #     IM_unwrapped,rowref,colref = FloodFill(IM_phase, branch_cuts, IM_mask,x,y) # Flood fill phase unwrapping
    #     #u_data = IM_mag*np.exp(1j*IM_unwrapped/scalingFactor) # rephase 10 is good for bottle
    #     gsfm = IM_unwrapped # rephase 10 is good for bottle
    #
    #     tryagain = False
    #     # figure; imagesc(IM_phase),  axis square, axis off, title('Wrapped phase');
    #     # figure; imagesc(angle(u_data)),  axis square, axis off, title('Unwrapped phase');
    #     # figure; imagesc(IM_unwrapped), axis square, axis off, title('Golden Unwrapped phase'); # golden
    #     # button = questdlg(promptMessage, titleBarCaption, 'Yes', 'No', 'Yes');
    #     # if strcmpi(button, 'Yes'):
    #     #     tryagain = False
    #     # else:
    #     #    tryagain = True

    # Map free precession per TR to off-resonance
    gsfm /= -TR*2
    view(gsfm)
    return(gsfm)
