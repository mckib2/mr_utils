import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
    import ismrmrd

import struct
import socket
import threading
import numpy as np

GADGET_MESSAGE_INT_ID_MIN                             =   0
GADGET_MESSAGE_CONFIG_FILE                            =   1
GADGET_MESSAGE_CONFIG_SCRIPT                          =   2
GADGET_MESSAGE_PARAMETER_SCRIPT                       =   3
GADGET_MESSAGE_CLOSE                                  =   4
GADGET_MESSAGE_TEXT                                   =   5
GADGET_MESSAGE_INT_ID_MAX                             = 999
GADGET_MESSAGE_EXT_ID_MIN                             = 1000
GADGET_MESSAGE_ACQUISITION                            = 1001 # DEPRECATED
GADGET_MESSAGE_NEW_MEASUREMENT                        = 1002 # DEPRECATED
GADGET_MESSAGE_END_OF_SCAN                            = 1003 # DEPRECATED
GADGET_MESSAGE_IMAGE_CPLX_FLOAT                       = 1004 # DEPRECATED
GADGET_MESSAGE_IMAGE_REAL_FLOAT                       = 1005 # DEPRECATED
GADGET_MESSAGE_IMAGE_REAL_USHORT                      = 1006 # DEPRECATED
GADGET_MESSAGE_EMPTY                                  = 1007 # DEPRECATED
GADGET_MESSAGE_ISMRMRD_ACQUISITION                    = 1008
GADGET_MESSAGE_ISMRMRD_IMAGE_CPLX_FLOAT               = 1009
GADGET_MESSAGE_ISMRMRD_IMAGE_REAL_FLOAT               = 1010 # DEPRECATED
GADGET_MESSAGE_ISMRMRD_IMAGE_REAL_USHORT              = 1011 # DEPRECATED
GADGET_MESSAGE_DICOM                                  = 1012 # DEPRECATED
GADGET_MESSAGE_CLOUD_JOB                              = 1013
GADGET_MESSAGE_GADGETCLOUD_JOB                        = 1014
GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_CPLX_FLOAT     = 1015 # DEPRECATED
GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_REAL_FLOAT     = 1016 # DEPRECATED
GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_REAL_USHORT    = 1017 # DEPRECATED
GADGET_MESSAGE_DICOM_WITHNAME                         = 1018
GADGET_MESSAGE_DEPENDENCY_QUERY                       = 1019
GADGET_MESSAGE_ISMRMRD_IMAGE_REAL_SHORT               = 1020 # DEPRECATED
GADGET_MESSAGE_ISMRMRD_IMAGEWITHATTRIB_REAL_SHORT     = 1021 # DEPRECATED
GADGET_MESSAGE_ISMRMRD_IMAGE                          = 1022
GADGET_MESSAGE_RECONDATA                              = 1023
GADGET_MESSAGE_ISMRMRD_WAVEFORM                       = 1026
GADGET_MESSAGE_EXT_ID_MAX                             = 4096

MAX_BLOBS_LOG_10 = 6

GadgetMessageIdentifier = struct.Struct('<H')
SIZEOF_GADGET_MESSAGE_IDENTIFIER = len(GadgetMessageIdentifier.pack(0))
GadgetMessageConfigurationFile = struct.Struct('<1024s')
GadgetMessageScript = struct.Struct('<I')
GadgetMessageAttribLength = struct.Struct('<Q')
SIZEOF_GADGET_MESSAGE_ATTRIB_LENGTH = len(GadgetMessageAttribLength.pack(0))
GadgetMessageBlobSize = struct.Struct('<I')
SIZEOF_GADGET_MESSAGE_BLOB_SIZE = len(GadgetMessageBlobSize.pack(0))
GadgetMessageBlobFilename = struct.Struct('<Q')
SIZEOF_GADGET_MESSAGE_BLOB_FILENAME = len(GadgetMessageBlobFilename.pack(0))


def readsock(sock, bytecount):
    """Reads a specific number of bytes from a socket"""
    chunks = []
    curcount = 0
    while curcount < bytecount:
        chunk = sock.recv(min(bytecount - curcount, 4096))
        if chunk == '':
            raise RuntimeError("socket connection closed")
        chunks.append(chunk)
        curcount += len(chunk)
    return b''.join(chunks)


class MessageReader(object):
    def read(self, sock):
        raise NotImplementedError("Must implement in derived class")

class ImageMessageReader(MessageReader):
    def __init__(self, filename, groupname):
        self.filename = filename
        self.groupname = groupname
        self.dataset = None

    def read(self, sock):
        # read image header
        serialized_header = readsock(sock, ismrmrd.hdf5.image_header_dtype.itemsize)
        img = ismrmrd.Image(serialized_header)

        # now the image's data should be a valid NumPy array of zeros
        dtype = img.data.dtype
        data_bytes = len(img.data.flat) * dtype.itemsize
        serialized_data = readsock(sock, data_bytes)
        img.data.ravel()[:] = np.frombuffer(serialized_data,dtype=dtype)

        if not self.dataset:
            # open dataset
            self.dataset = ismrmrd.Dataset(self.filename, self.groupname)

        self.dataset.append_image("image_%d" % img.image_series_index, img)


