'''A simple viewer.

The idea is for this to be really simple to use.  It will do a lot of
guessing if you don't provide it with details.  For example, if a 3D dataset
is provided as the image and you don't say which axes are in-plane, it will
guess that the largest two axis are in-plane.  If the 3rd dimension is small,
then it will choose to view the images as a montage, if it is large it will
play it as a movie.  Of course there are many options if you know what you're
doing (and I do, since I wrote it...).

Fourier transforms, logarithmic scale, coil combination, averaging, and
converting from raw data are all supported out of the box.
'''

import logging
import pathlib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.util import montage as skimontage
from ismrmrdtools.coils import calculate_csm_walsh, calculate_csm_inati_iter

from mr_utils.load_data import load_raw, load_mat
from mr_utils.coils.coil_combine import coil_pca

def mat_keys(filename, ignore_dbl_underscored=True, no_print=False):
    '''Give the keys found in a .mat filcoil_ims,coil_dim=-1,n_components=4e.

    filename -- .mat filename.
    ignore_dbl_underscored -- Remove keys beginng with two underscores.
    '''

    data = load_mat(filename)
    keys = list(data.keys())

    if ignore_dbl_underscored:
        keys = [x for x in keys if not x.startswith('__')]

    if not no_print:
        print('Keys: ', keys)

    return keys

