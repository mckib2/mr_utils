'''readParcFileEntries'''

import logging
import os

import numpy as np

def readParcFileEntries(siemens_dat, ParcRaidHead, VBFILE):
    '''
    struct MrParcRaidFileEntry
    {
      uint32_t measId_;
      uint32_t fileId_;
      uint64_t off_;
      uint64_t len_;
      char patName_[64];
      char protName_[64];
    };
    '''

    #TODO: Using a list right now, structured np array would probably be better
    NUM_ENTRIES = 64
    ParcFileEntries = []

    if VBFILE:
        logging.info('VB line file detected.')

        # In case of VB file, we are just going to fill these with zeros.
        # It doesn't exist.
        for ii in range(NUM_ENTRIES):
            ParcFileEntries.append({
                'measId_':0,
                'fileId_':0,
                'off_':0,
                'len_':0,
                'patName_':'',
                'protName_':''})

        ParcFileEntries[0]['off_'] = 0

        # Rewind a bit, we have no raid file header.
        siemens_dat.seek(0, os.SEEK_END)

        # This is the whole size of the dat file
        ParcFileEntries[0]['len_'] = siemens_dat.tell()

        # Rewind a bit, we have no raid file header.
        siemens_dat.seek(0, os.SEEK_SET)

        # blank
        logging.info('Protocol name: %s', ParcFileEntries[0]['protName_'])

    else:
        logging.info('VD line file detected.')

        for ii in range(NUM_ENTRIES):
            entry = {}
            entry['measId_'], entry['fileId_'] = np.fromfile(
                siemens_dat, dtype=np.uint32, count=2) #pylint: disable=E1101
            entry['off_'], entry['len_'] = np.fromfile(
                siemens_dat, dtype=np.uint64, count=2) #pylint: disable=E1101
            entry['patName_'], entry['protName_'] = np.fromfile(
                siemens_dat, dtype='U64', count=2) # could be S64?

            ParcFileEntries.append(entry)

            if ii < ParcRaidHead['count_']:
                logging.info(
                    'Protocol name: %s', ParcFileEntries[ii]['protName_'])

    return ParcFileEntries
