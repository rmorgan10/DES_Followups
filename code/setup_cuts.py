"""This script queries the DB for limiting mags and creates cut inputs."""

import glob
import sys

import pandas as pd

import psycopg2


# Get exposures to query
event_name = sys.argv[1]
exp_file = '../events/%s/exptable.txt' %event_name
exp_file_stream = open(exp_file, 'r')
exp_list = [x.strip() for x in exp_file_stream.readlines()]

# Connect to exposure DB
password = glob.glob(".*.password")[0].split('.')[1]
conn =  psycopg2.connect(
    database='decam_prd',
    user='decam_reader',
    host='des61.fnal.gov',
    password=password,
    port=5443) 

# Create data storage object. {band: {nite: lim mag}}
data = {}

# Query for all exposures
for expnum in exp_list:
    query = """
select 
    filter, 
    to_char(date::timestamp - interval '1 DAY' ,'YYYYMMDD') as nite,
    to_char(
        case 
            when filter='g' then 23.4 
            when filter='r' then 23.1 
            when filter='i' then 22.5 
            when filter='z' then 21.8 
            when filter='Y' then 20.3 
        end + 1.25*log(sum(qc_teff*exptime)/90.), '99.99') as depth
from exposure.exposure 
where id = {expnum}
group by 
    filter,
    date;
""".format(expnum=expnum)

    df = pd.read_sql(query, conn)
    band = str(df['filter'].values[0])
    nite = str(df['nite'].values[0])
    depth = float(df['depth'].values[0])
    
    if band in data:
        if nite in data[band]:
            if depth > data[band][nite]:
                data[band][nite] = depth
        else:
            data[band][nite] = depth
    else:
        data[band] = {nite: depth}

conn.close()

# Construct the cuts.py file within the event directory
cut_file_data = """
from astropy.time import Time

class CutList:
    def __init__(self):
        self.all_cuts = [x for x in dir(self) if x[0] != '_']
        return

    def detected_on_one_nite(self, lc, md):
        depth_dict = {data_repr}

        if 'FLT' in lc.columns:
            flt_col_name = 'FLT'
        else:
            flt_col_name = 'BAND'

        if 'NITE' not in lc.columns:
            nites = []
            mjds = lc['MJD'].values
            for mjd in mjds:
                mjd_time = Time(float(mjd), format='mjd')
                year, month, day = mjd_time.iso.split(' ')[0].split('-')
                nites.append('%s%s%s' %(year, month, day))
            lc['NITE'] = nites

        for (flt, nite), df in lc.groupby([flt_col_name, 'NITE']):
            if flt not in depth_dict:
                continue
            else:
                if nite not in depth_dict[flt]:
                    continue

            if df['MAG'].values.min() < depth_dict[flt][str(nite)]:
                return True
        return False

    def detected_on_two_nites(self, lc, md):
        depth_dict = {data_repr}

        if 'FLT' in lc.columns:
            flt_col_name = 'FLT'
        else:
            flt_col_name = 'BAND'

        if 'NITE' not in lc.columns:
            nites = []
            mjds = lc['MJD'].values
            for mjd in mjds:
                mjd_time = Time(float(mjd), format='mjd')
                year, month, day = mjd_time.iso.split(' ')[0].split('-')
                nites.append('%s%s%s' %(year, month, day))
            lc['NITE'] = nites

        detections = 0
        for (flt, nite), df in lc.groupby([flt_col_name, 'NITE']):
            if flt not in depth_dict:
                continue
            else:
                if nite not in depth_dict[flt]:
                    continue

            if df['MAG'].values.min() < depth_dict[flt][str(nite)]:
                detections += 1
            if detections == 2:
                return True
        return False
""".format(data_repr=data.__repr__())

cut_py_file = open("../events/%s/cuts.py" %event_name, 'w+')
cut_py_file.write(cut_file_data)
cut_py_file.close()

cut_file_csv_data = """NUMBER,NAME\n1,detected_on_one_nite\n2,detected_on_two_nites"""
cut_csv_file = open("../events/%s/cuts.csv" %event_name, 'w+')
cut_csv_file.write(cut_file_csv_data)
cut_csv_file.close()