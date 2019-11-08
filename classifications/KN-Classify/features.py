# A class to code all feature extraction functions

import numpy as np
import pandas as pd

class FeatureExtractor():
    def __init__(self):
        self.features = [x for x in dir(self) if x[0:2] != '__']
        self.families = ['nobs_brighter_than',
                         'slope',
                         'same_nite_color_diff',
                         'total_color_diff',
                         'snr',
                         'flat',
                         'half',
                         'mag']
        self.feat_families = {fam: [x for x in self.features if x.find(fam) != -1] for fam in self.families}
        self.single_features = [x for x in self.features if x.find('color') == -1]
        self.double_features = [x for x in self.features if x.find('color') != -1]

        return

    """
    nobs brighter than
    """

    def nobs_brighter_than_20(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 1000.0 #10 ** ((27.5 - 20.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values[lc['FLT'].values == flt1], dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_21(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 398.107 #10 ** ((27.5 - 21.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values[lc['FLT'].values == flt1], dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_215(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 251.189 #10 ** ((27.5 - 21.5) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values[lc['FLT'].values == flt1], dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_22(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 158.489 #10 ** ((27.5 - 22.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values[lc['FLT'].values == flt1], dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_225(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 100.0 #10 ** ((27.5 - 22.5) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values[lc['FLT'].values == flt1], dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_23(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 63.096 #10 ** ((27.5 - 23.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values[lc['FLT'].values == flt1], dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_20_any_flt(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 1000.0 #10 ** ((27.5 - 20.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values, dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_21_any_flt(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 398.107 #10 ** ((27.5 - 21.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values, dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_215_any_flt(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 251.189 #10 ** ((27.5 - 21.5) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values, dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_22_any_flt(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 158.489 #10 ** ((27.5 - 22.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values, dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_225_any_flt(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 100.0 #10 ** ((27.5 - 22.5) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values, dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    def nobs_brighter_than_23_any_flt(self, lc, md, flt1, flt2=None):
        fluxcal_cut = 63.096 #10 ** ((27.5 - 23.0) / 2.5)
        fluxcals = np.array(lc['FLUXCAL'].values, dtype=float)
        if len(fluxcals) > 0:
            return len(fluxcals[fluxcals > fluxcal_cut])
        else:
            return 'N'

    """
    slope
    """

    def slope_average(self, lc, md, flt1, flt2=None):
        mags = np.array(lc[lc['FLT'] == flt1]['MAG'].values, dtype=float)
        mjds = np.array(lc[lc['FLT'] == flt1]['MJD'].values, dtype=float)
        if len(mags) > 1:
            return (mags[-1] - mags[0]) / (mjds[-1] - mjds[0]) 
        else:
            return 'N'
            
    def slope_max(self, lc, md, flt1, flt2=None):
        mags = np.array(lc[lc['FLT'] == flt1]['MAG'].values, dtype=float)
        mjds = np.array(lc[lc['FLT'] == flt1]['MJD'].values, dtype=float)
        if len(mags) > 1:
            return np.max(np.diff(mags) / np.diff(mjds))
        else:
            return 'N'

    def slope_min(self, lc, md, flt1, flt2=None):
        mags = np.array(lc[lc['FLT'] == flt1]['MAG'].values, dtype=float)
        mjds = np.array(lc[lc['FLT'] == flt1]['MJD'].values, dtype=float)
        if len(mags) > 1:
            return np.min(np.diff(mags) / np.diff(mjds))
        else:
            return 'N'

    def slope_mjd_of_max(self, lc, md, flt1, flt2=None):
        mags = np.array(lc[lc['FLT'] == flt1]['MAG'].values, dtype=float)
        mjds = np.array(lc[lc['FLT'] == flt1]['MJD'].values, dtype=float)
        if len(mags) > 1:
            return mjds[np.argmax(np.diff(mags) / np.diff(mjds))]
        else:
            return 'N'

    def slope_mjd_of_min(self, lc, md, flt1, flt2=None):
        mags = np.array(lc[lc['FLT'] == flt1]['MAG'].values, dtype=float)
        mjds = np.array(lc[lc['FLT'] == flt1]['MJD'].values, dtype=float)
        if len(mags) > 1:
            return mjds[np.argmin(np.diff(mags) / np.diff(mjds))]
        else:
            return 'N'

    """
    same nite color difference
    """
    def same_nite_color_diff_max(self, lc, md, flt1, flt2):
        #likely needs to be sped up
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) < 2:
            return 'N'
        lc['NITE'] = [int(round(x)) for x in np.array(lc['MJD'].values, dtype=float)]
        colors = []
        for nite in np.unique(lc['NITE'].values):
            try: 
                color = np.max(lc['MAG'].values[(lc['NITE'].values == nite) & (lc['FLT'].values == flt1)] - lc['MAG'].values[(lc['NITE'].values == nite) & (lc['FLT'].values == flt2)])
                colors.append(color)
            except:
                pass
        if len(colors) > 0:
            return np.max(colors)
        else:
            return 'N'
    
    def same_nite_color_diff_min(self, lc, md, flt1, flt2):
        #likely needs to be sped up
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) < 2:
            return 'N'
        lc['NITE'] = [int(round(x)) for x in np.array(lc['MJD'].values, dtype=float)]
        colors = []
        for nite in np.unique(lc['NITE'].values):
            try: 
                color = np.min(lc['MAG'].values[(lc['NITE'].values == nite) & (lc['FLT'].values == flt1)] - lc['MAG'].values[(lc['NITE'].values == nite) & (lc['FLT'].values == flt2)])
                colors.append(color)
            except:
                pass
        if len(colors) > 0:
            return np.min(colors)
        else:
            return 'N'

    def same_nite_color_diff_average(self, lc, md, flt1, flt2):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) < 2:
            return 'N'
        #likely needs to be sped up
        lc['NITE'] = [int(round(x)) for x in np.array(lc['MJD'].values, dtype=float)]
        colors = []
        for nite in np.unique(lc['NITE'].values):
            try: 
                color = np.max(lc['MAG'].values[(lc['NITE'].values == nite) & (lc['FLT'].values == flt1)] - lc['MAG'].values[(lc['NITE'].values == nite) & (lc['FLT'].values == flt2)])
                colors.append(color)
            except:
                pass
        if len(colors) > 0:
            return np.mean(colors)
        else:
            return 'N'

    """
    total color differences
    """
    def total_color_diff_max_max(self, lc, md, flt1, flt2):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) > 0 and len(lc['MAG'].values[lc['FLT'].values == flt2]) > 0:
            return np.max(lc['MAG'].values[lc['FLT'].values == flt1]) - np.max(lc['MAG'].values[lc['FLT'].values == flt2])
        else:
            return 'N'

    def total_color_diff_max_min(self, lc, md, flt1, flt2):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) > 0 and len(lc['MAG'].values[lc['FLT'].values == flt2]) > 0:
            return np.max(lc['MAG'].values[lc['FLT'].values == flt1]) - np.min(lc['MAG'].values[lc['FLT'].values == flt2])
        else:
            return 'N'

    def total_color_diff_min_max(self, lc, md, flt1, flt2):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) > 0 and len(lc['MAG'].values[lc['FLT'].values == flt2]) > 0:
            return np.min(lc['MAG'].values[lc['FLT'].values == flt1]) - np.max(lc['MAG'].values[lc['FLT'].values == flt2])
        else:
            return 'N'

    def total_color_diff_min_min(self, lc, md, flt1, flt2):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) > 0 and len(lc['MAG'].values[lc['FLT'].values == flt2]) > 0:
            return np.min(lc['MAG'].values[lc['FLT'].values == flt1]) - np.min(lc['MAG'].values[lc['FLT'].values == flt2])
        else:
            return 'N'

    def total_color_diff_mean_mean(self, lc, md, flt1, flt2):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) > 0 and len(lc['MAG'].values[lc['FLT'].values == flt2]) > 0:
            return np.mean(lc['MAG'].values[lc['FLT'].values == flt1]) - np.mean(lc['MAG'].values[lc['FLT'].values == flt2])
        else:
            return 'N'


    """
    snr
    """
    def snr_max(self, lc, md, flt1, flt2=None):
        if len(lc['FLUXCAL'].values[lc['FLT'].values == flt1]) > 0:
            return np.max(np.array(lc['FLUXCAL'].values, dtype=float)[lc['FLT'].values == flt1] / np.array(lc['FLUXCALERR'].values, dtype=float)[lc['FLT'].values == flt1])
        else:
            return 'N'

    def snr_mean(self, lc, md, flt1, flt2=None):
        if len(lc['FLUXCAL'].values[lc['FLT'].values == flt1]) > 0:
            return np.mean(np.array(lc['FLUXCAL'].values, dtype=float)[lc['FLT'].values == flt1] / np.array(lc['FLUXCALERR'].values, dtype=float)[lc['FLT'].values == flt1])
        else:
            return 'N'

    def snr_mjd_of_max(self, lc, md, flt1, flt2=None):
        if len(lc['FLUXCAL'].values[lc['FLT'].values == flt1]) > 0:
            snrs = np.array(lc['FLUXCAL'].values, dtype=float)[lc['FLT'].values == flt1] / np.array(lc['FLUXCALERR'].values, dtype=float)[lc['FLT'].values == flt1]
            return lc['MJD'].values[np.argmax(snrs)]
        else:
            return 'N'

    """
    flat line fitting
    """
    def flat_reduced_chi2(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 3:
            return 'N'
        magerrs = lc['MAGERR'].values[lc['FLT'].values == flt1]
        av = np.mean(mags)

        chi2 = np.sum((mags - av) ** 2 / magerrs ** 2)
        dof = len(mags) - 1
        return chi2 / dof

    def flat_reduced_chi2_weighted(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 3:
            return 'N'
        magerrs= lc['MAGERR'].values[lc['FLT'].values == flt1]
        weighted_av = np.sum(mags / magerrs**2) / np.sum(1 / magerrs**2)

        chi2 = np.sum((mags - weighted_av) ** 2 / magerrs ** 2)
        dof = len(mags) - 1
        return chi2 / dof

    def flat_nobs_3_sigma_from_line(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 3:
            return 'N'
        magerrs= lc['MAGERR'].values[lc['FLT'].values == flt1]
        av = np.mean(mags)
        return len(mags[np.abs((mags - av) / magerrs) > 3])

    def flat_nobs_3_sigma_from_line_weighted(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 3:
            return 'N'
        magerrs= lc['MAGERR'].values[lc['FLT'].values == flt1]
        weighted_av = np.sum(mags / magerrs**2) / np.sum(1 / magerrs**2)
        return len(mags[np.abs((mags - weighted_av) / magerrs) > 3])

    def flat_nobs_2_sigma_from_line(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 3:
            return 'N'
        magerrs = lc['MAGERR'].values[lc['FLT'].values == flt1]
        av = np.mean(mags)
        return len(mags[np.abs((mags - av) / magerrs) > 2])

    def flat_nobs_2_sigma_from_line_weighted(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 3:
            return 'N'
        magerrs= lc['MAGERR'].values[lc['FLT'].values == flt1]
        weighted_av = np.sum(mags / magerrs**2) / np.sum(1 / magerrs**2)
        return len(mags[np.abs((mags - weighted_av) / magerrs) > 2])

    """
    half light curve mags
    """

    def half_first_average_mag(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 6:
            return 'N'
        split = (np.max(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1]) - np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])) / 2 + np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])
        return np.mean(lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values <= split)])

    def half_second_average_mag(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 6:
            return 'N'
        split = (np.max(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1]) - np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])) / 2 + np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])
        return np.mean(lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values >= split)])

    def half_first_average_mag_weighted(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 6:
            return 'N'
        split = (np.max(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1]) - np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])) / 2 + np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])
        mags = lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values <= split)]
        magerrs = lc['MAGERR'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values <= split)]
        return np.sum(mags / magerrs**2) / np.sum(1 / magerrs**2)

    def half_second_average_mag_weighted(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 6:
            return 'N'
        split = (np.max(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1]) - np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])) / 2 + np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])
        mags = lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values >= split)]
        magerrs= lc['MAGERR'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values >= split)]
        return np.sum(mags / magerrs**2) / np.sum(1 / magerrs**2)

    def half_split_average_mag_difference(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 6:
            return 'N'
        split = (np.max(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1]) - np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])) / 2 + np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])
        right_mags = lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values >= split)]
        left_mags = lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values <= split)]
        return np.mean(left_mags) - np.mean(right_mags)

    def half_split_average_mag_difference_weighted(self, lc, md, flt1, flt2=None):
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        if len(mags) < 6:
            return 'N'
        split = (np.max(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1]) - np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])) / 2 + np.min(np.array(lc['MJD'].values, dtype=float)[lc['FLT'].values == flt1])
        right_mags = lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values >= split)]
        right_magerrs= lc['MAGERR'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values >= split)]
        left_mags = lc['MAG'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values <= split)]
        left_magerrs = lc['MAGERR'].values[(lc['FLT'].values == flt1) & (lc['MJD'].values <= split)]
        right_weighted_average = np.sum(right_mags / right_magerrs**2) / np.sum(1 / right_magerrs**2)
        left_weighted_average = np.sum(left_mags / left_magerrs**2) / np.sum(1 / left_magerrs**2)
        return np.mean(left_mags) - np.mean(right_mags)

    """
    full light curve mags
    """

    def mag_average(self, lc, md, flt1, flt2=None):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) < 1:
            return 'N'
        return np.mean(lc['MAG'].values[lc['FLT'].values == flt1])

    def mag_average_weighted(self, lc, md, flt1, flt2=None):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) < 1:
            return 'N'
        mags = lc['MAG'].values[lc['FLT'].values == flt1]
        magerrs= lc['MAGERR'].values[lc['FLT'].values == flt1]
        return np.sum(mags / magerrs**2) / np.sum(1 / magerrs**2)

    def mag_brightest(self, lc, md, flt1, flt2=None):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) < 1:
            return 'N'
        return np.min(np.array(lc[lc['FLT'] == flt1]['MAG'].values, dtype=float))

    def mag_total_change(self, lc, md, flt1, flt2=None):
        if len(lc['MAG'].values[lc['FLT'].values == flt1]) < 2:
            return 'N'
        return lc['MAG'].values[lc['FLT'].values == flt1][0] - lc['MAG'].values[lc['FLT'].values == flt1][-1]
