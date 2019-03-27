'''readSyncdata'''

import os
from ctypes import c_uint32

import numpy as np

from mr_utils.load_data.s2i import sScanHeader, sMDH

def readSyncdata(siemens_dat, VBFILE, acquisitions, dma_length,
                 scanheader, header, last_scan_counter):

    if VBFILE:
        len = dma_length - sMDH.itemsize

        # Is VB magic? For now let's assume it's not, and that this
        # is just Siemens secret sauce.
        siemens_dat.seek(len, os.SEEK_CUR)
        # return std::vector<ISMRMRD::Waveform>();
        return None
    else:
        raise NotImplementedError()

        len = dma_length - sScanHeader.itemsize

        # siemens_dat.seekg(len,siemens_dat.cur)
        # return std::vector<ISMRMRD::Waveform>()
        cur_pos = siemens_dat.tell()
        packetSize = np.fromfile(
            siemens_dat, dtype=c_uint32, count=1)

        packedID = siemens_dat.read(52)

        # packedID indicates this isn't PMU data, so let's jump ship
        if 'PMU' not in packedID:
            siemens_dat.seek(cur_pos)
            siemens_dat.seek(len, os.SEEK_CUR)
            # return std::vector<ISMRMRD::Waveform>();
            return None

        learning_phase = 'PMULearnPhase' in packedID

        (swappedFlag, timestamp0, timestamp, packerNr,
         duration) = np.fromfile(siemens_dat, dtype=c_uint32, count=5)

        # magic = PMU_Type_inverse[np.fromfile(
        #     siemens_dat, dtype=c_uint32, count=1)[0]]

#         # Read in all the PMU data first, to figure out if we have
#         # multiple ECGs.
#         std::map<PMU_Type, std::tuple<std::vector<PMUdata>, uint32_t >> pmu_map;
#         std::set<PMU_Type> ecg_types = {PMU_Type::ECG1, PMU_Type::ECG2, PMU_Type::ECG3, PMU_Type::ECG4};
#         std::map<PMU_Type, std::tuple<std::vector<PMUdata>, uint32_t >> ecg_map;
#         while (magic != PMU_Type::END) {
#             //Read and store period
#             uint32_t period;
#
#             siemens_dat.read((char *) &period, sizeof(uint32_t));
#
#             //Allocate and read data
#             std::vector<PMUdata> data(duration / period);
#             siemens_dat.read((char *) data.data(), data.size() * sizeof(PMUdata));
#             //Split into ECG and PMU sets.
#             if (ecg_types.count(magic)) {
#                 ecg_map[magic] = std::make_tuple(std::move(data), period);
#             } else {
#                 pmu_map[magic] = std::make_tuple(std::move(data), period);
#             }
#             //Read next tag
#             siemens_dat.read((char *) &magic, sizeof(uint32_t));
#             if (!PMU_Types.count(magic))
#                 throw std::runtime_error("Malformed file");
#
#
#         }
#
#         //Have to handle ECG seperately.
#
#         std::vector<ISMRMRD::Waveform> waveforms;
#         waveforms.reserve(5);
#         if (ecg_map.size() > 0 || pmu_map.size() > 0) {
#
#             if (ecg_map.size() > 0) {
#
#                 size_t channels = ecg_map.size();
#                 size_t number_of_elements = std::get<0>(ecg_map.begin()->second).size();
#
#                 auto ecg_waveform = ISMRMRD::Waveform(number_of_elements, channels + 1);
#                 ecg_waveform.head.waveform_id = waveformId.at(PMU_Type::ECG1) + 5 * learning_phase;
#
#                 uint32_t *ecg_waveform_data = ecg_waveform.data;
#
#                 uint32_t *trigger_data = ecg_waveform_data + number_of_elements * channels;
#                 std::fill(trigger_data, trigger_data + number_of_elements, 0);
#                 //Copy in the data
#                 for (auto key_val : ecg_map) {
#                     auto tup = unpack_pmu(std::get<0>(key_val.second));
#                     auto &data = std::get<0>(tup);
#                     auto &trigger = std::get<1>(tup);
#
#                     std::copy(data.begin(), data.end(), ecg_waveform_data);
#                     ecg_waveform_data += data.size();
#
#                     for (auto i = 0; i < number_of_elements; i++) trigger_data[i] |= trigger[i];
#
#                 }
#
# //                ecg_waveform.head.sample_time_us = sample_time_us.at(PMU_Type::ECG1);
#                 waveforms.push_back(std::move(ecg_waveform));
#
#
#             }
#
#
#             for (auto key_val : pmu_map) {
#                 auto tup = unpack_pmu(std::get<0>(key_val.second));
#                 auto &data = std::get<0>(tup);
#                 auto &trigger = std::get<1>(tup);
#
#                 auto waveform = ISMRMRD::Waveform(data.size(), 2);
#                 waveform.head.waveform_id = waveformId.at(key_val.first) + 5 * learning_phase;
#                 std::copy(data.begin(), data.end(), waveform.data);
#
#                 std::copy(trigger.begin(), trigger.end(), waveform.data + data.size());
#
#                 # waveform.head.sample_time_us = sample_time_us.at(key_val.first)
#                 waveforms.push_back(std::move(waveform))
#             }
#             # Figure out number of ECG channels
#
#
#         for waveform in waveforms:
#             waveform['head']['time_stamp'] = timestamp
#             waveform['head']['measurement_uid'] = scanheader['lMeasUID']
#             waveform['head']['scan_counter'] = last_scan_counter
#             waveform['head']['sample_time_us'] = duration*100/waveform['head']['number_of_samples']
#
#         if waveforms:
#             makeWaveformHeader(header) # Add the header if needed
#
#         siemens_dat.seek(cur_pos)
#         siemens_dat.seek(len, os.CUR)
#         return waveforms