def view(
        image,
        load_opts={},
        is_raw=None,
        prep=None,
        fft=False,
        fft_axes=None,
        fftshift=None,
        avg_axis=None,
        coil_combine_axis=None,
        coil_combine_method='walsh',
        coil_combine_opts={},
        is_imspace=False,
        mag=None,
        phase=False,
        log=False,
        imshow_opts={'cmap':'gray'},
        montage_axis=None,
        montage_opts={'padding_width':2},
        movie_axis=None,
        movie_repeat=True,
        save_npy=False,
        debug_level=logging.DEBUG,
        test_run=False
    ):
    '''Image viewer to quickly inspect data.

    image -- Name of the file including the file extension or numpy array.
    load_opts -- Options to pass to data loader.

    is_raw -- Inform if data is raw. Will attempt to guess from extension.
    prep -- Lambda function to process the data before it's displayed.

    fft -- Whether or not to perform n-dimensional FFT of data.
    fft_axes -- Axis to perform FFT over, determines dimension of n-dim FFT.
    fftshift -- Whether or not to perform fftshift. Defaults to True if fft.

    avg_axis -- Take average over given set of axes.
    coil_combine_axis -- Which axis to perform coil combination over.
    coil_combine_method -- Method to use to combine coils.
    coil_combine_opts -- Options to pass to the coil combine method.
    is_imspace -- Whether or not the data is in image space. For coil combine.

    mag -- View magnitude image. Defaults to True if data is complex.
    phase -- View phase image.
    log -- View log of magnitude data. Defaults to False.
    imshow_opts -- Options to pass to imshow. Defaults to { 'cmap'='gray' }.

    montage_axis -- Which axis is the number of images to be shown.
    montage_opts -- Additional options to pass to the skimage.util.montage.

    movie_axis -- Which axis is the number of frames of the movie.
    movie_repeat -- Whether or not to put movie on endless loop.

    save_npy -- Whether or not to save the output as npy file.

    debug_level -- Level of verbosity. See logging module.
    test_run -- Doesn't show figure, returns debug object. Mostly for testing.
    '''

    # Set up logging...
    logging.basicConfig(format='%(levelname)s: %(message)s', level=debug_level)

    # If the user wants to look at numpy matrix, recognize that filename is the
    # matrix:
    if isinstance(image, np.ndarray):
        logging.info('Image is a numpy array!')
        data = image
    elif isinstance(image, list):
        # If user sends a list, try casting to numpy array
        logging.info('Image is a list, trying to cast as numpy array...')
        data = np.array(image)
    else:
        # Find the file extension
        ext = pathlib.Path(image).suffix

        # If the user says data is raw, then trust the user
        if is_raw or (ext == '.dat'):
            data = load_raw(image, **load_opts)
        elif ext == '.npy':
            data = np.load(image, **load_opts)
        elif ext == '.mat':
            # Help out the user a little bit...  If only one nontrivial key is
            # found then go ahead and assume it's that one
            data = None
            if not len(list(load_opts)):
                keys = mat_keys(image, no_print=True)
                if len(keys) == 1:
                    logging.info('No key supplied, but one key for mat \
                        dictionary found (%s), using it...', keys[0])
                    data = load_mat(image, key=keys[0])

            # If we can't help the user out, just load it as normal
            if data is None:
                data = load_mat(image, **load_opts)
        elif ext == '.h5':
            raise NotImplementedError();
        else:
            raise Exception('File type %s not understood!' % ext)


    # Right off the bat, remove singleton dimensions
    if 1 in data.shape:
        logging.info('Current shape %s: Removing singleton dimensions...',
                     str(data.shape))
        data = data.squeeze()
        logging.info('New shape: %s', str(data.shape))

    # Average out over any axis specified
    if avg_axis is not None:
        data = np.mean(data, axis=avg_axis)

    # Let's collapse the coil dimension using the specified algorithm
    if coil_combine_axis is not None:

        # We'll need to know the fft_axes if the data is in kspace
        if not is_imspace and fft_axes is None:
            raise ValueError(
                'fft_axes required to do coil combination of k-space data!')

        if coil_combine_method == 'walsh':
            assert len(fft_axes) == 2, 'Walsh only works with 2D images!'
            logging.info('Performing Walsh 2d coil combine across axis %d...',
                         list(range(data.ndim))[coil_combine_axis])

            # We need to do this is image domain...
            if not is_imspace:
                fft_data = np.fft.ifftshift(np.fft.ifftn(
                    data, axes=fft_axes), axes=fft_axes)
            else:
                fft_data = data

            # walsh expects (coil,y,x)
            fft_data = np.moveaxis(fft_data, coil_combine_axis, 0)
            csm_walsh, _ = calculate_csm_walsh(fft_data, **coil_combine_opts)
            fft_data = np.sum(
                csm_walsh*np.conj(fft_data), axis=0, keepdims=True)

            # Sum kept the axis where coil used to be so we can rely on
            # fft_axes to be correct when do the FT back to kspace
            fft_data = np.moveaxis(fft_data, 0, coil_combine_axis)

            # Now move back to kspace and squeeze the dangling axis
            if not is_imspace:
                data = np.fft.fftn(np.fft.fftshift(
                    fft_data, axes=fft_axes), axes=fft_axes).squeeze()
            else:
                data = fft_data.squeeze()

        elif coil_combine_method == 'inati':

            logging.info('Performing Inati coil combine across axis %d...',
                         list(range(data.ndim))[coil_combine_axis])

            # Put things into image space if we need to
            if not is_imspace:
                fft_data = np.fft.ifftshift(np.fft.ifftn(
                    data, axes=fft_axes), axes=fft_axes)
            else:
                fft_data = data

            # inati expects (coil,z,y,x)
            fft_data = np.moveaxis(fft_data, coil_combine_axis, 0)
            _, fft_data = calculate_csm_inati_iter(
                fft_data, **coil_combine_opts)

            # calculate_csm_inati_iter got rid of the axis, so we need to add
            # it back in so we can use the same fft_axes
            fft_data = np.expand_dims(fft_data, coil_combine_axis)

            # Now move back to kspace and squeeze the dangling axis
            if not is_imspace:
                data = np.fft.fftn(np.fft.fftshift(
                    fft_data, axes=fft_axes), axes=fft_axes).squeeze()
            else:
                data = fft_data.squeeze()

        elif coil_combine_method == 'pca':
            logging.info('Performing PCA coil combine across axis %d...',
                         list(range(data.ndim))[coil_combine_axis])

            # We don't actually care whether we do this is in kspace or imspace
            if not is_imspace:
                logging.info('PCA doesn\'t care that image might not be in \
                    image space.')

            if 'n_components' not in coil_combine_opts:
                n_components = int(data.shape[coil_combine_axis]/2)
                logging.info('Deciding to use %d components.', n_components)
                coil_combine_opts['n_components'] = n_components

            data = coil_pca(
                data, coil_dim=coil_combine_axis, **coil_combine_opts)

        else:
            logging.error('Coil combination method "%s" not supported!',
                          coil_combine_method)
            logging.warning('Attempting to skip coil combination!')


    # Show the image.  Let's also try to help the user out again.  If we have
    # 3 dimensions, one of them is probably a montage or a movie.  If the user
    # didn't tell us anything, it's going to crash anyway, so let's try
    # guessing what's going on...
    if (data.ndim > 2) and (movie_axis is None) and (montage_axis is None):
        logging.info('Data has %d dimensions!', data.ndim)

        # We will always assume that inplane resolution is larger than the
        # movie/montage dimensions

        # If only 3 dims, then one must be montage/movie dimension
        if data.ndim == 3:
            # assume inplane resolution larger than movie/montage dim
            min_axis = np.argmin(data.shape)

            # Assume 10 is the most we'll want to montage
            if data.shape[min_axis] < 10:
                logging.info('Guessing axis %d is montage...', min_axis)
                montage_axis = min_axis
            else:
                logging.info('Guessing axis %d is movie...', min_axis)
                movie_axis = min_axis

        # If 4 dims, guess smaller dim will be montage, larger guess movie
        elif data.ndim == 4:
            montage_axis = np.argmin(data.shape)

            # Consider the 4th dimension as the color channel in skimontage
            montage_opts['multichannel'] = True

            # Montage will go through skimontage which will remove the
            # montage_axis dimension, so find the movie dimension without the
            # montage dimension:
            tmp = np.delete(data.shape[:], montage_axis)
            movie_axis = np.argmin(tmp)

            logging.info('Guessing axis %d is montage, axis %d will be \
                movie...', montage_axis, movie_axis)


    # fft and fftshift will require fft_axes.  If the user didn't give us
    # axes, let's try to guess them:
    if (fft or (fftshift is not False)) and (fft_axes is None):
        all_axes = list(range(data.ndim))

        if (montage_axis is not None) and (movie_axis is not None):
            fft_axes = np.delete(
                all_axes, [all_axes[montage_axis], all_axes[movie_axis]])
        elif montage_axis is not None:
            fft_axes = np.delete(all_axes, all_axes[montage_axis])
        elif movie_axis is not None:
            fft_axes = np.delete(all_axes, all_axes[movie_axis])
        else:
            fft_axes = all_axes

        logging.info(
            'User did not supply fft_axes, guessing %s...', str(fft_axes))

    # Perform n-dim FFT across fft_axes if desired
    if fft:
        data = np.fft.fftn(data, axes=fft_axes)

    # Perform fftshift if desired.  If the user does not specify fftshift, if
    # fft is performed, then fftshift will also be performed.  To override this
    # behavior, simply supply fftshift=False in the arguments.  Similarly, to
    # force fftshift even if no fft was performed, supply fftshift=True.
    if fft and (fftshift is None):
        fftshift = True
    elif fftshift is None:
        fftshift = False

    if fftshift:
        data = np.fft.fftshift(data, axes=fft_axes)

    # Take absolute value to view if necessary, must take abs before log
    if np.iscomplexobj(data) or (mag is True) or (log is True):
        data = np.abs(data)

        if log:
            # Don't take log of 0!
            data[data == 0] = np.nan
            data = np.log(data)


    # If we asked for phase, let's work out how we'll do that
    if phase and ((mag is None) or (mag is True)):
        # TODO: figure out which axis to concatenate the phase onto
        data = np.concatenate((data, np.angle(data)), axis=fft_axes[-1])
    elif phase and (mag is False):
        data = np.angle(data)


    # Run any processing before imshow
    if callable(prep):
        data = prep(data)


    if montage_axis is not None:
        # We can deal with 4 dimensions if we allow multichannel
        if data.ndim == 4 and 'multichannel' not in montage_opts:
            montage_opts['multichannel'] = True

            # When we move the movie_axis to the end, we will need to adjust
            # the montage axis in case we displace it.  We need to move it to
            # the end so skimontage will consider it the multichannel
            data = np.moveaxis(data, movie_axis, -1)
            if movie_axis < montage_axis:
                montage_axis -= 1

        # Put the montage axis in front
        data = np.moveaxis(data, montage_axis, 0)
        data = skimontage(data, **montage_opts)

        if data.ndim == 3:
            # If we had 4 dimensions, we just lost one, so now we need to know
            # where the movie dimension went off to...
            if movie_axis > montage_axis:
                movie_axis -= 1
            # Move the movie axis back, it's no longer the color channel
            data = np.moveaxis(data, -1, movie_axis)

    if movie_axis is not None:
        fig = plt.figure()
        data = np.moveaxis(data, movie_axis, -1)
        im = plt.imshow(data[..., 0], **imshow_opts)

        def updatefig(frame):
            im.set_array(data[..., frame])
            return im,  # pylint: disable=R1707

        ani = animation.FuncAnimation(
            fig,
            updatefig,
            frames=data.shape[-1],
            interval=50,
            blit=True,
            repeat=movie_repeat)

        if not test_run:
            plt.show()
    else:
        if data.ndim == 1:
            plt.plot(data)
        elif data.ndim == 2:
            # Just a regular old 2d image...
            plt.imshow(data, **imshow_opts)
        else:
            raise ValueError('%d is too many dimensions!' % data.ndim)

        if not test_run:
            plt.show()

    # Save what we looked at if desired
    if save_npy:
        if ext:
            filename = image
        else:
            filename = 'view-output'
        np.save(filename, data)

    # If we're testing, return all the local vars
    if test_run:
        return locals()

