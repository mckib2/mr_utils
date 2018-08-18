

def load_mat(filename,rays=72,raw=False,save=True):
    filename_npy = Path(filename).with_suffix('.npy')

    # Check to see if we've loaded this before...
    if Path(filename_npy).is_file():
        print('npy file already created...Loading now...')
        t0 = time()
        data = np.load(filename_npy)
        print('%s loaded in %g sec with dims ' % (filename_npy,time()-t0),end='')
        print(data.shape)
    else:
        print('Loading data...')
        t0 = time()
        if raw:
            key = 'kSpace'
        else:
            key = 'Image_%d_rays' % rays

        data = loadmat(filename)[key]
        print('Loaded %s in %g sec with dims ' % (filename,time()-t0),end='')

        # Scale to reasonable values
        if raw:
            scale_data = 10./np.mean(np.abs(data.flatten()))
            data *= scale_data

        # Save a npy so we can load that in next time
        if save:
            np.save(filename_npy,data)
            print('%s saved!' % filename_npy)

    return(data)
