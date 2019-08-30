# A module for quick calculations

from astropy.cosmology import z_at_value
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

def get_ligo_z_range(dist, sigma):

    #assume a cosmology
    cosmo = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)
    
    #calculate z range
    min_dist = (dist - sigma) * u.Mpc
    min_z = z_at_value(cosmo.luminosity_distance, min_dist)
    max_dist = (dist + sigma) * u.Mpc
    max_z = z_at_value(cosmo.luminosity_distance, max_dist)

    return round(min_z, 3), round(max_z, 3)


