
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D

dat.title = '1D_evaporation_eos4'
#--- run the model ------------------------------------

#os.system(" tough2 -to sam6_0.listing sam6 4")
os.system(' tough2 -to '+dat.title+'.listing '+dat.title+' 4')