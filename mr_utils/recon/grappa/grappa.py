'''Simple GRAPPA implementation for learning purposes.

Please use Gadgetron's implementation if you need to use GRAPPA for real.
'''

import warnings # We know skimage will complain about importing imp...

import numpy as np
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from skimage.util.shape import view_as_windows

def grappa2d(coil_ims, sens, acs, Rx, Ry, kernel_size=(3, 3)):
    '''Simple 2D GRAPPA implementation.

    Parameters
    ==========
    coil_ims : array_like
        Coil images with sensity weightings corresponding to `sens`.
    sens : array_like
        Coil sensitivy maps.
    acs : array_like
        Autocalibration signal/region measurements.
    Rx : int
        Undersampling factor in x dimension.
    Ry : int
        Undersampling factor in y dimension.
    kernel_size : tuple
        Size of kernel, (x, y).

    Returns
    =======
    recon : array_like
        Reconstructed image from coil images and sensitivies.
    '''

    # We get coil ims in and we want these in kspace
    kspace_d = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(
        coil_ims), axes=(1, 2)))

    # Separate the autocalibration region into patches to get source matrix
    N = sens.shape[0] # number of coils
    S0 = np.zeros((
        N, (acs.shape[1] - 2)*(acs.shape[2] - 2),
        kernel_size[0]*kernel_size[1]), dtype='complex')
    for ii in range(N):
        S0[ii, :, :] = view_as_windows(np.ascontiguousarray(
            acs[ii, :, :]), kernel_size).reshape((S0.shape[1], S0.shape[2]))

    # Remove the unknown values.  The remaiming values form source matrix,
    # S, for each coil
    S_temp = S0[:, :, [0, 1, 2, 6, 7, 8]]
    S = np.hstack(S_temp[:])

    # The middle pts form target vector, T, for each coil
    T = S0[:, :, 4].T

    # Invert S to find weights, W
    W = np.linalg.pinv(S).dot(T)

    # Now onto the forward problem to fill in the missing lines...

    # Make patches out of all acquired data (skip the missing lines)
    S0 = np.zeros((
        N, int((kspace_d.shape[1] - 2)/Rx)*int((kspace_d.shape[2] - 2)/Ry),
        kernel_size[0]*kernel_size[1]), dtype='complex')
    for ii in range(N):
        S0[ii, :, :] = view_as_windows(
            np.ascontiguousarray(kspace_d[ii, :, :]), kernel_size,
            step=(Rx, Ry)).reshape((S0.shape[1], S0.shape[2]))

    # Remove the unknown values.  The remaiming values form source matrix,
    # S, for each coil
    S_new_temp = S0[:, :, [0, 1, 2, 6, 7, 8]]
    S_new = np.hstack(S_new_temp[:])

    # Now it's a forward problem to find missing values
    T_new = S_new.dot(W)

    # Back fill in the missing lines to recover the image
    lines = np.reshape(T_new.T, (N, -1, coil_ims.shape[2] - 2))
    kspace_d[:, 1:-1:Rx, 1:-1] = lines

    # put the coil images back in image space and send it back
    recon = np.fft.fftshift(np.fft.ifft2(np.fft.ifftshift(
        kspace_d), axes=(1, 2)))
    return recon

