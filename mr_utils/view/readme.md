
# VIEW
## mr_utils.view.view

[Source](https://github.com/mckib2/mr_utils/blob/master/mr_utils/view/view.py)

```
NAME
    mr_utils.view.view - A simple viewer.

DESCRIPTION
    The idea is for this to be really simple to use.  It will do a lot of
    guessing if you don't provide it with details.  For example, if a 3D dataset
    is provided as the image and you don't say which axes are in-plane, it will
    guess that the largest two axis are in-plane.  If the 3rd dimension is small,
    then it will choose to view the images as a montage, if it is large it will
    play it as a movie.  Of course there are many options if you know what you're
    doing (and I do, since I wrote it...).
    
    Fourier transforms, logarithmic scale, coil combination, averaging, and
    converting from raw data are all supported out of the box.

FUNCTIONS
    mat_keys(filename, ignore_dbl_underscored=True, no_print=False)
        Give the keys found in a .mat filcoil_ims,coil_dim=-1,n_components=4e.
        
        filename -- .mat filename.
        ignore_dbl_underscored -- Remove keys beginng with two underscores.
    
    view(image, load_opts={}, is_raw=None, is_line=None, prep=None, fft=False, fft_axes=None, fftshift=None, avg_axis=None, coil_combine_axis=None, coil_combine_method='walsh', coil_combine_opts={}, is_imspace=False, mag=None, phase=False, log=False, imshow_opts={'cmap': 'gray'}, montage_axis=None, montage_opts={'padding_width': 2}, movie_axis=None, movie_repeat=True, save_npy=False, debug_level=10, test_run=False)
        Image viewer to quickly inspect data.
        
        image -- Name of the file including the file extension or numpy array.
        load_opts -- Options to pass to data loader.
        
        is_raw -- Inform if data is raw. Will attempt to guess from extension.
        is_line -- Whether or not this is a line plot (as opposed to image).
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


```

