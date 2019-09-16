# A class to contain all cuts

import pandas as pd
import numpy as np

#for testing
from random import randint

#snid_lists
import snid_lists

class CutList:
    def __init__(self):
        self.all_cuts = [x for x in dir(self) if x[0] != '_']
        return

    #Example cuts
    def test_method(self, lc, md):
        if randint(0, 10) >= 5:
            return True
        else:
            return False

    def test_method1(self, lc, md):
        if randint(0, 10) >= 3:
            return True
        else:
            return False

    def test_method2(self, lc, md):
        return True

    #define all cuts below such that they return true if pass and return false if fail
    #define all cuts with both lc and md arguments even if they are unused

    def at_least_one_type_1_detection(self, lc, md):
        #Type 1: no errors and ml score > 0.7
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        photprobs = np.array([float(x) for x in lc['PHOTPROB'].values])
        #good_photflags_no_errors = photflags[np.where((photflags & 8192) & (photflags & ~1016))]
        #good_photflags_no_errors = photflags[np.where((photflags & 4096) & (photflags & ~1016) & (photprobs > 0.7))]
        good_photflags_no_errors = photflags[np.where((photflags > 4095) & (photprobs > 0.7))]
        if len(good_photflags_no_errors) > 0: 
            return True
        else: 
            return False

    def at_least_one_additional_detection_of_type_2_or_better(self, lc, md):
        #Type 2: no errors, but any ml score is allowed
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        marginal_photflags_no_errors = photflags[np.where((photflags & 4096) & (photflags & ~1016))]
        if len(marginal_photflags_no_errors) > 1:
            return True
        else:
            return False

    def at_least_one_hour_separation_between_detections(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        mjds = np.array([float(x) for x in lc['MJD'].values])
        mjd_good = list(mjds[np.where((photflags & 8192) & (photflags & ~1016))])
        mjd_marginal = list(mjds[np.where((photflags & 4096) & (photflags & ~1016))])

        two_type_1_detections_separated_by_an_hour = np.max(mjd_good) - np.min(mjd_good) > 0.042
        mixed_mjds = mjd_good + mjd_marginal
        one_detection_of_each_type_separated_by_an_hour = np.max(mixed_mjds) - np.min(mixed_mjds) > 0.042

        if two_type_1_detections_separated_by_an_hour or one_detection_of_each_type_separated_by_an_hour:
            return True
        else:
            return False

    def at_least_five_type_2_or_type_1_detections_with_ml_above_08(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        photprobs = np.array([float(x) for x in lc['PHOTPROB'].values])
        marg_photprobs = photprobs[np.where((photflags & 4096) & (photflags & ~1016))]
        #if len(marg_photprobs[np.where(marg_photprobs > 0.8)]) > 4:
        if len(marg_photprobs) > 4:
            return True
        else:
            return False

    def at_least_four_type_2_or_type_1_detections_with_ml_above_08(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        photprobs = np.array([float(x) for x in lc['PHOTPROB'].values])
        marg_photprobs = photprobs[np.where((photflags & 4096) & (photflags & ~1016))]
        #marg_photprobs = photprobs[np.where(photflags > 4095)]
        if len(marg_photprobs[np.where(marg_photprobs > 0.8)]) > 3:
            return True
        else:
            return False

    def first_epoch_has_a_type_1_detection(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        #good_photflags_no_errors = photflags[np.where((photflags & 8192) & (photflags & ~1016))]
        mjds = lc['MJD'].values
        min_mjd = round(np.min(mjds), 0)
        good_mjds = mjds[np.where((photflags & 8192) & (photflags & ~1016))]
        rounded_good_mjds = [round(x, 0) for x in good_mjds]
        if min_mjd in rounded_good_mjds:
            return True
        else:
            return False

    def at_least_two_type_2_detections(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        marginal_photflags_no_errors = photflags[np.where((photflags & 4096) & (photflags & ~1016))]
        if len(marginal_photflags_no_errors) > 1:
            return True
        else:
            return False

    def at_least_five_type_2_or_better_detections(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        marginal_photflags_no_errors = photflags[np.where((photflags & 4096) & (photflags & ~1016))]
        if len(marginal_photflags_no_errors) > 4:
            return True
        else:
            return False

    #super strict
    def all_detections_are_type_1(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        good_photflags = photflags[np.where((photflags & 8192) & (photflags & ~1016))]
        if len(photflags) == len(good_photflags):
            return True
        else:
            return False

    def all_detections_have_ml_above_07(self, lc, md):
        photprobs = np.array([float(x) for x in lc['PHOTPROB'].values])
        good_photprobs = photprobs[np.where(photprobs > 0.7)]
        if len(photprobs) == len(good_photprobs):
            return True
        else:
            return False

    def at_least_two_detections_with_photflag_12288(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        good_photflags = photflags[np.where((photflags > 12287) & (photflags < 12289))]
        if len(good_photflags) > 1:
            return True
        else:
            return False

    def at_least_two_type_1_detections(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        good_photflags = photflags[np.where((photflags & 8192) & (photflags & ~1016))]
        if len(good_photflags) > 1:
            return True
        else:
            return False

    def at_least_one_detection_with_snr_above_10(self, lc, md):
        snr = lc['FLUXCAL'].values / lc['FLUXCALERR'].values
        if np.max(snr) > 10.0:
            return True
        else:
            return False


    def detected_on_at_least_two_nights(self, lc, md):
        mjds = lc['MJD'].values
        rounded_mjds = [round(x, 0) for x in mjds]
        if len(np.unique(rounded_mjds)) > 1:
            return True
        else:
            return False

    def flux_changes_by_at_least_factor_of_1_point_2(self, lc, md):
        if np.max(lc['FLUXCAL'].values) / np.min(lc['FLUXCAL'].values) > 1.2:
            return True
        else:
            return False

    #consistent with ligo dist
    
    #decreaseing flux 
    def decreases_in_flux_by_at_least_two_sigma(self, lc, md):
        pass


    def no_bad_subtractions_in_stamps(self, lc, md):
        if int(md['FAKE']) == 2:
            #automatic pass for sims
            return True
        else:

            passing_snids = []


            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False

    def no_pre_existing_stellar_object_in_stamps(self, lc, md):
        if int(md['FAKE']) == 2:
            #automatic pass for sims 
            return True
        else:

            passing_snids = []


            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False



    def visual_inspection_GW190814_1001(self, lc, md):
        if int(md['FAKE']) == 2:
            if int(md['SIM_MODEL_INDEX']) == 12:
                #all agn cut out by requirement of visible transient
                return False
            else:
                #other simulated transient classes we would expect to be visible
                return True
        else:
            passing_snids = snid_lists.GW190814_1001_visual_inspection()
            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False

    def fading_by_more_than_015_mag_per_day_6_through_16(self, lc, md):
        for flt in np.unique(lc['FLT'].values):
            flt_lc = lc[lc['FLT'] == flt]
            
            if flt_lc.shape[0] < 2:
                continue

            #only allow type 2 detections to be used as trustworthy flux measurements
            mjds = np.array([float(x) for x in flt_lc['MJD'].values])
            fluxes = np.array([float(x) for x in flt_lc['FLUXCAL'].values])
            photflags = np.array([int(x) for x in flt_lc['PHOTFLAG'].values])
            
            #Start of NITE 6: 58714.6
            mjd_6_16 = mjds[np.where((mjds > 58714.6) & (fluxes > 0.0) & (photflags > 4095))]
            flux_6_16 = fluxes[np.where((mjds > 58714.6) & (fluxes > 0.0) & (photflags > 4095))]
            if len(mjd_6_16) < 2:
                continue
            
            mag_6_16 = 27.5 - 2.5 * np.log10(flux_6_16)

            if (mag_6_16[-1] - mag_6_16[0]) / (mjd_6_16[-1] - mjd_6_16[0]) > -0.15:
                return False

        return True

        
