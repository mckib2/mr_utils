'''Python port of Merry's bSSFP parameter mapping code.

This is an alternative to PLANET.
'''

import numpy as np
import matplotlib.pyplot as plt
from tqdm import trange

from mr_utils.recon.ssfp import gs_recon as EllipticalModel256
from mr_utils.recon.ssfp.merry_param_mapping.ssfp_fit import SSFPfit
from mr_utils.recon.ssfp.merry_param_mapping.optimize import optimize
from mr_utils.recon.ssfp.merry_param_mapping.plot_ellipse import plotEllipse

def param_map(N=256, add_noise=False, disp=False):
    '''This code will simulate the elliptical signal model found in the paper
    "Banding Artifact Removal for bSSFP Imaging with an Elliptical Signal
    Model" by Xiang, Qing-San and Hoff, Michael N.

    N -- Size of phantom.
    add_noise -- Whether or not to simulate noise.
    disp -- Show debugging plots.
    '''

    # The first step is to create the phantom image.  For this I need matrices
    # where each entry represents a voxel's tissue/scan parameters.

    # First initialize everything.
    T1 = np.zeros((N, N))
    T2 = np.zeros((N, N))
    offres = np.zeros((N, N))
    alpha = np.zeros((N, N))
    M0 = np.zeros((N, N))
    _temp_m0 = np.linspace(1, 10, 200)

    # Next set up the desired values across the phantom.  This phantom will be
    # fat on top and water on bottom.  Each section will be 200 pixels wide by
    # 100 pixels tall, which will leave margins of 28 pixels.

    # At 3 T fat has a T1 of 300 ms and a T2 of 85 ms. synovial fluid 4813 T1
    # 325 T2
    for kk in range(29, 128): # Iterate through the rows
        for nn in range(29, 228): # Iterate through the columns
            T1[kk, nn] = 300
            T2[kk, nn] = 85
            M0[kk, nn] = 1

            # Introduces a linear variation in the x direction, producing
            # banding.
            offres[kk, nn] = nn - 29

            # Assume a uniform flip angle across the image.
            alpha[kk, nn] = np.deg2rad(30)

    # At 3 T water has a T1 of 3000 ms and a T2 of 160 ms. Cartilage 1568 T1 32
    # T2
    for kk in range(129, 228): # Iterate through the rows
        for nn in range(29, 228): # Iterate through the columns
            T1[kk, nn] = 1200
            T2[kk, nn] = 30
            M0[kk, nn] = 1

            # Introduces a linear variation in the x direction, producing
            # banding.
            offres[kk, nn] = nn - 29

            # Assume a uniform flip angle across the image.
            alpha[kk, nn] = np.deg2rad(30)

    # Set up scan parameters (in milliseconds).
    TR = 10
    TE = 5

    # Set up magnetization matrices for the x and y components for each pixel.
    # Matrix for dphi = 0 degrees
    Mx0 = np.zeros((N, N))
    My0 = np.zeros((N, N))
    a0 = np.zeros((N, N))
    b0 = np.zeros((N, N))
    M_0 = np.zeros((N, N))

    # Matrix for dphi = 22.5 degrees
    Mx22 = np.zeros((N, N))
    My22 = np.zeros((N, N))
    a22 = np.zeros((N, N))
    b22 = np.zeros((N, N))
    M22 = np.zeros((N, N))

    # Matrix for dphi = 45 degrees
    Mx45 = np.zeros((N, N))
    My45 = np.zeros((N, N))
    a45 = np.zeros((N, N))
    b45 = np.zeros((N, N))
    M45 = np.zeros((N, N))

    # Matrix for dphi = 67.5 degrees
    Mx67 = np.zeros((N, N))
    My67 = np.zeros((N, N))
    a67 = np.zeros((N, N))
    b67 = np.zeros((N, N))
    M67 = np.zeros((N, N))

    # Matrix for dphi = 90 degrees
    Mx90 = np.zeros((N, N))
    My90 = np.zeros((N, N))
    a90 = np.zeros((N, N))
    b90 = np.zeros((N, N))
    M90 = np.zeros((N, N))

    # Matrix for dphi = 112.5 degrees
    Mx112 = np.zeros((N, N))
    My112 = np.zeros((N, N))
    a112 = np.zeros((N, N))
    b112 = np.zeros((N, N))
    M112 = np.zeros((N, N))

    # Matrix for dphi = 135 degrees
    Mx135 = np.zeros((N, N))
    My135 = np.zeros((N, N))
    a135 = np.zeros((N, N))
    b135 = np.zeros((N, N))
    M135 = np.zeros((N, N))

    # Matrix for dphi = 157.5 degrees
    Mx157 = np.zeros((N, N))
    My157 = np.zeros((N, N))
    a157 = np.zeros((N, N))
    b157 = np.zeros((N, N))
    M157 = np.zeros((N, N))

    # Matrix for dphi = 180 degrees
    Mx180 = np.zeros((N, N))
    My180 = np.zeros((N, N))
    a180 = np.zeros((N, N))
    b180 = np.zeros((N, N))
    M180 = np.zeros((N, N))

    # Matrix for dphi = 202.5 degrees
    Mx202 = np.zeros((N, N))
    My202 = np.zeros((N, N))
    a202 = np.zeros((N, N))
    b202 = np.zeros((N, N))
    M202 = np.zeros((N, N))

    # Matrix for dphi = 225 degrees
    Mx225 = np.zeros((N, N))
    My225 = np.zeros((N, N))
    a225 = np.zeros((N, N))
    b225 = np.zeros((N, N))
    M225 = np.zeros((N, N))

    # Matrix for dphi = 247.5 degrees
    Mx247 = np.zeros((N, N))
    My247 = np.zeros((N, N))
    a247 = np.zeros((N, N))
    b247 = np.zeros((N, N))
    M247 = np.zeros((N, N))

    # Matrix for dphi = 270 degrees
    Mx270 = np.zeros((N, N))
    My270 = np.zeros((N, N))
    a270 = np.zeros((N, N))
    b270 = np.zeros((N, N))
    M270 = np.zeros((N, N))

    # Matrix for dphi = 292.5 degrees
    Mx292 = np.zeros((N, N))
    My292 = np.zeros((N, N))
    a292 = np.zeros((N, N))
    b292 = np.zeros((N, N))
    M292 = np.zeros((N, N))

    # Matrix for dphi = 315 degrees
    Mx315 = np.zeros((N, N))
    My315 = np.zeros((N, N))
    a315 = np.zeros((N, N))
    b315 = np.zeros((N, N))
    M315 = np.zeros((N, N))

    # Matrix for dphi = 337.5 degrees
    Mx337 = np.zeros((N, N))
    My337 = np.zeros((N, N))
    a337 = np.zeros((N, N))
    b337 = np.zeros((N, N))
    M337 = np.zeros((N, N))

    # Simulate SSFP on each pixel in which the phantom is defined.
    for kk in trange(29, 228, leave=False, desc='Simulate SSFP'):
        # Iterate through the rows
        for nn in range(29, 228): # Iterate through the columns
            Mx0[kk, nn], My0[kk, nn], a0[kk, nn], b0[kk, nn], M_0[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 0, offres[kk, nn], M0[kk, nn])
            Mx22[kk, nn], My22[kk, nn], a22[kk, nn], b22[kk, nn], M22[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], np.pi / 8, offres[kk, nn], M0[kk, nn])
            Mx45[kk, nn], My45[kk, nn], a45[kk, nn], b45[kk, nn], M45[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], np.pi / 4, offres[kk, nn], M0[kk, nn])
            Mx67[kk, nn], My67[kk, nn], a67[kk, nn], b67[kk, nn], M67[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 3 * np.pi / 8, offres[kk, nn], M0[kk, nn])
            Mx90[kk, nn], My90[kk, nn], a90[kk, nn], b90[kk, nn], M90[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], np.pi / 2, offres[kk, nn], M0[kk, nn])
            Mx112[kk, nn], My112[kk, nn], a112[kk, nn], b112[kk, nn], M112[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 5 * np.pi / 8, offres[kk, nn], M0[kk, nn])
            Mx135[kk, nn], My135[kk, nn],a135[kk, nn], b135[kk, nn], M135[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 3 * np.pi / 4, offres[kk, nn], M0[kk, nn])
            Mx157[kk, nn], My157[kk, nn], a157[kk, nn], b157[kk, nn], M157[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 7 * np.pi / 8, offres[kk, nn], M0[kk, nn])
            Mx180[kk, nn], My180[kk, nn],a180[kk, nn], b180[kk, nn], M180[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], np.pi, offres[kk, nn], M0[kk, nn])
            Mx202[kk, nn], My202[kk, nn], a202[kk, nn], b202[kk, nn], M202[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 9 * np.pi / 8, offres[kk, nn], M0[kk, nn])
            Mx225[kk, nn], My225[kk, nn], a225[kk, nn], b225[kk, nn], M225[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 5 * np.pi / 4, offres[kk, nn], M0[kk, nn])
            Mx247[kk, nn], My247[kk, nn], a247[kk, nn], b247[kk, nn], M247[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 11 * np.pi / 8, offres[kk, nn], M0[kk, nn])
            Mx270[kk, nn], My270[kk, nn], a270[kk, nn], b270[kk, nn], M270[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 3 * np.pi / 2, offres[kk, nn], M0[kk, nn])
            Mx292[kk, nn], My292[kk, nn], a292[kk, nn], b292[kk, nn], M292[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 13 * np.pi / 8, offres[kk, nn], M0[kk, nn])
            Mx315[kk, nn], My315[kk, nn], a315[kk, nn], b315[kk, nn], M315[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 7 * np.pi / 4, offres[kk, nn], M0[kk, nn])
            Mx337[kk, nn], My337[kk, nn], a337[kk, nn], b337[kk, nn], M337[kk, nn] = SSFPfit(T1[kk, nn], T2[kk, nn], TR, TE, alpha[kk, nn], 15 * np.pi / 8, offres[kk, nn], M0[kk, nn])


    # Create the complex images from Mx and My.
    I0 = Mx0 + 1j*My0
    _I22 = Mx22 + 1j*My22
    I45 = Mx45 + 1j*My45
    _I67 = Mx67 + 1j*My67
    I90 = Mx90 + 1j*My90
    _I112 = Mx112 + 1j*My112
    I135 = Mx135 + 1j*My135
    _I157 = Mx157 + 1j*My157
    I180 = Mx180 + 1j*My180
    _I202 = Mx202 + 1j*My202
    I225 = Mx225 + 1j*My225
    _I247 = Mx247 + 1j*My247
    I270 = Mx270 + 1j*My270
    _I292 = Mx292 + 1j*My292
    I315 = Mx315 + 1j*My315
    _I337 = Mx337 + 1j*My337

    #--------------------------------------------------------------------------
    # The following code plots four of the phase cycled images.  It is
    # contained within an if block, so if you desire to run it, replace false
    # with true.
    #--------------------------------------------------------------------------
    if disp:
        # Plot the phase cycled images.  For brevity I will only plot the
        # images with 0, 90, 180, and 270 degree phase cycling.
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.imshow(np.abs(I0))
        plt.title('0 Degree Phase Cycling')
        plt.subplot(2, 2, 2)
        plt.imshow(np.abs(I90))
        plt.title('90 Degree Phase Cycling')
        plt.subplot(2, 2, 3)
        plt.imshow(np.abs(I180))
        plt.title('180 Degree Phase Cycling')
        plt.subplot(2, 2, 4)
        plt.imshow(np.abs(I270))
        plt.title('270 Degree Phase Cycling')
        plt.show()
    #--------------------------------------------------------------------------


    #--------------------------------------------------------------------------
    # The following code adds noise to the four phase cycled images used in the
    # elliptical model banding artifact removal.  It is contained in an if
    # block, so if you do not want noise, replace true with false.
    #
    # Also, I use the 0, 90, 180, and 270 degree phase cycled images, but any
    # two pairs of phase cycled images will work, as long as each image is 180
    # degrees offset from its paired image.
    #--------------------------------------------------------------------------
    if add_noise:
        s = 0.001 # std deviation
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I0 += n
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I90 += n
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I180 += n
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I270 += n
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I45 += n
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I135 += n
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I225 += n
        n = np.random.normal(0, s, (N, N)) + 1j*np.random.normal(0, s, (N, N))
        I315 += I315
    #--------------------------------------------------------------------------


    # Calculate the banding-removed image using the algorithm in the elliptical
    # model paper.
    M = EllipticalModel256(I0, I90, I180, I270)

    # Display elliptical model image.
    if disp:
        # plt.figure()
        # plt.imshow(np.abs(I))
        # plt.title('Eliptical Model - Banding Removed')
        # plt.show()

        plt.figure()
        plt.title('0 PC')
        plt.subplot(2, 2, 1)
        plt.plot(I0.real[30, 29:228])
        plt.subplot(2, 2, 2)
        plt.plot(I0.imag[30, 29:228])
        plt.subplot(2, 2, 3)
        plt.plot(np.abs(I0[30, 29:228]))
        plt.subplot(2, 2, 4)
        plt.plot(np.angle(I0[30, 29:228]))
        plt.show()

        plt.figure()
        plt.title('180 PC')
        plt.subplot(2, 2, 1)
        plt.plot(I180.real[30, 29:228])
        plt.subplot(2, 2, 2)
        plt.plot(I180.imag[30, 29:228])
        plt.subplot(2, 2, 3)
        plt.plot(np.abs(I180[30, 29:228]))
        plt.subplot(2, 2, 4)
        plt.plot(np.angle(I180[30, 29:228]))
        plt.show()
        # compare to Lauzon paper figure 1

    ## Elliptical fit done here
    # phi = [0 pi/2 pi 3/2*pi 1/4*pi 3/4*pi 5/4*pi 7/4*pi 67*pi/180 247*pi/180]
    row = 130
    col = 129 #%70; %30;
    # 8 phase-cycles
    # phi=[0 pi/2 pi 3/2*pi 1/4*pi 3/4*pi 5/4*pi 7/4*pi];
    # I=[I0(row,col); I90(row, col); I180(row,col); I270(row, col);
    #          I45(row,col); I135(row,col); I225(row,col); I315(row,col)];
    # 4 phase-cycles

    offres_est = np.angle(M)
    offres_est[29:228, 29:228] = np.unwrap(offres_est[29:228, 29:228], axis=1)
    offres_est /= np.pi*TR*1e-3

    num_iters = len(list(range(29, 228)))
    xopt4 = np.zeros((num_iters, 4))
    error = np.zeros((num_iters, 4))
    fopts = np.zeros((num_iters, 1))
    t1map = np.zeros((N, N))
    t2map = np.zeros((N, N))
    offresmap = np.zeros((N, N))
    m0map = np.zeros((N, N))
    kk = 0
    phi = np.array([0, np.pi/2, np.pi, 3/2*np.pi, 1/4*np.pi, 3/4*np.pi,
                    5/4*np.pi, 7/4*np.pi])
    for row in trange(29, 228, leave=False, desc='Make Param Maps'):
        for col in range(29, 228):
            kk += 1
            I = np.array([I0[row, col], I90[row, col], I180[row, col],
                          I270[row, col], I45[row, col], I135[row, col],
                          I225[row, col], I315[row, col]])
            # phi=[0 pi/2 pi 3/2*pi ];
            # I=[I0(row,col); I90(row, col); I180(row,col); I270(row, col)];
            _phasecycles = phi
            xopt, fopt = optimize(I.conj().T, TE, TR, phi,
                                  offres_est[row, col]/100, 1.2,
                                  alpha[row, col],
                                  1000/100, 100/10)
            xopt4[kk, :] = xopt
            t1map[row, col] = xopt[0]*100
            t2map[row, col] = xopt[1]*10
            offresmap[row, col] = xopt[2]*100
            m0map[row, col] = xopt[3]

            fopts[kk] = fopt
            error[kk, :] = np.abs(xopt - np.array([T1[row, col]/100,
                                                   T2[row, col]/10,
                                                   offres[row, col]/100,
                                                   M0[row, col]/10]))

    if disp:
        # plot ellipse and fit of a pixel
        row = 130
        col = 30
        # plotEllipse(T1, T2, TR, TE, alpha, offres, M0, dphi)
        xt, yt = plotEllipse(T1[row, col], T2[row, col], TR, TE,
                             alpha[row, col], offres[row, col], M0[row, col],
                             1)
        xe, ye = plotEllipse(t1map[row, col], t2map[row, col], TR, TE,
                             alpha[row, col], offresmap[row, col],
                             m0map[row, col], 1)
        plt.figure()
        plt.plot(xt, yt, 'b')
        plt.plot(xe, ye, 'g')
        plt.plot(I0[row, col], 'rx')
        plt.plot(I90[row, col], 'rx')
        plt.plot(I180[row, col], 'rx')
        plt.plot(I270[row, col], 'rx')
        plt.plot(I45[row, col], 'rx')
        plt.plot(I135[row, col], 'rx')
        plt.plot(I225[row, col], 'rx')
        plt.plot(I315[row, col], 'rx')
        plt.axis('equal')
        plt.show()

    ## I COMMENTED THESE OUT FOR LATER
    # if false
    #     nx=200;
    #     x=linspace(0,2,nx); %M0
    #     Z=zeros(nx,1);
    #     for k=1:nx
    #         Z(k)=ellipticalfit( I', TE, TR, phasecycles, offres(row,col)/100, x(k), alpha(row,col), T1(row,col)/100, T2(row,col)/10 );
    #     end
    #     figure; plot(Z); xlabel('M0'); ylabel('f(x)');
    # end
    #
    # if false %plot alpha
    #     nx=200;
    #     x=linspace(alpha(row,col)-alpha(row,col)*.2,alpha(row,col)+alpha(row,col)*.2,nx); %M0
    #     Z=zeros(nx,1);
    #     for k=1:nx
    #         Z(k)=ellipticalfit( I', TE, TR, phasecycles, offres(row,col)/100, 1, x(k), T1(row,col)/100, T2(row,col)/10 );
    #     end
    #     figure; plot(Z); xlabel('M0'); ylabel('f(x)');
    # end
    #
    # # contour plot for M0 and alpha
    # if false
    #     nx=200;
    #     ny=200;
    #     x=linspace(0,2,nx); %M0
    #     y=linspace((alpha(row,col)-alpha(row,col)*.2),(alpha(row,col)+alpha(row,col)*.2),ny); %alpha
    #     [X,Y]=ndgrid(x,y);
    #     Z=zeros(nx,ny);
    #     for k=1:nx
    #         for kk=1:ny
    #             [Z(k,kk)]=ellipticalfit( I', TE, TR, phasecycles, offres(row,col)/100, X(k,kk), Y(k,kk), T1(row,col)/100, T2(row,col)/10 );
    #         end
    #     end
    #     figure; contour(X,Y,Z,50); xlabel('M0'); ylabel('Alpha in radians'); hold on;
    #     plot(1, alpha(row,col), 'kx');
    #     colorbar(); title('Fitting');
    #
    # %contour plot for M0 and off-resonance
    # if false
    # nx=200;
    # ny=200;
    # x=linspace(0,10,nx); %M0
    # y=linspace(0,400,ny); %off-resonance
    # [X,Y]=ndgrid(x,y);
    # Z=zeros(nx,ny);
    # check=ellipticalfit( I', TE, TR, phasecycles, offres(row,col)/100, 1/10, alpha(row,col), T1(row,col)/1000, T2(row,col)/100 );
    # for k=1:nx
    #     for kk=1:ny
    #         [Z(k,kk)]=norm(ellipticalfit( I', TE, TR, phasecycles, Y(k,kk)/100, X(k,kk)/10, alpha(row,col), T1(row,col)/1000, T2(row,col)/100 ));
    #     end
    # end
    # figure; contour(X,Y,Z,50); xlabel('M0'); ylabel('Off-resonance in Hz'); hold on;
    # plot(1, offres(row,col), 'kx');
    # colorbar(); title('Fitting');
    # end
    #
    # %contour plot for M0 and T1
    # if false
    # nx=200;
    # ny=200;
    # x=linspace(0,10,nx); %M0
    # y=linspace(200,1500,ny); %T2
    # [X,Y]=ndgrid(x,y);
    # Z=zeros(nx,ny);
    # for k=1:nx
    #     for kk=1:ny
    #         [Z(k,kk)]=norm(ellipticalfit( I', TE, TR, phasecycles, offres(row,col)/100, X(k,kk)/10, alpha(row,col), Y(k,kk)/1000, T2(row,col)/100 ));
    #     end
    # end
    # figure; contour(X,Y,Z,50); xlabel('M0'); ylabel('T1 ms'); hold on;
    # plot(1, T1(row,col), 'kx');
    # colorbar(); title('Fitting');
    # end
    #
    # %contour plot for M0 and T2
    # if false
    # nx=200;
    # ny=200;
    # x=linspace(0,10,nx); %M0
    # y=linspace(5,200,ny); %T2
    # [X,Y]=ndgrid(x,y);
    # Z=zeros(nx,ny);
    # for k=1:nx
    #     for kk=1:ny
    #         [Z(k,kk)]=norm(ellipticalfit( I', TE, TR, phasecycles, offres(row,col)/100, X(k,kk)/10, alpha(row,col), T1(row,col)/1000, Y(k,kk)/100 ));
    #     end
    # end
    # figure; contour(X,Y,Z,50); xlabel('M0'); ylabel('T2 ms'); hold on;
    # plot(1, T2(row,col), 'kx');
    # colorbar(); title('Fitting');
    # end
    #
    # %contour plot for off-resonance and alpha
    # if false
    # nx=200;
    # ny=200;
    # x=linspace(0,100,nx); %off-resonance
    # y=linspace((alpha(row,col)-alpha(row,col)*.2),(alpha(row,col)+alpha(row,col)*.2),ny); %alpha
    # [X,Y]=ndgrid(x,y);
    # Z=zeros(nx,ny);
    # for k=1:nx
    #     for kk=1:ny
    #         [Z(k,kk)]=ellipticalfit( I', TE, TR, phasecycles, X(k,kk)/100, 1, Y(k,kk), T1(row,col)/100, T2(row,col)/10 );
    #     end
    # end
    # figure; contour(X,Y,Z,50); xlabel('Off-resonance in Hz'); ylabel('Alpha in radians'); hold on;
    # plot(offres(row,col), alpha(row,col), 'kx');
    # colorbar(); title('Fitting');
    # end
    #
    # %contour for T1 and T2
    # if false
    # nx=200;
    # ny=200;
    # x=linspace(200,1500,nx); %for fat 200:1200
    # y=linspace(5,200,ny); %for fat 20:200
    # [X,Y]=ndgrid(x,y);
    # Z=zeros(nx,ny);
    # for k=1:nx
    #     for kk=1:ny
    #         [Z(k,kk)]=norm(ellipticalfit( I', TE, TR, phasecycles, offres(row,col)/100, 1/10, alpha(row,col), X(k,kk)/1000, Y(k,kk)/100 ));
    #     end
    # end
    # figure; contour(X,Y,Z,50); xlabel('T1'); ylabel('T2'); hold on;
    # plot(T1(row,col), T2(row,col), 'kx');
    # colorbar(); title('Fitting');
    # end

if __name__ == '__main__':

    param_map(disp=True)