if __name__ == '__main__':

    # Quick commandline interface
    import argparse
    parser = argparse.ArgumentParser(
        description='Image viewer to quickly inspect data.')

    class StoreDictKeyPair(argparse.Action):
        '''Utility for ArgumentParser to store key/val pair.'''

        def __call__(self, parser, namespace, values, option_string=None):
            my_dict = {}
            for kv in values.split(","):
                k, v = kv.split("=")
                my_dict[k] = v
            setattr(namespace, self.dest, my_dict)


    parser.add_argument('-i', metavar='image', dest='image', \
        help='Name of the file including the file extension or numpy array.', \
        required=True)
    parser.add_argument('--load_opts', action=StoreDictKeyPair, \
        metavar='KEY1=VAL1,KEY2=VAL2...', \
        help='Options to pass to data loader', default={})
    parser.add_argument('--is_raw', action='store_true', \
        help='Inform if data is raw. Will attempt to guess from extension.', \
        default=None)
    parser.add_argument('--fft', action='store_true', \
        help='Whether or not to perform n-dimensional FFT of data.')
    parser.add_argument('--fft_axes', nargs='*', type=int, metavar='axis', \
        help='Axis to perform FFT over, determines dimension of n-dim FFT.', \
        default=None)
    parser.add_argument('--fftshift', action='store_true', \
        help='Whether or not to perform fftshift. Defaults to True if fft.', \
        default=None)
    parser.add_argument('--mag', action='store_true', \
        help='View magnitude image. Defaults to True if data is complex.', \
        default=None)
    parser.add_argument('--log', action='store_true', \
        help='View log of magnitude data. Defaults to False.')
    parser.add_argument('--cmap', help='Color map to use in plot.', \
        default='gray')
    parser.add_argument('--montage_axis', nargs=1, type=int, metavar='axis', \
        help='Which axis is the number of images to be shown.', default=None)
    parser.add_argument('--montage_opts', action=StoreDictKeyPair, \
        metavar='KEY1=VAL1,KEY2=VAL2...', \
        help='Additional options to pass to the skimage.util.montage.', \
        default={'padding_width':2})
    parser.add_argument('--movie_axis', nargs=1, type=int, metavar='axis', \
        help='Which axis is the number of frames of the movie.', default=None)
    parser.add_argument('--movie_no_repeat', action='store_false', \
        dest='movie_repeat', \
        help='Whether or not to put movie on endless loop.', default=True)

    args = parser.parse_args()

    view(**vars(args))