# def grappa_gfactor_2d_jvc2(
#     kspace_sampled,
#     kspace_acs,
#     Rx,
#     Ry,
#     acs_size,
#     kernel_size=(3,3),
#     lambda_tik=None,
#     num_cycl,
#     subs=1,
#     delx=None,
#     dely=None,
#     weights_p):
#     '''GRAPPA with tikhonov regularization.
#
#     Rz -- Acceleration in Rz.
#     Ry -- Acceleration in Ry.
#     num_cycl -- Number of cycles to reconstruct.
#     lambda_tik -- Tikhonov regularization parameter for kernel calibration.
#     delx,dely -- k-space sampling offset of each coil
#
#     Ouput:
#     img_grappa
#     mask
#     mask_acs
#     image_weights
#     g_fnl
#     '''
#
#     if lambda_tik is None:
#         lambda_tik = np.finfo(np.float32).eps
#
#
#     N[0],N[1],num_chan = kspace_sampled.shape[:]
#
#     if delx is None:
#         delx = np.zeros(num_chan)
#     if dely is None:
#         dely = np.zeros(num_chan)
#
#     num_acsX,num_acsY = acs_size.shape[:]
#
#
#     # sampling and acs masks
#     mask_acs = np.zeros((N,num_chan))
#     mask_acs[N/2-num_acsX/2:N/2+num_acsX/2 + 1, num_chan/2-num_acsY/2:num_chan/2+num_acsY/2 + 1, :] = 1
#
#     mask = np.zeros((N,num_chan))
#     for c in range(num_chan):
#         mask[delx[c]::Rx, dely[c]::Ry, c] = 1
#
#
#     kernel_hsize = np.array([(kernel_size[0]-1)/2,(kernel_size[1]-1)/2])
#
#     # pad_size = kernel_hsize .* [Rx,Ry];
#     pad_size = kernel_size*np.array([Rx,Ry])
#     N_pad = N + 2*pad_size
#
#
#     # k-space limits for training:
#     ky_begin = 1 + Ry*kernel_hsize[1] # first kernel center point that fits acs region
#     ky_end = num_acsY - Ry*kernel_hsize1[1] + 1 # last kernel center point that fits acs region
#     ky_end = ky_end - np.max(dely)
#
#     kx_begin = 1 + Rx*kernel_hsize[0] # first kernel center point that fits acs region
#     kx_end = num_acsX - Rx*kernel_hsize[0] + 1 # last kernel center point that fits acs region
#     kx_end = kx_end - np.max(delx)
#
#
#     # k-space limits for recon:
#     Ky_begin = 1 + Ry*kernel_hsize(1) # first kernel center point that fits acs region
#     Ky_end = N_pad[1] - Ry*kernel_hsize(1) # last kernel center point that fits acs region
#     Ky_end = Ky_end - np.max(dely)
#
#     Kx_begin = 1 + Rx*kernel_hsize[0] # first kernel center point that fits acs region
#     Kx_end = N_pad[0] - Rx*kernel_hsize[0] # last kernel center point that fits acs region
#     Kx_end = Kx_end - np.max(delx)
#
#
#
#     # count the no of kernels that fit in acs
#     ind = 1
#     for ky in range(ky_begin,ky_end):
#         for kx in range(kx_begin,kx_end):
#             ind += 1
#     num_ind = ind
#
#
#     kspace_acs_crop = kspace_acs[end/2-num_acsX/2:end/2+num_acsX/2 + 1, end/2-num_acsY/2:end/2+num_acsY/2 + 1, :]
#
#
# Rhs = zeross([num_ind, num_chan, Rx*Ry-1]);
# acs = zeross([kernel_size, num_chan]);
# Acs = zeross([num_ind, prod(kernel_size) * num_chan]);
#
# disp(['ACS mtx size: ', num2str(size(Acs))])
#
#
# ind = 1;
#
# for ky = ky_begin : ky_end
#     for kx = kx_begin : kx_end
#
#         for c = 1:num_chan
#             acs(:,:,c) = kspace_acs_crop(delx(c)+kx-kernel_hsize(1)*Rx : Rx : delx(c)+kx+kernel_hsize(1)*Rx, dely(c)+ky-kernel_hsize(2)*Ry : Ry : dely(c)+ky+kernel_hsize(2)*Ry, c);
#         end
#
#         Acs(ind,:) = acs(:);
#
#         idx = 1;
#         for ry = 1:Ry-1
#
#             for c = 1:num_chan
#                 Rhs(ind,c,idx) = kspace_acs_crop(delx(c)+kx, dely(c)+ky-ry, c);
#             end
#
#             idx = idx + 1;
#         end
#
#         for rx = 1:Rx-1
#             for ry = 0:Ry-1
#
#                 for c = 1:num_chan
#                     Rhs(ind,c,idx) = kspace_acs_crop(delx(c)+kx-rx, dely(c)+ky-ry, c);
#                 end
#
#                 idx = idx + 1;
#             end
#         end
#
#         ind = ind + 1;
#     end
# end
#
#
# if lambda_tik
#     [u,s,v] = svd(Acs, 'econ');
#
#     s_inv = diag(s);
#
#     disp(['condition number: ', num2str(max(abs(s_inv)) / min(abs(s_inv)))])
#
#     s_inv = conj(s_inv) ./ (abs(s_inv).^2 + lambda_tik);
#
#     Acs_inv = v * diag(s_inv) * u';
# end
#
#
# % estimate kernel weights
#
# weights = zeros([prod(kernel_size) * num_chan, num_chan, Rx*Ry-1]);
#
# for r = 1:Rx*Ry-1
#     disp(['Kernel group : ', num2str(r)])
#
#     for c = 1:num_chan
#
#         if ~lambda_tik
#             weights(:,c,r) = Acs \ Rhs(:,c,r);
#         else
#             weights(:,c,r) = Acs_inv * Rhs(:,c,r);
#         end
#
#     end
# end
#
#
#
# % recon undersampled data
#
# Weights = permute(weights, [2,1,3]);
#
# kspace_recon = padarray(kspace_sampled, [pad_size, 0]);
# data = zeross([kernel_size, num_chan]);
#
#
# for ky = Ky_begin : Ry : Ky_end
#     for kx = Kx_begin : Rx : Kx_end
#
#         for c = 1:num_chan
#             data(:,:,c) = kspace_recon(delx(c)+kx-kernel_hsize(1)*Rx : Rx : delx(c)+kx+kernel_hsize(1)*Rx, dely(c)+ky-kernel_hsize(2)*Ry : Ry : dely(c)+ky+kernel_hsize(2)*Ry, c);
#         end
#
#
#         idx = 1;
#         for ry = 1:Ry-1
#             Wdata = Weights(:,:,idx) * data(:);
#
#             for c = 1:num_chan
#                 kspace_recon(delx(c)+kx, dely(c)+ky-ry, c) = Wdata(c);
#             end
#
#             idx = idx + 1;
#         end
#
#         for rx = 1:Rx-1
#             for ry = 0:Ry-1
#                 Wdata = Weights(:,:,idx) * data(:);
#
#                 for c = 1:num_chan
#                     kspace_recon(delx(c)+kx-rx, dely(c)+ky-ry, c) = Wdata(c);
#                 end
#
#                 idx = idx + 1;
#             end
#         end
#
#     end
# end
#
# kspace_recon = kspace_recon(1+pad_size(1):end-pad_size(1), 1+pad_size(2):end-pad_size(2), :);
#
#
# if subs
#     % subsititute sampled & acs data
#     kspace_recon = kspace_recon .* (~mask & ~mask_acs) + kspace_sampled .* (~mask_acs) + kspace_acs .* mask_acs;
# end
#
# img_grappa = ifft2c(kspace_recon);
#
#
#
#
#
#
# % image space grappa weights
# if nargout > 3
#
#     image_weights = zeross([N, num_chan, num_chan]);
#
#
#     for c = 1:num_chan
#
#         idx = 1;
#
#         image_weights(delx(c) + 1+end/2, dely(c) + 1+end/2, c, c) = 1;
#
#         for ry = 1:Ry-1
#
#             w = weights(:, c, idx);
#
#             W = reshape(w, [kernel_size, num_chan]);
#
#             for coil = 1:num_chan
#                 image_weights( delx(coil) + 1+end/2 - kernel_hsize(1)*Rx :Rx: delx(coil) + 1+end/2 + kernel_hsize(1)*Rx, ...
#                     dely(coil) + ry + 1+end/2 - kernel_hsize(2)*Ry :Ry: dely(coil) + ry + 1+end/2 + kernel_hsize(2)*Ry, coil, c) = W(:,:,coil);
#             end
#
#
#             idx = idx + 1;
#
#         end
#
#         for rx = 1:Rx-1
#             for ry = 0:Ry-1
#
#                 w = weights(:, c, idx);
#
#                 W = reshape(w, [kernel_size, num_chan]);
#
#                 for coil = 1:num_chan
#                     image_weights( delx(coil) + rx + 1+end/2 - kernel_hsize(1)*Rx :Rx: delx(coil) + rx + 1+end/2 + kernel_hsize(1)*Rx, ...
#                         dely(coil) + ry + 1+end/2 - kernel_hsize(2)*Ry :Ry: dely(coil) + ry + 1+end/2 + kernel_hsize(2)*Ry, coil, c) = W(:,:,coil);
#                 end
#
#                 idx = idx + 1;
#
#             end
#         end
#
#     end
#
#
#     image_weights = flipdim( flipdim( ifft2c2( image_weights ), 1 ), 2 ) * sqrt(prod(N));
#
#
#
#     g_fnl = 0;
#
#     if (nargin == 11) && ( sum(weights_p(:)) ~=0 )
#
#         % coil combined g-factor
#
#         img_weights = image_weights / (Ry * Rx);
#
#         num_actual = size(weights_p, 3);
#
#         g_cmb = zeross([N, num_chan]);
#
#         for c = 1:num_chan
#
#             weights_coil = squeeze( img_weights(:,:,c,1:num_actual) );
#
#             g_cmb(:,:,c) = sum(weights_p .* weights_coil, 3);
#
#         end
#
#         g_comb = sqrt( sum(g_cmb .* conj( g_cmb ), 3) );
#
#         p_comb = sqrt( sum(weights_p .* conj( weights_p ), 3) );
#
#         g_fnl = g_comb ./ p_comb;
#
#     end
#
# end
#
# end
#


if __name__ == '__main__':
    pass
