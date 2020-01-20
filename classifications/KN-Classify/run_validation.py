import os

os.system('python validate_conditions_classify.py GW190510_KNC fair seeing')
os.system('python validate_conditions_classify.py GW190510_KNC fair skymag')
os.system('python validate_conditions_classify.py GW190510_KNC fair deltat')

os.system('python validate_conditions_classify.py GW190510_KNC poor seeing')
os.system('python validate_conditions_classify.py GW190510_KNC poor skymag')
os.system('python validate_conditions_classify.py GW190510_KNC poor deltat')
