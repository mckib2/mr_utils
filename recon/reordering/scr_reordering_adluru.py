import numpy as np
from time import time


def intshft(m,sh):
    '''Shift image m by coordinates specified by sh'''

    nx,ny = m.shape[:]

    m3 = m.copy()
    m2 = m.copy()

    k1 = np.abs(sh[0])
    k2 = np.abs(sh[1])

    if (sh[0] > 0 and sh[1] > 0):
        m2[k1:,k2:] = m[:-k1,:-k2]

    if (sh[0] < 0 and sh[1] < 0):
        m2[:-k1,:-k2] = m[k1:,k2:]

    if (sh[0] > 0 and sh[1] < 0):
        m2[k1:,:-k2] = m[:-k1,k2:]

    if (sh[0] < 0 and sh[1] > 0):
        m2[:-k1,k2:] = m[k1:,:-k2]

    if (sh[0] == 0 and sh[1] == 0):
        m2 = m3.copy()

    if (sh[0] < 0 and sh[1] == 0):
        m2[:-k1,:] = m[k1:,:]

    if (sh[0] > 0 and sh[1] == 0):
        m2[k1:,:] = m[:-k1,:]

    if (sh[0] == 0 and sh[1] > 0):
        m2[:,k2:] = m[:,:-k2]

    if (sh[0] == 0 and sh[1] < 0):
        m2[:,:-k2] = m[:,k2:]

    return(m2)

def TVG(out_img,beta_sqrd):

    # Computing numerator terms
    temp_a = np.diff(out_img,1,1)
    temp_b = np.diff(out_img,1,0)

    T1_num = np.zeros(out_img.shape,dtype='complex')
    T1_num[:,:-1] = temp_a
    T2_num = np.zeros(out_img.shape,dtype='complex')
    T2_num[:,1:] = temp_a
    T3_num = np.zeros(out_img.shape,dtype='complex')
    T3_num[:-1,:] = temp_b
    T4_num = np.zeros(out_img.shape,dtype='complex')
    T4_num[1:,:] = temp_b

    # Generating imgs for computing denominator terms
    xmyp_img = intshft(out_img,[-1,1])
    xmym_img = intshft(out_img,[1,1])
    xpym_img = intshft(out_img,[1,-1])
    # xmyp_img = np.roll(out_img,(-1,1))
    # xmym_img = np.roll(out_img,(1,1))
    # xpym_img = np.roll(out_img,(1,-1))

    # Computing denominator terms
    T1_den = np.sqrt(beta_sqrd + np.abs(T1_num)**2 + (np.abs((T3_num + T4_num)/2))**2)
    T2_den = np.sqrt(beta_sqrd + np.abs(T2_num)**2 + (np.abs((xmyp_img - xmym_img)/2))**2)
    T3_den = np.sqrt(beta_sqrd + np.abs(T3_num)**2 + (np.abs((T1_num + T2_num)/2))**2)
    T4_den = np.sqrt(beta_sqrd + np.abs(T4_num)**2 + (np.abs((xpym_img - xmym_img)/2))**2)

    # Computing the terms
    T1 = T1_num/T1_den
    T2 = T2_num/T2_den
    T3 = T3_num/T3_den
    T4 = T4_num/T4_den

    TV_update = T1 - T2 + T3 - T4
    return(TV_update)


def TVG_re_order(out_img,beta_sqrd,sort_order_real_x,sort_order_real_y):

    # re-ordering in x,y
    x_ordered_img = np.zeros(out_img.shape)
    y_ordered_img = np.zeros(out_img.shape)

    sx,sy = out_img.shape[:]

    for jj in range(sy):
        a_temp = out_img[:,jj]
        b_temp = sort_order_real_x[:,jj]
        y_ordered_img[:,jj] = a_temp[b_temp.astype(int)]

    for ii in range(sx):
        a_temp = out_img[ii,:]
        b_temp = sort_order_real_y[ii,:]
        x_ordered_img[ii,:] = a_temp[b_temp.astype(int)]


    # Computing numerator terms
    xpy_img = intshft(x_ordered_img,[0,-1])
    # xpy_img = np.roll(x_ordered_img,(0,-1))
    T1_num = xpy_img - x_ordered_img
    xmy_img = intshft(x_ordered_img,[0,1])
    # xmy_img = np.roll(x_ordered_img,(0,1))
    T2_num = x_ordered_img - xmy_img

    xyp_img = intshft(y_ordered_img,[-1,0])
    # xyp_img = np.roll(y_ordered_img,(-1,0))
    T3_num = xyp_img - y_ordered_img
    xym_img = intshft(y_ordered_img,[1,0])
    # xym_img = np.roll(y_ordered_img,(1,0))
    T4_num = y_ordered_img - xym_img

    xmyp_img_new = intshft(y_ordered_img,[-1,1])
    xmym_img_new = intshft(y_ordered_img,[1,1])
    # xmyp_img_new = np.roll(y_ordered_img,(-1,1))
    # xmym_img_new = np.roll(y_ordered_img,(1,1))

    xpym_img_new = intshft(x_ordered_img,[1,-1])
    xmym_img_new2 = intshft(x_ordered_img,[1,1])
    # xpym_img_new = np.roll(x_ordered_img,(1,-1))
    # xmym_img_new2 = np.roll(x_ordered_img,(1,1))

    # Computing denominator terms
    T1_den = np.sqrt(beta_sqrd + np.abs(T1_num)**2 + (np.abs((xyp_img - xym_img)/2))**2)
    T2_den = np.sqrt(beta_sqrd + np.abs(T2_num)**2 + (np.abs((xmyp_img_new - xmym_img_new)/2))**2)
    T3_den = np.sqrt(beta_sqrd + np.abs(T3_num)**2 + (np.abs((xpy_img - xmy_img)/2))**2)
    T4_den = np.sqrt(beta_sqrd + np.abs(T4_num)**2 + (np.abs((xpym_img_new - xmym_img_new2)/2))**2)

    # Computing the terms
    T1 = T1_num/T1_den
    T2 = T2_num/T2_den
    T3 = T3_num/T3_den
    T4 = T4_num/T4_den

    TV_update_x = T1 - T2
    TV_update_y = T3 - T4

    TV_update_y_new = np.zeros(TV_update_x.shape)
    TV_update_x_new = np.zeros(TV_update_x.shape)

    a_temp = np.zeros(sy)
    b_temp = np.zeros(sx)

    for jj in range(sy):
        b_temp[sort_order_real_x[:,jj].astype(int)] = TV_update_y[:,jj]
        TV_update_y_new[:,jj] = b_temp

    for ii in range(sx):
        a_temp[sort_order_real_y[ii,:].astype(int)] = TV_update_x[ii,:]
        TV_update_x_new[ii,:] = a_temp

    TV_update = TV_update_y_new + TV_update_x_new

    return(TV_update)



