
# SIM
## mr_utils.sim.bloch.bloch

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/sim/bloch/bloch.py)

```
NAME
    mr_utils.sim.bloch.bloch

FUNCTIONS
    gre(T1, T2, M0, Nt, h, alpha, beta, gamma, TR, TE, Bx=0, By=0, Bz=3)
        Finite difference Bloch simulation of spoiled GRE pulse sequence.
        
        T1 -- longitudinal relaxation constant.
        T2 -- transverse relaxation constant.
        M0 -- value at thermal equilibrium.
        Nt -- number of time points for finite difference solution.
        h -- step size for finite difference solutions.
        alpha,beta,gamma -- RF pulse tip angles.
        TR -- repetition time.
        TE -- echo time.
        Bx -- x component of magnetic field.
        By -- y component of magnetic field.
        Bz -- z component of magnetic field.
        
        T1,T2,M0 can be arrays (must be same size) to simulate phantoms.
    
    rotation(alpha, beta, gamma)
        Create 3D rotation matrix from alpha,beta,gamma.
    
    sim(T1, T2, M0, Nt, h, alpha, beta, gamma, Bx=0, By=0, Bz=3)
        Finite difference solution to Bloch equations.
        
        T1 -- longitudinal relaxation constant.
        T2 -- transverse relaxation constant.
        M0 -- value at thermal equilibrium.
        Nt -- number of time points for finite difference solution.
        h -- step size for finite difference solutions.
        alpha,beta,gamma -- RF pulse tip angles.
        Bx -- x component of magnetic field.
        By -- y component of magnetic field.
        Bz -- z component of magnetic field.
        
        T1,T2,M0 can be arrays (must be same size) to simulate phantoms.
        
        See:
        https://en.wikipedia.org/wiki/Bloch_equations#Matrix_form_of_Bloch_equations
    
    sim_loop(T1, T2, M0, Nt, h, alpha, beta, gamma, Bx=0, By=0, Bz=3)
        Loop implementation to verify matrix implementation.


```

