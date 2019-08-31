# A class to contain all cuts

import pandas as pd
import numpy as np

class CutList:
    def __init__(self):
        self.all_cuts = [x for x in dir(self) if x[0] != '_']
        
    def test_method(self):
        return True

    #define all cuts below such that they return true if pass and return false if fail



#cutlist = CutList()
#print cutlist.all_cuts
