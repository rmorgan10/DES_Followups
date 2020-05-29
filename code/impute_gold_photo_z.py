# Query the Y3 Gold catalog at locations of host galaxies and overwrite the redshift info

import numpy as np
import sys

event_name = sys.argv[1]

d = np.load('../events/%s/sims_and_data/LightCurvesReal_PYTHON/LightCurvesReal.npy' %event_name).item()