def sort_real_imag_parts_space(full_data_recon_complex):
    '''Determines the sort order for real and imag components.
    '''

    sx,sy = full_data_recon_complex.shape[:]

    real_full_data = full_data_recon_complex.real
    imag_full_data = full_data_recon_complex.imag

    sort_order_real_x = np.zeros(real_full_data.shape)
    sort_order_real_y = np.zeros(real_full_data.shape)

    sort_order_imag_x = np.zeros(real_full_data.shape)
    sort_order_imag_y = np.zeros(real_full_data.shape)

    for jj in range(sy):
        sort_order_real_x[:,jj] = np.argsort(real_full_data[:,jj])
        sort_order_imag_x[:,jj] = np.argsort(imag_full_data[:,jj])

    for ii in range(sx):
        sort_order_real_y[ii,:] = np.argsort(real_full_data[ii,:])
        sort_order_imag_y[ii,:] = np.argsort(imag_full_data[ii,:])

    return(sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y)


def scr_reordering_adluru(kspace,mask,prior=None,alpha0=1,alpha1=.002,beta2=1e-8,niters=5000):
    '''Reconstruct undersampled data with spatial TV constraint and reordering.

    kspace -- undersampled k-space data
    mask -- Undersampling mask
    prior -- Prior image estimate, what to base reordering on
    alpha0 -- Weight of the fidelity term in cost function
    alpha1 -- Weight of the TV term, regularization parameter
    beta2 -- beta squared, small constant to keep sqrt defined
    niters -- number of iterations

    Ref: G.Adluru, E.V.R. DiBella. "Reordering for improved constrained
    reconstruction from undersampled k-space data". International Journal of
    Biomedical Imaging vol. 2008, Article ID 341684, 12 pages, 2008.
    doi:10.1155/2008/341684.
    '''

    # Find a place to start from
    measuredImgDomain = np.fft.ifft2(kspace)
    img_est = measuredImgDomain.copy()
    W_img_est = np.fft.ifft2(np.fft.fft2(img_est)*mask)

    # If we don't have one...use undersampled data as prior
    if prior is None:
        prior = img_est.copy()

    # Determine ordering
    sort_order_real_x,sort_order_imag_x,sort_order_real_y,sort_order_imag_y = sort_real_imag_parts_space(prior*1000)

    # gradient descent minimization
    t0 = time()
    for ii in range(niters):
        # Find fidelity term
        # W_img_est = np.fft.ifft2(np.fft.fft2(img_est)*mask)
        fidelity_update = alpha0*(measuredImgDomain - W_img_est)

        # Spatial re-ordering - TV
        TV_term_reorder_update_real = TVG_re_order(img_est.real,beta2,sort_order_real_x,sort_order_real_y)
        TV_term_reorder_update_imag = TVG_re_order(img_est.imag,beta2,sort_order_imag_x,sort_order_imag_y)
        TV_term_reorder_update = alpha1*0.5*(TV_term_reorder_update_real + 1j*TV_term_reorder_update_imag)

        # Computing spatial regul - TV
        TV_term_update = TVG(img_est,beta2)*alpha1*0.5

        # Take a step
        img_est += fidelity_update + TV_term_update + TV_term_reorder_update

        W_img_est = np.fft.ifft2(np.fft.fft2(img_est)*mask)

        print('Status: [%d%%]\r' % (100*ii/niters),end='')
    print('Total time: %g sec' % (time()-t0))

    return(img_est)

if __name__ == '__main__':
    pass
