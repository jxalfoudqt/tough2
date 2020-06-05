from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import time
from t2data import *
from mpl_toolkits.mplot3d import Axes3D

#--- run the model ------------------------------------

# delete exisiting input file
cwd=os.getcwd()
inp_path=os.path.join(os.getcwd(),inp.title)

t = time.time()
os.system(' tough2 -to '+inp.title[:4]+'.out '+inp.title+' 7')
#os.system(' itough2 -tough2 '+inp.title+'.listing '+inp.title+' 4')
#os.system('treactv2087_eos4_gf')
#os.system('tr2.087_eos4_lnx')
elapsed = time.time() - t
print('Simulation Elapsed: %s minutes' %(elapsed/60))