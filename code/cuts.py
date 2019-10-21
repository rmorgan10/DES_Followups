# A class to contain all cuts

import pandas as pd
import numpy as np

np.random.seed(6)

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

    def at_least_one_snr_5_detection(self, lc, md):
        fluxes = np.array(lc['FLUXCAL'].values, dtype=float)
        fluxerrs = np.array(lc['FLUXCALERR'].values, dtype=float)
        snr = fluxes / fluxerrs
        good_snrs = snr[np.where(snr > 5.0)]
        if len(good_snrs) > 0:
            return True
        else:
            return False


    def at_least_one_type_1_detection(self, lc, md):
        #Type 1: no errors and ml score > 0.7
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        photprobs = np.array([float(x) for x in lc['PHOTPROB'].values])
        if int(md['FAKE']) == 0: 
            good_photflags_no_errors = photflags[np.where(((photflags & 8192) != 0) & ((photflags & 1016) == 0))]
        else:
            #good_photflags_no_errors = photflags[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0) & (photprobs > 0.7))]
            good_photflags_no_errors = photflags[np.where(((photflags & 4096) != 0) & (photprobs > 0.7))] 

        if len(good_photflags_no_errors) > 0: 
            return True
        else: 
            return False

    def at_least_one_additional_detection_of_type_2_or_better(self, lc, md):
        #Type 2: no errors, but any ml score is allowed
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        marginal_photflags_no_errors = photflags[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0))]
        if len(marginal_photflags_no_errors) > 1:
            return True
        else:
            return False

    def at_least_one_hour_separation_between_detections(self, lc, md):
        photflags = np.array([int(x) for x in lc['PHOTFLAG'].values])
        photprobs = np.array(lc['PHOTPROB'], dtype=float)
        mjds = np.array([float(x) for x in lc['MJD'].values])
        if int(md['FAKE']) == 0:
            mjd_good = list(mjds[np.where(((photflags & 8192) != 0) & ((photflags & 1016) == 0))])
        else:
            mjd_good = list(mjds[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0) & (photprobs > 0.7))])
        
        mjd_marginal = list(mjds[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0))])

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

    ### GW190814_1001 RESULTS                        
    # star: 0.0043266 + 2.04622306123e-05 - 2.03116973886e-05  
    # galaxy: 0.0517372 + 6.94684156921e-05 - 6.9342809866e-05  
    # object: 0.013142 + 3.56627088227e-05 - 3.54864011889e-05    
    def at_least_2_arcsec_from_DES_galaxy(self, lc, md):
        if int(md['FAKE']) == 2:
            choice = np.random.uniform(low=0.0, high=1.0, size=1)[0]
            if choice < 0.0517372:
                return False
            else:
                return True
        else:
            passing_snids = snid_lists.GW190814_1001_DES_galaxy()
            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False

    def at_least_2_arcsec_from_DES_star(self, lc, md):
        if int(md['FAKE']) == 2:
            choice = np.random.uniform(low=0.0,high=1.0, size=1)[0]
            if choice < 0.0043266:
                return False
            else:
                return True
        else:
            passing_snids = snid_lists.GW190814_1001_DES_star()
            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False

    def at_least_2_arcsec_from_DES_object(self, lc, md):
        if int(md['FAKE']) == 2:
            choice = np.random.uniform(low=0.0, high=1.0, size=1)[0]
            if choice < 0.013142:
                return False
            else:
                return True
        else:
            passing_snids = snid_lists.GW190814_1001_DES_object()
            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False
            

    def away_from_known_bright_things(self, lc, md):
        if int(md['FAKE']) == 2:
            #total_area = 57.7949 #deg**2
            #masked_area = ((20. / 60.)**2 + (8. / 60.)**2 + (3. / 60.)**2) * np.pi
            #masked_fraction = masked_area / total_area
            choice = np.random.uniform(low=0.0, high=1.0, size=1)[0]
            if choice > 0.007142:
                return True
            else:
                return False
        else:
            passing_snids = snid_lists.GW190814_1001_near_bright_things()
            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False


    def at_least_1_detection_with_snr_7(self, lc, md):
        photflags = np.array(lc['PHOTFLAG'], dtype=int)
        fluxes = np.array(lc['FLUXCAL'], dtype=float)
        fluxerrs = np.array(lc['FLUXCALERR'], dtype=float)

        snr = fluxes / fluxerrs
        good_snr = snr[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0) & (snr > 7.0))]
        
        if len(good_snr) > 0:
            return True
        else:
            return False

        
    def GW190814_1001_bad_quality_missing_from_website(self, lc, md):
        if int(md['FAKE']) == 2:
            return True
        else:
            failing_snids = [635379, 689968, 690767, 692862, 695174, 696015]
            if int(md['SNID']) in failing_snids:
                return False
            else:
                return True

    def GW190814_1001_spec_confirmed_sn(self, lc, md):
        if int(md['FAKE']) == 2:
            model_index = int(md['SIM_MODEL_INDEX'])
            if model_index == 12 or model_index == 7:
                #allow agn and kn to pass
                return True
            else:
                #give SN a chance equal to our rate of passing
                num_confirmed = 4.0
                num_total = 27.0
                choice = np.random.uniform(low=0.0, high=num_total, size=1)[0]
                if choice < num_confirmed:
                    #confirmed SN
                    return False
                else:
                    #unconfirmed object, allow to pass
                    return True
        else:
            failing_snids = [661833, 627394, 614750, 624921]
            if int(md['SNID']) in failing_snids:
                return False
            else:
                return True

    def GW190814_1001_photo_z_inconsistent(self, lc, md):
        if int(md['FAKE']) == 2:
            #assume we have photo z since field was in DES footprint
            ##pz_err = np.random.uniform(low=0.02, high=float(md['SIM_REDSHIFT_CMB']) / 10.0 + 0.02, size=1)[0]
            ##pz_err = np.abs(float(md['SIM_REDSHIFT_CMB']) - 0.06) / np.abs(6.8 * float(md['SIM_REDSHIFT_CMB']) - 0.41)
            ##pz_err = np.abs(float(md['SIM_REDSHIFT_CMB']) - 0.06) / np.abs(12.5 * float(md['SIM_REDSHIFT_CMB']) - 3.25)    
            pz_err_proxy = np.random.uniform(low=0.02, high=0.06, size=1)[0]
            pz_err = pz_err_proxy * ( 1.0 + float(md['SIM_REDSHIFT_CMB']))
            pz = np.random.normal(loc=float(md['SIM_REDSHIFT_CMB']), scale=np.sqrt(pz_err), size=1)[0]
            if pz - pz_err < 0:
                pz = float(md['SIM_REDSHIFT_CMB']) + 0.005
                pz_err = 0.005
            
        else:
            pz = float(md['REDSHIFT_FINAL'])
            pz_err = float(md['REDSHIFT_FINAL_ERR'])
            if pz < 0.0 or pz > 2.0:
                #redshift info doesn't exist, allow to pass
                return True
            elif pz_err < 0.02 or pz_err > 2.0:
                #untrustworthy pz_err
                pz_err = 0.02
        
        #now that we have pz and pz_err, check that it is consistent with LIGO
        if np.abs(pz - 0.06) / np.sqrt(0.005**2 + pz_err**2) < 3.0:
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
                ##unless they are in a galaxy with an AGN, so use the AGN rate to account for the confusion
                choice = np.random.uniform(low=0.0, high=1.0, size=1)[0]
                if choice > 0.0016:
                    return True
                else:
                    return False
        else:
            #use the 448 list instead
            ##passing_snids = snid_lists.GW190814_1001_visual_inspection()
            passing_snids = snid_lists.GW190814_1001_visual_inspection()
            if int(md['SNID']) in passing_snids:
                return True
            else:
                return False

    def fading_by_more_than_3_sigma_day_6_through_16(self, lc, md):
        for flt in np.unique(lc['FLT'].values):
            flt_lc = lc[lc['FLT'] == flt]
            
            if flt_lc.shape[0] < 2:
                continue

            #only allow type 2 detections to be used as trustworthy flux measurements
            mjds = np.array([float(x) for x in flt_lc['MJD'].values])
            fluxes = np.array([float(x) for x in flt_lc['FLUXCAL'].values])
            fluxerrs = np.array([float(x) for x in flt_lc['FLUXCALERR'].values])
            photflags = np.array([int(x) for x in flt_lc['PHOTFLAG'].values])
            
            #Start of NITE 6: 58714.6
            mjd_6_16 = mjds[np.where((mjds > 58714.6) & (fluxes > 0.0) & (photflags > 4095))]
            flux_6_16 = fluxes[np.where((mjds > 58714.6) & (fluxes > 0.0) & (photflags > 4095))]
            fluxerr_6_16 = fluxerrs[np.where((mjds > 58714.6) & (fluxes > 0.0) & (photflags > 4095))]
            if len(mjd_6_16) < 2:
                continue
            
            mag_6_16 = 27.5 - 2.5 * np.log10(flux_6_16)
            mag_magerr_6_16 = 27.5 - 2.5 * np.log10(flux_6_16 + fluxerr_6_16)
            magerr_6_16 = np.abs(mag_magerr_6_16 - mag_6_16)

            #if (mag_6_16[-1] - mag_6_16[0]) / (mjd_6_16[-1] - mjd_6_16[0]) > -0.15:
            #    return False
            if (mag_6_16[0] - mag_6_16[-1]) / (magerr_6_16[0]**2 + magerr_6_16[-1]**2) > -3:
                #fading by less than 3 sigma --maybe lessen to 2
                return False

        return True

        
    def not_in_gaia_1_arcsec_GW190814_1001(self, lc, md):
        if int(md['FAKE']) != 0:
            return True
        else:
            good_snids = snid_lists.not_in_gaia_1_arcsec_GW190814_1001_snids()
            if int(md['SNID']) in good_snids:
                return True
            else:
                return False


