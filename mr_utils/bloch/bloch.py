import numpy as np
import matplotlib.pyplot as plt

def rotation(alpha,beta,gamma):

    ca = np.cos(alpha)
    cb = np.cos(beta)
    cg = np.cos(gamma)

    sa = np.sin(alpha)
    sb = np.sin(beta)
    sg = np.sin(gamma)

    rot = np.array([
        [ ca*cb*cg - sa*sg,-ca*cb*sg - sa*cg,ca*sb ],
        [ sa*cb*cg + ca*sg,-sa*cb*sg + ca*cg,sa*sb ],
        [ -sb*cg,sb*sg,cb ]
    ])

    return(rot)


def sim(T1,T2,M0,Nt,h,alpha,beta,gamma,Bx=0,By=0,Bz=3,gyro=1):

    spins = np.zeros((Nt,3,) + M0.shape)
    spins[0,2,...] = M0

    wx = gyro*Bx*np.ones(T1.shape)
    wy = gyro*By*np.ones(T1.shape)
    wz = gyro*Bz*np.ones(T1.shape)

    R1 = -1/T1
    R2 = -1/T2

    # Tip
    spins[0,:,...] = rotation(alpha,beta,gamma).dot(spins[0,:,...].squeeze())[:,None,None,None]
    # print(rotation(alpha,beta,gamma).dot(spins[:,...].squeeze()))

    for tt in range(1,Nt):
        for xx in range(T1.shape[0]):
            for yy in range(T1.shape[1]):
                for zz in range(T1.shape[2]):

                    # xn = (-spins[tt-1,0,xx,yy,zz]/T2[xx,yy,zz] + gyro*Bz*spins[tt-1,1,xx,yy,zz] - gyro*By*spins[tt-1,-1,xx,yy,zz])*h + spins[tt-1,0,xx,yy,xx]
                    # yn = (-gyro*Bz*spins[tt-1,0,xx,yy,zz] - spins[tt-1,1,xx,yy,zz]/T2[xx,yy,zz] + gyro*Bx*spins[tt-1,-1,xx,yy,zz])*h + spins[tt-1,1,xx,yy,xx]
                    # zn = (gyro*By*spins[tt-1,0,xx,yy,zz] - gyro*Bx*spins[tt-1,1,xx,yy,zz] + (M0[xx,yy,zz] - spins[tt-1,-1,xx,yy,zz])/T1[xx,yy,zz])*h + spins[tt-1,-1,xx,yy,zz]
                    # spins[tt,:,xx,yy,zz] = [ xn,yn,zn ]

                    A = np.array([
                        [  R2[xx,yy,zz], wz[xx,yy,zz],-wy[xx,yy,zz] ],
                        [ -wz[xx,yy,zz], R2[xx,yy,zz], wx[xx,yy,zz] ],
                        [  wy[xx,yy,zz],-wx[xx,yy,zz], R1[xx,yy,zz] ]
                    ])
                    spins[tt,:,xx,yy,zz] = A.dot(spins[tt-1,:,xx,yy,zz])*h + spins[tt-1,:,xx,yy,zz] + np.array([ 0,0,M0[xx,yy,zz]/T1[xx,yy,zz] ])*h
                    # assert np.allclose(spins[tt,:,xx,yy,zz],[ xn,yn,zn ])

    plt.plot(np.sqrt(np.sum(spins[:,0:2,0,0,0]**2,axis=1)))
    plt.plot(spins[:,2,0,0,0])
    plt.show()

if __name__ == '__main__':

    M0 = np.ones((1,1,1))*1.0
    T1 = np.ones((1,1,1))*1.5
    T2 = np.ones((1,1,1))*0.8
    Nt = 100000
    t,h = np.linspace(0,10,Nt,retstep=True)
    print('h: %g' % h)
    print('Nt: %d' % Nt)
    alpha = 0
    beta = np.pi/2
    gamma = 0

    sim(T1,T2,M0,Nt,h,alpha,beta,gamma)