class ImageAttribMessageReader(ImageMessageReader):
    def read(self, sock):
        # read image header
        serialized_header = readsock(sock, ismrmrd.hdf5.image_header_dtype.itemsize)
        # read meta attributes
        msg = readsock(self.sock, SIZEOF_GADGET_MESSAGE_ATTRIB_LENGTH)
        attrib_len = GadgetMessageAttribLength.unpack(msg)[0]
        attribs = readsock(self.sock, attrib_len)

        # make a new image
        img = ismrmrd.Image(serialized_header, attribs)

        # now the image's data should be a valid NumPy array of zeros
        dtype = img.data.dtype
        data_bytes = len(img.data.flat) * dtype.itemsize
        serialized_data = readsock(sock, data_bytes)
        img.data.ravel()[:] = np.fromstring(serialized_data, dtype=dtype)

        if not self.dataset:
            # open dataset
            self.dataset = ismrmrd.Dataset(self.filename, self.groupname)

        self.dataset.append_image("image_%d" % img.image_series_index, img)

class BlobMessageReader(MessageReader):
    def __init__(self, prefix, suffix):
        self.prefix = prefix
        self.suffix = suffix
        self.num_calls = 0

    def read(self, sock):
        # read sizeof blob data and blob data itself
        msg = readsock(self.sock, SIZEOF_GADGET_MESSAGE_BLOB_SIZE)
        nbytes = GadgetMessageBlobSize.unpack(msg)[0]
        blob = readsock(self.sock, nbytes)

        filename = '%s_%06d.%s' (self.prefix, self.num_calls, self.suffix)
        with open(filename, 'wb') as f:
            f.write(blob)

        self.num_calls += 1

class BlobAttribMessageReader(BlobMessageReader):
    def read(self, sock):
        # read blob data
        msg = readsock(self.sock, SIZEOF_GADGET_MESSAGE_BLOB_SIZE)
        nbytes = GadgetMessageBlobSize.unpack(msg)[0]
        blob = readsock(self.sock, nbytes)

        # read filename
        msg = readsock(self.sock, SIZEOF_GADGET_MESSAGE_BLOB_FILENAME)
        filename_len = GadgetMessageBlobFilename.unpack(msg)[0]
        filename = readsock(self.sock, filename_len)

        # read meta attributes
        msg = readsock(self.sock, SIZEOF_GADGET_MESSAGE_ATTRIB_LENGTH)
        attrib_len = GadgetMessageAttribLength.unpack(msg)[0]
        attribs = readsock(self.sock, attrib_len)

        # save files
        filename_image = '%s.%s' % (filename, self.suffix)
        filename_attrib = '%s_attrib.xml' % (filename)
        if len(self.prefix) > 0:
            filename_image = '%s_%s' % (self.prefix, filename_image)
            filename_attrib = '%s_%s' % (self.prefix, filename_attrib)

        with open(filename_image, 'wb') as f:
            f.write(blob)

        with open(filename_attrib, 'wb') as f:
            f.write(attribs)

        self.num_calls += 1

class Connector(object):
    def __init__(self, hostname=None, port=None):
        if hostname and port:
            self.connect(hostname, port)
        self.readers = {}
        self.writers = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.reader_thread = None

    def connect(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.sock.connect((hostname, port))
        self.reader_thread = threading.Thread(name="GadgetronClientConnector read_task", target=self.read_task)
        self.reader_thread.start()

    def read_task(self):
        while True:
            msg = readsock(self.sock, SIZEOF_GADGET_MESSAGE_IDENTIFIER)
            kind = GadgetMessageIdentifier.unpack(msg)[0]

            if kind == GADGET_MESSAGE_CLOSE:
                print('GADGET_MESSAGE_CLOSE')
                break
            elif kind not in self.readers:
                print("***Invalid message ID received: %d" % kind)
                continue

            reader = self.readers[kind]
            reader.read(self.sock)

    def wait(self):
        self.reader_thread.join()

    def register_reader(self, kind, reader):
        self.readers[kind] = reader

    def register_writer(self, kind, writer):
        self.writers[kind] = writer

    def send_gadgetron_configuration_script(self, contents):
        msg = GadgetMessageIdentifier.pack(GADGET_MESSAGE_CONFIG_SCRIPT)
        script_len = GadgetMessageScript.pack(len(contents) + 1)
        contents_with_nul = '%s\0' % contents
        self.sock.send(msg)
        self.sock.send(script_len)
        self.sock.send(contents_with_nul)

    def send_gadgetron_configuration_file(self, filename):
        msg = GadgetMessageIdentifier.pack(GADGET_MESSAGE_CONFIG_FILE)
        cfg = GadgetMessageConfigurationFile.pack(filename.encode('utf-8'))
        self.sock.send(msg)
        self.sock.send(cfg)

    def send_gadgetron_parameters(self, xml):
        msg = GadgetMessageIdentifier.pack(GADGET_MESSAGE_PARAMETER_SCRIPT)
        script_len = GadgetMessageScript.pack(len(xml) + 1)
        xml_with_nul = b'%s\0' % xml
        self.sock.send(msg)
        self.sock.send(script_len)
        self.sock.send(xml_with_nul)

    def send_gadgetron_close(self):
        msg = GadgetMessageIdentifier.pack(GADGET_MESSAGE_CLOSE)
        self.sock.send(msg)

    def send_ismrmrd_acquisition(self, acq):
        msg = GadgetMessageIdentifier.pack(GADGET_MESSAGE_ISMRMRD_ACQUISITION)

        self.sock.send(msg)
        self.sock.send(b'%s' % acq.getHead())
        self.sock.send(acq.traj.tobytes())
        self.sock.send(acq.data.tobytes())

    def __del__(self):
        if self.sock:
            self.sock.close()
            self.sock = None
