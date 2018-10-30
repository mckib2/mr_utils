import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pathlib
from mr_utils.load_data import load_raw,load_mat
from skimage.util import montage as skimontage
from mr_utils.view.mat_keys import mat_keys

def view(
        filename,
        load_opts={},
        is_raw=None,
        raw_loader='s2i',
        prep=None,
        fft=False,
        fft_axes=(0,1),
        fftshift=None,
        mag=None,
        cmap='gray',
        montage=False,
        montage_axis=-1,
        montage_opts={'padding_width':2},
        movie=False,
        movie_axis=-1,
        movie_repeat=True,
    ):
    '''Image viewer to quickly inspect data.

    filename -- Name of the file including the file extension.
    load_opts -- Options to pass to data loader.

    is_raw -- Inform if data is raw. Will attempt to guess from extension.
    raw_loader -- Raw data loader to use (see mr_utils.load_data.load_raw).
    prep -- Lambda function to process the data before it's displayed.

    fft -- Whether or not to perform n-dimensional FFT of data.
    fft_axes -- Axis to perform FFT over, determines dimension of n-dim FFT.
    fftshift -- Whether or not to perform fftshift. Defaults to True if fft.

    mag -- View magnitude image. Defaults to True if data is complex.
    cmap -- Color map to use in plot.

    montage -- View images as a montage.
    montage_axis -- Which axis is the number of images to be shown.
    montage_opts -- Additional options to pass to the skimage.util.montage.

    movie -- Whether or not the data is to be played as a movie.
    movie_axis -- Which axis is the number of frames of the movie.
    movie_repeat -- Whether or not to put movie on endless loop.
    '''

    # Find the file extension
    ext = pathlib.Path(filename).suffix

    # If the user says data is raw, then trust the user
    if is_raw or (ext == '.dat'):
        data = load_raw(filename,use=raw_loader)
    elif ext == '.npy':
        data = np.load(filename)
    elif ext == '.mat':
        # Help out the user a little bit...  If only one nontrivial key is
        # found then go ahead and assume it's that one
        data = None
        if not len(list(load_opts)):
            keys = mat_keys(filename,no_print=True)
            if len(keys) == 1:
                data = load_mat(filename,key=keys[0])

        # If we can't help the user out, just load it as normal
        if data is None:
            data = load_mat(filename,**load_opts)
    else:
        raise Exception('File type %s not understood!' % ext)

    # Perform n-dim FFT across fft_axes if desired
    if fft:
        data = np.fft.fftn(data,axes=fft_axes)

    # Perform fftshift if desired.  If the user does not specify fftshift, if
    # fft is performed, then fftshift will also be performed.  To override this
    # behavior, simply supply fftshift=False in the arguments.  Similarly, to
    # force fftshift even if no fft was performed, supply fftshift=True.
    if (fft and (fftshift is None)):
        fftshift = True
    else:
        fftshift = False
    if fftshift:
        data = np.fft.fftshift(data)

    # Take absolute value to view if necessary
    if (np.any(np.iscomplex(data))) or (mag is True):
        data = np.abs(data)

    # Run any processing before imshow
    if callable(prep):
        data = prep(data)

    # Show the image.  Let's also try to help the user out again.  If we have
    # 3 dimensions, one of them is probably a montage or a movie.  If the user
    # didn't tell us anything, it's going to crash anyway, so let's try
    # guessing what's going on...
    if (data.ndim > 2) and (not movie) and (not montage):
        print('Data has more than 2 dimensions!',end=' ')

        # assume inplane resolution larger than movie/montage dim
        min_axis = np.argmin(data.shape)

        # Assume 10 is the most we'll want to montage
        if data.shape[min_axis] < 10:
            print('Guessing axis %d is montage...' % min_axis)
            montage = True
            montage_axis = min_axis
        else:
            print('Guessing axis %d is movie...' % min_axis)
            movie = True
            movie_axis = min_axis

    if montage:
        # Put the montage axis in front
        data = np.moveaxis(data,montage_axis,0)
        data = skimontage(data,**montage_opts)

    if movie:
        fig = plt.figure()
        data = np.moveaxis(data,movie_axis,-1)
        im = plt.imshow(data[...,0])

        def updatefig(frame):
            im.set_array(data[...,frame])
            return im,

        ani = animation.FuncAnimation(fig,updatefig,frames=data.shape[-1],interval=50,blit=True,repeat=movie_repeat)
        plt.show()
    else:
        plt.imshow(data,cmap=cmap)
        plt.show()

if __name__ == '__main__':
    pass
