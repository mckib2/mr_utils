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
                print('No key supplied, but one key for mat dictionary found (%s), using it...' % keys[0])
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
        im = plt.imshow(data[...,0],cmap=cmap)

        def updatefig(frame):
            im.set_array(data[...,frame])
            return im,

        ani = animation.FuncAnimation(fig,updatefig,frames=data.shape[-1],interval=50,blit=True,repeat=movie_repeat)
        plt.show()
    else:
        # Just a regular old 2d image...
        plt.imshow(data,cmap=cmap)
        plt.show()

if __name__ == '__main__':

    # Quick commandline interface
    import argparse,json
    parser = argparse.ArgumentParser(description='Image viewer to quickly inspect data.')

    class StoreDictKeyPair(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            my_dict = {}
            for kv in values.split(","):
                k,v = kv.split("=")
                my_dict[k] = v
            setattr(namespace, self.dest, my_dict)


    parser.add_argument('-f',metavar='filename',dest='filename',help='Name of the file including the file extension.',required=True)
    parser.add_argument('--load_opts',action=StoreDictKeyPair,metavar='KEY1=VAL1,KEY2=VAL2...',help='Options to pass to data loader',default={})
    parser.add_argument('--is_raw',action='store_true',help='Inform if data is raw. Will attempt to guess from extension.',default=None)
    parser.add_argument('--raw_loader',choices=['s2i','bart','rdi'],help='Raw data loader to use (see mr_utils.load_data.load_raw).',default='s2i')
    # parser.add_argument('prep -- Lambda function to process the data before it's displayed.
    parser.add_argument('--fft',action='store_true',help='Whether or not to perform n-dimensional FFT of data.')
    parser.add_argument('--fft_axes',nargs='*',type=int,metavar='axis',help='Axis to perform FFT over, determines dimension of n-dim FFT.',default=(0,1))
    parser.add_argument('--fftshift',action='store_true',help='Whether or not to perform fftshift. Defaults to True if fft.',default=None)
    parser.add_argument('--mag',action='store_true',help='View magnitude image. Defaults to True if data is complex.',default=None)
    parser.add_argument('--cmap',help='Color map to use in plot.',default='gray')
    parser.add_argument('--montage',action='store_true',help='View images as a montage.')
    parser.add_argument('--montage_axis',nargs=1,type=int,metavar='axis',help='Which axis is the number of images to be shown.',default=-1)
    parser.add_argument('--montage_opts',action=StoreDictKeyPair,metavar='KEY1=VAL1,KEY2=VAL2...',help='Additional options to pass to the skimage.util.montage.',default={'padding_width':2})
    parser.add_argument('--movie',action='store_true',help='Whether or not the data is to be played as a movie.')
    parser.add_argument('--movie_axis',nargs=1,type=int,metavar='axis',help='Which axis is the number of frames of the movie.',default=-1)
    parser.add_argument('--movie_no_repeat',action='store_false',dest='movie_repeat',help='Whether or not to put movie on endless loop.',default=True)

    args = parser.parse_args()

    view(**vars(args))
