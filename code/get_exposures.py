# A modeule to extract the pointings for a set of follow-up observations from the database

#import easyaccess as ea
import glob
import psycopg2

import numpy as np
import pandas as pd
import sys

event_name = sys.argv[1]
propid = sys.argv[2]
first_exposure = sys.argv[3]
last_exposure = sys.argv[4]

query = """SELECT id as EXPNUM,
       TO_CHAR(date - '12 hours'::INTERVAL, 'YYYYMMDD') AS NITE,
       EXTRACT(EPOCH FROM date - '1858-11-17T00:00:00Z')/(24*60*60) AS MJD_OBS,
       ra AS RADEG,
       declination AS DECDEG,
       filter AS BAND,
       exptime AS EXPTIME,
       propid AS PROPID,
       flavor AS OBSTYPE,
       qc_teff as TEFF,
       object as OBJECT 
FROM exposure.exposure 
WHERE flavor='object' and exptime>29.999 and RA is not NULL and propid = '%s' and id between %s and %s
ORDER BY id""" % (propid, first_exposure, last_exposure)

#get password
password = glob.glob(".*.password")[0].split('.')[1]

conn =  psycopg2.connect(database='decam_prd',
                           user='decam_reader',
                           host='des61.fnal.gov',
                           password=password,
                           port=5443) 
some_exposures = pd.read_sql(query, conn)
conn.close()

some_exposures['EXPNUM'].to_csv('../events/%s/exptable_full.txt' %event_name, index=False)

