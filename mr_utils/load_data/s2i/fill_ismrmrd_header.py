'''fill_ismrmrd_header

This is currently not working and silently failing.
'''

import logging

def fill_ismrmrd_header(h, study_date, study_time):
    '''Add dates/times to ISMRMRD header.'''
    try:

        # ---------------------------------
        # fill more info into the ismrmrd header
        # ---------------------------------
        # study
        study_date_needed = False
        study_time_needed = False

        if h.studyInformation:
            if not h.studyInformation.studyDate:
                study_date_needed = True

            if not h.studyInformation.studyTime:
                study_time_needed = True

        else:
            study_date_needed = True
            study_time_needed = True


        if study_date_needed or study_time_needed:
            # ISMRMRD::StudyInformation study;
            # print(type(h))
            # print(dir(h))
            # How do we create a study and how do we add it to the header, h?


            if study_date_needed and study_date != '':
                # study.studyDate.set(study_date)
                # setattr(h.studyInformation.studyDate, study_date)
                logging.info('Study date: %s', study_date)

            if study_time_needed and study_time != '':
                # study.studyTime.set(study_time)
                # h.studyInformation.append(studyTime), study_time)
                logging.info('Study time: %s', study_time)


            # h.studyInformation.set(study)

        # ---------------------------------
        # go back to string
        # ---------------------------------

    except Exception as e:
        print(e)
        return False

    return h
