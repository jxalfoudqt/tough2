
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from t2incons import *
from mpl_toolkits.mplot3d import Axes3D

liquid_density_kgPm3=1000
water_molecular_weight=0.018
kpaPpa=1.e-3
R_value=8.3145
mPmm=1.e-3
dayPs=1./(3600*24)
T_kelven=273.15

dat       = t2data()
dat.title = 'rhpdiff'
# --- post-process the output ---------------------------
lst = t2listing(dat.title+'.listing')
dat = t2data(dat.title)

element_number                                                                                                                          = dat.meshmaker[0][1][1][1]['nequ']+dat.meshmaker[0][1][2][1]['nlog']+dat.meshmaker[0][1][3][1]['nlog']+dat.meshmaker[0][1][4][1]['nequ']
element_value                                                                                                                           = np.empty(element_number)
element_value[:]                                                                                                                        = np.nan
element_value[0]                                                                                                                        = np.array(dat.meshmaker[0][1][0][1]['radii'])
element_value[np.arange(1,2+dat.meshmaker[0][1][2][1]['nlog'],1)]                                                                       = np.linspace(dat.meshmaker[0][1][1][1]['dr'],dat.meshmaker[0][1][2][1]['rlog'],dat.meshmaker[0][1][2][1]['nlog']+1)
element_value[np.arange(dat.meshmaker[0][1][2][1]['nlog']+1,2+dat.meshmaker[0][1][3][1]['nlog']+dat.meshmaker[0][1][2][1]['nlog'],1)]   = np.linspace(dat.meshmaker[0][1][2][1]['rlog'],dat.meshmaker[0][1][3][1]['rlog'],dat.meshmaker[0][1][3][1]['nlog']+1)
connection_value                        = (element_value[:-1]+element_value[1:])/2

connection_area_m2                      = np.pi*connection_value*2*np.array(dat.meshmaker[0][1][5][1]['layer'])
connection_area_m2_alltimes             = np.empty((len(connection_area_m2),lst.num_times))
connection_area_m2_alltimes[:,0]        = connection_area_m2
connection_area_m2_alltimes[:,1]        = connection_area_m2
connection_area_m2_alltimes[:,2]        = connection_area_m2
      
	  
gas_density_kgPm3                       = np.array([lst.history(('e',lst.element.row_name[i],'DG'))[1] for i in range(lst.element.num_rows)])
liq_density_kgPm3                       = np.array([lst.history(('e',lst.element.row_name[i],'DL'))[1] for i in range(lst.element.num_rows)])
gas_saturation                          = np.array([lst.history(('e',lst.element.row_name[i],'SG'))[1] for i in range(lst.element.num_rows)])
liq_saturation                          = np.array([lst.history(('e',lst.element.row_name[i],'SL'))[1] for i in range(lst.element.num_rows)])
gas_pressure_pa                         = np.array([lst.history(('e',lst.element.row_name[i],'P'))[1] for i in range(lst.element.num_rows)])
air_pressure_pa                         = np.array([lst.history(('e',lst.element.row_name[i],'PAIR'))[1] for i in range(lst.element.num_rows)])
capillary_pressure_pa                   = np.array([lst.history(('e',lst.element.row_name[i],'PCAP'))[1] for i in range(lst.element.num_rows)])
temperature_degree                      = np.array([lst.history(('e',lst.element.row_name[i],'T'))[1] for i in range(lst.element.num_rows)])
vapor_mass_fraction_in_gas              = 1-np.array([lst.history(('e',lst.element.row_name[i],'XAIRG'))[1] for i in range(lst.element.num_rows)])
                                        
liquid_flow_kgPs                        = -1*np.array([lst.history(('c',lst.connection.row_name[i],'FLO(LIQ.)'))[1] for i in range(lst.connection.num_rows)])
liquid_flow_mmPday                      = liquid_flow_kgPs/connection_area_m2_alltimes/liquid_density_kgPm3/mPmm/dayPs
gas_flow_kgPs                           = -1*np.array([lst.history(('c',lst.connection.row_name[i],'FLO(GAS)'))[1] for i in range(lst.connection.num_rows)])
gas_flow_mmPday                         = gas_flow_kgPs/connection_area_m2_alltimes/liquid_density_kgPm3/mPmm/dayPs
vapor_diff_flow_kgPs                    = -1*np.array([lst.history(('c',lst.connection.row_name[i],'VAPDIF'))[1] for i in range(lst.connection.num_rows)])
vapor_diff_flow_mmPday                  = vapor_diff_flow_kgPs/connection_area_m2_alltimes/liquid_density_kgPm3/mPmm/dayPs