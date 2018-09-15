import numpy as np

def load_raw(
    filename,
    use='bart',
    bart_args='-A',
    s2i_ROS=True):

    if use == 'bart':
        from bart import bart,cfl
        from tempfile import NamedTemporaryFile
        from subprocess import Popen,PIPE
        from os import remove

        # I can't figure out how to use the prebaked bart interface to get
        # twixread to work, so I'll just do this...
        tmp_name = NamedTemporaryFile().name
        cmd = 'bart twixread %s %s %s' % (bart_args,filename,tmp_name)
        print(cmd)
        # data = bart(1,'twixread %s %s' % (bart_args,filename))
        process = Popen(cmd.split(),stdout=PIPE)
        output,error = process.communicate()
        if output is not None:
            print(output.decode('utf-8'))
            data = cfl.readcfl(tmp_name).squeeze()
            remove('%s.cfl' % tmp_name)
            remove('%s.hdr' % tmp_name)

        if error is not None:
            print(error)
            raise Exception("BART exited with an error.")

    elif use == 's2i':
        from tempfile import NamedTemporaryFile
        from subprocess import Popen,PIPE
        import ismrmrd

        tmp_name = NamedTemporaryFile().name

        cmd = 'siemens_to_ismrmrd -f %s -o %s' % (filename,tmp_name)
        process = Popen(cmd.split(),stdout=PIPE)
        output,error = process.communicate()
        if output is not None:
            print(output.decode('utf-8'))

            # Load in the file and start getting to work...
            # See https://github.com/ismrmrd/ismrmrd-python-tools/blob/master/recon_ismrmrd_dataset.py
            dset = ismrmrd.Dataset(tmp_name,'/dataset',False)

            header = ismrmrd.xsd.CreateFromDocument(dset.read_xml_header())
            enc = header.encoding[0]
            # print(dset.read_xml_header().decode('utf-8'))

            # Matrix size
            eNx = enc.encodedSpace.matrixSize.x
            eNy = enc.encodedSpace.matrixSize.y
            eNz = enc.encodedSpace.matrixSize.z
            rNx = enc.reconSpace.matrixSize.x
            rNy = enc.reconSpace.matrixSize.y
            rNz = enc.reconSpace.matrixSize.z

            # Field of View
            eFOVx = enc.encodedSpace.fieldOfView_mm.x
            eFOVy = enc.encodedSpace.fieldOfView_mm.y
            eFOVz = enc.encodedSpace.fieldOfView_mm.z
            rFOVx = enc.reconSpace.fieldOfView_mm.x
            rFOVy = enc.reconSpace.fieldOfView_mm.y
            rFOVz = enc.reconSpace.fieldOfView_mm.z

            #Parallel imaging factor
            acc_factor = enc.parallelImaging.accelerationFactor.kspace_encoding_step_1

            # Number of Slices, Avgs, Contrasts, etc. - Note we Reps are not counted here
            ncoils = header.acquisitionSystemInformation.receiverChannels
            if enc.encodingLimits.slice != None:
                nslices = enc.encodingLimits.slice.maximum + 1
            else:
                nslices = 1

            if enc.encodingLimits.average != None:
                navgs = enc.encodingLimits.average.maximum + 1
            else:
                navgs = 1

            if enc.encodingLimits.contrast != None:
                ncontrasts = enc.encodingLimits.contrast.maximum + 1
            else:
                ncontrasts = 1

            # In case there are noise scans in the actual dataset, we will skip them.
            firstacq=0
            for acqnum in range(dset.number_of_acquisitions()):
                acq = dset.read_acquisition(acqnum)

                if acq.isFlagSet(ismrmrd.ACQ_IS_NOISE_MEASUREMENT):
                    print("Found noise scan at acq ", acqnum)
                    continue
                else:
                    firstacq = acqnum
                    print("Imaging acquisition starts acq ", acqnum)
                    break

            #Calculate prewhiterner taking BWs into consideration
            a = dset.read_acquisition(firstacq)
            data_dwell_time = a.sample_time_us
            noise_receiver_bw_ratio = 0.79
            # dmtx = coils.calculate_prewhitening(noise,scale_factor=(data_dwell_time/noise_dwell_time)*noise_receiver_bw_ratio)

            # Process the actual data
            all_data = np.zeros((navgs, ncontrasts, nslices, ncoils, eNz, eNy, rNx), dtype=np.complex64)

            # Loop through the rest of the acquisitions and stuff
            for acqnum in range(firstacq,dset.number_of_acquisitions()):
                acq = dset.read_acquisition(acqnum)

                acq_data_prw = acq.data #coils.apply_prewhitening(acq.data,dmtx)

                # Remove oversampling if needed
                if s2i_ROS and (eNx != rNx):
                    xline = np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(acq_data_prw,axes=(1)),axis=(1)),axes=(1))
                    xline *= np.sqrt(np.prod(np.take(xline.shape,(1))))

                    x0 = int((eNx - rNx) / 2)
                    x1 = int((eNx - rNx) / 2 + rNx)
                    xline = xline[:,x0:x1]
                    acq.resize(rNx,acq.active_channels,acq.trajectory_dimensions)
                    acq.center_sample = int(rNx/2)
                    # need to use the [:] notation here to fill the data
                    k = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(xline,axes=(1)),axis=(1)),axes=(1))
                    k /= np.sqrt(np.prod(np.take(k.shape,(1))))
                    acq.data[:] = k

                # Stuff into the buffer
                avg = acq.idx.average
                contrast = acq.idx.contrast
                slice = acq.idx.slice
                y = acq.idx.kspace_encode_step_1
                z = acq.idx.kspace_encode_step_2
                all_data[avg, contrast, slice, :, z, y, :] = acq.data

            data = all_data.astype('complex64').transpose((6,5,4,3,0,1,2)).squeeze()

        if error is not None:
            print(error)
            raise Exception("siemens_to_ismrmrd exited with an error.")

    elif use == 'rdi':
        from rawdatarinator.raw import raw
        data = raw(filename)['kSpace'].transpose((0,1,3,2))
    else:
        raise Exception('You must specify a method to read raw data in!')


    print('Dimensions are (x,y,coils,avg)')
    print(data.shape)
    return(data)


if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt
    sys.path.append("..")
    from test_data.test_data import raw_data

    data = load_raw(raw_data,use='bart')
    # data = load_raw(raw_data,use='s2i')
    # data = load_raw(raw_data,use='rdi')

    for ii in range(4):
        plt.subplot(4,1,ii+1)
        plt.imshow(np.abs(np.fft.ifftshift(np.fft.ifft2(data[:,:,ii,0].T))),cmap='gray')
    plt.show()
