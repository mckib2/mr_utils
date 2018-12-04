import numpy as np
from skimage.restoration import unwrap_phase,denoise_tv_bregman
from mr_utils import view
from mr_utils.recon.ssfp import gs_recon
# from mrr.unwrapping.functions import unwrap_array

def gs_field_map(I0,I1,I2,I3,TR,gs_recon_opts={}):
    '''Use the elliptical signal model to estimate the field map.

    I0,I1 -- First phase-cycle pair, separated by 180 degrees.
    I1,I3 -- Second phase-cycle pair, separated by 180 degrees.
    TR -- Repetition time of acquisitons in ms.
    gs_recon_opts -- Options to pass to gs_recon.

    Returns wrapped field map in hertz.

    Implements field map estimation given in:
        Taylor, Meredith, et al. "MRI Field Mapping using bSSFP Elliptical
        Signal model." Proceedings of the ISMRM Annual Conference (2017).
    '''

    # TE = 2*TR
    gs_sol = gs_recon(I0,I1,I2,I3,**gs_recon_opts)
    # gsfm = np.angle(gs_sol)/(2*np.pi*TE)
    gsfm = -1*np.angle(gs_sol)/(np.pi*TR) # this one actually works...
    return(gsfm)

    # # view(np.concatenate((I0,I1,I2,I3)))
    #
    # # First find the geometric solution to the elliptical signal model
    # gs_sol = gs_recon(I0,I1,I2,I3)
    # # view(gs_sol)
    #
    # # The complex estimate of the GS has a phase that is half the angular free
    # # precession per repetition time (TR)
    # gsfm = np.angle(gs_sol)
    # gsfm[np.isnan(gsfm)] = False
    # # view(gsfm)
    #
    # # # Try TV denoising
    # # gsfm = denoise_tv_bregman(gsfm,weight=20)
    # # view(gsfm)
    #
    # # First phase unwrap
    # assert (np.min(gsfm) > -np.pi) and (np.max(gsfm) < np.pi)
    # gsfm = unwrap_phase(gsfm)

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
    # I'm uncomfortable with this negative sign
    # Also, removed the scaling by 2 at the beginning and dividing it back out
    # here, as unwrap_phase expects -pi -> pi input.
    # gsfm /= -TR*np.pi
    # # view(gsfm)
    # return(gsfm)
