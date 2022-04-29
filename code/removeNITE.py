import re
import os
import sys
import glob
from dateutil import rrule
from datetime import datetime
from shutil import copyfile

event_name = sys.argv[1]

start_date = '20000101'
end_date = '20301231'

dates = [date.strftime('%Y%m%d') for date in rrule.rrule(rrule.DAILY, dtstart=datetime.strptime(start_date, '%Y%m%d'),until=datetime.strptime(end_date, '%Y%m%d'))]

obs_str = '^OBS: .'
varlist_str = '^VARLIST: .'

obs_regex = re.compile(obs_str)
varlist_regex = re.compile(varlist_str)

print("../events/%s/sims_and_data/LightCurvesReal/" %event_name)

datFiles = glob.glob("../events/%s/sims_and_data/LightCurvesReal/*.dat" %event_name)
#datFiles = glob.glob("./des_real*.dat")

for datFile in datFiles:

    bottomlines = []
    bottomline_start_index = 10000

    f = open("temp.dat", 'w')
    f1 = open(datFile, 'r')
    lines = f1.readlines()
    f1.close()
    for line in lines:
        if line[:8] != 'VARLIST:' and lines.index(line) < bottomline_start_index:
            f.write(line)
        elif line[:8] != 'VARLIST:' and lines.index(line) > bottomline_start_index:
            bottomlines.append(line)
        else:
            bottomline_start_index = lines.index(line)
            bottomlines.append(line)
    for bottomline in bottomlines:
        if bottomline[:8] != 'VARLIST:' and bottomline[:4] !='OBS:':
            f.write(bottomline)
            continue
        bline = bottomline.split(' ')
        var_and_space = []
        full_element = ''
        for element in bline:
            if element != '':
                if full_element != '':
                    var_and_space.append(full_element)
                full_element = element+' '
            else:
                full_element += ' '
        for i in var_and_space:
            if i[:4] == "NITE":
                var_and_space.remove(i)
                break
            if i.strip() in dates:
                var_and_space.remove(i)
                break
        bline_str = ''
        for e in var_and_space:
            bline_str += e
        bline_str += '\n'
        f.write(bline_str)
    f.close()
    os.system('mv temp.dat %s' %datFile)
