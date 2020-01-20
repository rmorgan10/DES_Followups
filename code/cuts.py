# A class to contain all cuts

from astropy.cosmology import FlatLambdaCDM
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

np.random.seed(6)

cosmo = FlatLambdaCDM(H0=70, Om0=0.3, Tcmb0=2.725)

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

    def at_least_one_MLSCORE_90_detection(self, lc, md):
        photprobs = np.array(lc['PHOTPROB'].values, dtype=float)
        good_photprobs = photprobs[photprobs > 0.9]
        if len(good_photprobs) > 0:
            return True
        else:
            return False

    def at_least_one_snr_10_detection(self, lc, md):
        fluxes = np.array(lc['FLUXCAL'].values, dtype=float)
        fluxerrs = np.array(lc['FLUXCALERR'].values, dtype=float)
        snr = fluxes / fluxerrs
        good_snrs = snr[np.where(snr > 10.0)]
        if len(good_snrs) > 0:
            return True
        else:
            return False

    def at_least_one_snr_7_detection(self, lc, md):
        fluxes = np.array(lc['FLUXCAL'].values, dtype=float)
        fluxerrs = np.array(lc['FLUXCALERR'].values, dtype=float)
        photflags = np.array(lc['PHOTFLAG'].values, dtype=int)
        type_2_detection_fluxes = fluxes[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0))]
        type_2_detection_fluxerrs = fluxerrs[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0))]
        snr = type_2_detection_fluxes / type_2_detection_fluxerrs
        good_snrs = snr[np.where(snr > 7.0)]
        if len(good_snrs) > 0:
            return True
        else:
            return False

    def at_least_one_snr_5_detection(self, lc, md):
        fluxes = np.array(lc['FLUXCAL'].values, dtype=float)
        fluxerrs = np.array(lc['FLUXCALERR'].values, dtype=float)
        snr = fluxes / fluxerrs
        good_snrs = snr[np.where(snr > 5.0)]
        if len(good_snrs) > 0:
            return True
        else:
            return False

    def at_least_one_snr_3_detection(self, lc, md):
        fluxes = np.array(lc['FLUXCAL'].values, dtype=float)
        fluxerrs = np.array(lc['FLUXCALERR'].values, dtype=float)
        snr = fluxes / fluxerrs
        good_snrs = snr[np.where(snr > 3.0)]
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

    def fading_cut_one_band(self, lc, md):
        mjds = np.array(lc['MJD'].values, dtype=float)
        flts = np.array(lc['FLT'].values, dtype=str)
        mags = np.array(lc['MAG'].values, dtype=float)
        photflags = np.array(lc['PHOTFLAG'].values, dtype=int)
        good_flts = flts[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0))]
        good_mjds = mjds[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0))]
        good_mags = mags[np.where(((photflags & 4096) != 0) & ((photflags & 1016) == 0))]
        for flt in np.unique(good_flts):
            cut_mjds = good_mjds[good_flts == flt]
            cut_mags = good_mags[good_flts == flt]
            final_mags = cut_mags[cut_mjds > 58713.0]
            if len(final_mags) > 1:
                if final_mags[-1] - final_mags[0] < 0.0: return False
        return True

    
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
    def at_least_05_arcsec_from_DES_galaxy(self, lc, md):
        if int(md['FAKE']) == 2:
            #choice = np.random.uniform(low=0.0, high=1.0, size=1)[0]
            #if choice < 0.0517372:
            #    return False
            #else:
            #    return True
            
            #use physical sn host sep pdf to choose distance
            #from DES3YR SN sample, H0=70
            bins = [(0.000, 0.148), (0.148, 1.362), (1.362, 2.575), (2.575, 3.789), 
                    (3.789, 5.002), (5.002, 6.216), (6.216, 7.430), (7.430, 8.643), 
                    (8.643, 9.857), (9.857, 11.070), (11.070, 12.284), (12.284, 13.497), 
                    (13.497, 14.711), (14.711, 15.925), (15.925, 17.138), (17.138, 18.352), 
                    (18.352, 19.565), (19.565, 20.779), (20.779, 21.992), (21.992, 23.206), 
                    (23.206, 24.420), (24.420, 26.500)]
            bin_probs = np.array([0.129, 0.125, 0.116, 0.105, 0.092, 0.080, 0.067, 0.055, 0.044, 
                         0.034, 0.026, 0.020, 0.015, 0.012, 0.010, 0.009, 0.010, 0.011, 
                         0.012, 0.012, 0.011, 0.006])
            bin_probs = bin_probs / np.sum(bin_probs)

            chosen_bin_index = np.random.choice(np.arange(len(bins), dtype=int), size=1, p=bin_probs)[0]
            chosen_bin = bins[chosen_bin_index]
            kpc_sep = np.random.uniform(low=chosen_bin[0], high=chosen_bin[1], size=1)[0]

            arcsec_per_kpc = cosmo.arcsec_per_kpc_comoving(float(md['SIM_REDSHIFT_CMB']))
            ang_sep = arcsec_per_kpc.value * kpc_sep
            if ang_sep >= 0.5:
                return True
            else:
                return False

        #try using host matching instead of gold
        elif int(md['HOSTGAL_NMATCH']) > 0:
            if float(md['HOSTGAL_SNSEP']) < 0.5:
                return False
            else:
                return True
        else:
            return False #data with no host, shouldn't happen, but cut anyways
             
        #else:
        #    passing_snids = snid_lists.GW190814_1001_near_galaxy_center()
        #    if int(md['SNID']) in passing_snids:
        #        return True
        #    else:
        #        return False

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

    def separated_from_foreground(self, lc, md):
        # at least 0.5 arcsec from DES star or object (0.00109)

        # at least 20 arcmin from NGC253

        # at least 8 arcmin from NGC288

        # at least 3 arcmin from HD4398

        #total_area = 57.7949 #deg**2                                                                                                                
        #masked_area = ((20. / 60.)**2 + (8. / 60.)**2 + (3. / 60.)**2) * np.pi
        #masked_fraction = masked_area / total_area
        #(0.007142)

        if int(md['FAKE']) == 2:
            choice = np.random.uniform(low=0.0, high=1.0, size=1)[0]
            if choice < 0.00823:
                return False
            else:
                return True
        else:
            passing_snids = snid_lists.GW190814_1001_near_foreground()
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
            #pz_err_proxy = np.random.uniform(low=0.02, high=0.06, size=1)[0]
            
            means = [18.428, 18.694, 19.535, 19.889, 20.423, 20.962, 21.267, 21.631, 21.856]
            stds = [1.394, 1.534, 1.364, 1.234, 1.309, 1.129, 0.949, 0.911, 0.853]
            z_bins = np.linspace(0.0, 0.6, 10)
            bin_index = np.argmax(z_bins[z_bins < float(md['SIM_REDSHIFT_CMB'])])
            if bin_index >= len(means):
                bin_index = len(means) - 1
            mag = np.random.normal(loc=means[bin_index], scale=stds[bin_index], size=1)[0]

            x = [16.386, 17.161, 17.927, 18.693, 19.489, 20.273, 21.048, 21.793, 22.575]
            y = [0.015, 0.019, 0.02, 0.025, 0.018, 0.026, 0.031, 0.041, 0.06]
            func = interp1d(x, y)

            if mag > np.max(x): mag = np.max(x) - 0.1
            if mag < np.min(x): mag = np.min(x) + 0.1

            z_err_proxy = func(mag)

            pz_err = z_err_proxy * (1.0 + float(md['SIM_REDSHIFT_CMB']))

            pz = np.random.normal(loc=float(md['SIM_REDSHIFT_CMB']), scale=pz_err, size=1)[0]
            while pz <= 0:
                pz = np.random.normal(loc=float(md['SIM_REDSHIFT_CMB']), scale=pz_err, size=1)[0]

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

    def has_host_30_arcsec(self, lc, md):
         if int(md['FAKE']) == 2:
             bins = [(0.000, 0.148), (0.148, 1.362), (1.362, 2.575), (2.575, 3.789),
                            (3.789, 5.002), (5.002, 6.216), (6.216, 7.430), (7.430, 8.643),
                            (8.643, 9.857), (9.857, 11.070), (11.070, 12.284), (12.284, 13.497),
                            (13.497, 14.711), (14.711, 15.925), (15.925, 17.138), (17.138, 18.352),
                            (18.352, 19.565), (19.565, 20.779), (20.779, 21.992), (21.992, 23.206),
                            (23.206, 24.420), (24.420, 26.500)]
             bin_probs = np.array([0.129, 0.125, 0.116, 0.105, 0.092, 0.080, 0.067, 0.055, 0.044,
                                          0.034, 0.026, 0.020, 0.015, 0.012, 0.010, 0.009, 0.010, 0.011,
                                          0.012, 0.012, 0.011, 0.006])
             bin_probs = bin_probs / np.sum(bin_probs)

             chosen_bin_index = np.random.choice(np.arange(len(bins), dtype=int), size=1, p=bin_probs)[0]
             chosen_bin = bins[chosen_bin_index]
             kpc_sep = np.random.uniform(low=chosen_bin[0], high=chosen_bin[1], size=1)[0]

             kpc_per_arcsec_angular_diameter = cosmo.kpc_comoving_per_arcmin(float(md['SIM_REDSHIFT_CMB'])) / 60.0 / (1.0 + float(md['SIM_REDSHIFT_CMB']))
             arcsec_sep = kpc_sep / kpc_per_arcsec_angular_diameter.value
             if arcsec_sep < 30.0:
                 return True
             else:
                 return False

         else:
             if int(md['HOSTGAL_NMATCH']) > 0:
                 if float(md['HOSTGAL_SNSEP']) < 30.0:
                     return True
                 else:
                     return False
             else:
                 return False

    def realtime_vetting(self, lc, md):
        if int(md['FAKE']) == 2:
            return True
        else:
            bad_snids = snid_lists.GW19084_1001_not_artifact()
            if int(md['SNID']) in bad_snids:
                return False
            else:
                return True

    def realtime_vetting_strict(self, lc, md):
        if int(md['FAKE']) == 2:
            if int(md['SIM_MODEL_INDEX']) == 12:
                #all agn cut out by requirement of visible transient 
                return False
            else:
                #other simulated transient classes we would expect to be visible 
                ##unless they are in a galaxy with an AGN, so use the AGN rate to account for the confusion 
                choice = np.random.uniform(low=0.0, high=1.0, size=1)[0]
                if choice > 0.0016:
                    #if not AGN, cut only if we are seeing lmited 
                    bins = [(0.000, 0.148), (0.148, 1.362), (1.362, 2.575), (2.575, 3.789),
                            (3.789, 5.002), (5.002, 6.216), (6.216, 7.430), (7.430, 8.643),
                            (8.643, 9.857), (9.857, 11.070), (11.070, 12.284), (12.284, 13.497),
                            (13.497, 14.711), (14.711, 15.925), (15.925, 17.138), (17.138, 18.352),
                            (18.352, 19.565), (19.565, 20.779), (20.779, 21.992), (21.992, 23.206),
                            (23.206, 24.420), (24.420, 26.500)]
                    bin_probs = np.array([0.129, 0.125, 0.116, 0.105, 0.092, 0.080, 0.067, 0.055, 0.044,
                                          0.034, 0.026, 0.020, 0.015, 0.012, 0.010, 0.009, 0.010, 0.011,
                                          0.012, 0.012, 0.011, 0.006])
                    bin_probs = bin_probs / np.sum(bin_probs)

                    chosen_bin_index = np.random.choice(np.arange(len(bins), dtype=int), size=1, p=bin_probs)[0]
                    chosen_bin = bins[chosen_bin_index]
                    kpc_sep = np.random.uniform(low=chosen_bin[0], high=chosen_bin[1], size=1)[0]

                    kpc_per_arcsec_angular_diameter = cosmo.kpc_comoving_per_arcmin(float(md['SIM_REDSHIFT_CMB'])) / 60.0 / (1.0 + float(md['SIM_REDSHIFT_CMB']))
                    arcsec_sep = kpc_sep / kpc_per_arcsec_angular_diameter.value
                    
                    seeing_limit = np.min(np.array(lc['PSF_SIG1'].values, dtype=float)) / 4.0

                    if arcsec_sep > seeing_limit:
                        return True
                    else:
                        return False

                else:
                    #if AGN, automatically cut since we sill  just see a point source 
                    return False
        else:
            bad_snids = snid_lists.GW19084_1001_not_artifact_strict()
            if int(md['SNID']) in bad_snids:
                return False
            else:
                return True

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
                    #if not AGN, cut only if we are seeing lmited
                    bins = [(0.000, 0.148), (0.148, 1.362), (1.362, 2.575), (2.575, 3.789),
                            (3.789, 5.002), (5.002, 6.216), (6.216, 7.430), (7.430, 8.643),
                            (8.643, 9.857), (9.857, 11.070), (11.070, 12.284), (12.284, 13.497),
                            (13.497, 14.711), (14.711, 15.925), (15.925, 17.138), (17.138, 18.352),
                            (18.352, 19.565), (19.565, 20.779), (20.779, 21.992), (21.992, 23.206),
                            (23.206, 24.420), (24.420, 26.500)]
                    bin_probs = np.array([0.129, 0.125, 0.116, 0.105, 0.092, 0.080, 0.067, 0.055, 0.044,
                                          0.034, 0.026, 0.020, 0.015, 0.012, 0.010, 0.009, 0.010, 0.011,
                                          0.012, 0.012, 0.011, 0.006])
                    bin_probs = bin_probs / np.sum(bin_probs)

                    chosen_bin_index = np.random.choice(np.arange(len(bins), dtype=int), size=1, p=bin_probs)[0]
                    chosen_bin = bins[chosen_bin_index]
                    kpc_sep = np.random.uniform(low=chosen_bin[0], high=chosen_bin[1], size=1)[0]

                    kpc_per_arcsec_angular_diameter = cosmo.kpc_comoving_per_arcmin(float(md['SIM_REDSHIFT_CMB'])) / 60.0 / (1.0 + float(md['SIM_REDSHIFT_CMB']))
                    arcsec_sep = kpc_sep / kpc_per_arcsec_angular_diameter.value
                    #arcsec_per_kpc = cosmo.arcsec_per_kpc_comoving(float(md['SIM_REDSHIFT_CMB']))
                    #arcsec_sep = kpc_sep * arcsec_per_kpc.value
                    seeing_limit = np.min(np.array(lc['PSF_SIG1'].values, dtype=float)) / 4.0
                    
                    if arcsec_sep > seeing_limit:
                        return True
                    else:
                        return False

                else:
                    #if AGN, automatically cut since we sill  just see a point source
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


        
