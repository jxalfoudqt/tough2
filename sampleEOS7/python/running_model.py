from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D


#--- run the model ------------------------------------

os.system(" tough2 -to sam6_0.listing sam6 4")