from t2listing import *
import numpy as np
from t2data import *

print('Parsing output file\n')

liquid_density_kgPm3   = 1000
water_molecular_weight = 0.018
kpaPpa                 = 1.e-3
R_value                = 8.3145
mPmm                   = 1.e-3
dayPs                  = 1./(3600*24)
T_kelven=273.15


# #--- post-process the output ---------------------------
dat.title = 'NB_for_TDB'
lst       = t2listing(dat.title+'.listing')

# #read element and connection
connection_direction          = np.array([blk.direction for blk in dat.grid.connectionlist])
element_coordinate            = np.array([j.centre for j in dat.grid.blocklist])                                       
element_value_x               = element_coordinate[:,0]
element_value_y               = element_coordinate[:,1]
element_value_z               = element_coordinate[:,2]
  
# #read element column
#lst.element.column_name
#['P', 'T', 'SG', 'SL', 'XBRINE(LIQ)', 'XAIRG', 'XAIRL', 'PCAP', 'DG', 'DL', 'POROSITY', 'LOG(K)']
gas_pressure_pa               = np.array([lst.history(('e',lst.element.row_name[i],'P'))[1] for i in range(lst.element.num_rows)])
#temperature_degree            = np.array([lst.history(('e',lst.element.row_name[i],'T'))[1] for i in range(lst.element.num_rows)])
#gas_saturation                = np.array([lst.history(('e',lst.element.row_name[i],'SG'))[1] for i in range(lst.element.num_rows)])
#liq_saturation                = np.array([lst.history(('e',lst.element.row_name[i],'SL'))[1] for i in range(lst.element.num_rows)])
#brine_mass_fraction_in_liquid = np.array([lst.history(('e',lst.element.row_name[i],'XBRINE(LIQ)'))[1] for i in range(lst.element.num_rows)])
#capillary_pressure_pa         = np.array([lst.history(('e',lst.element.row_name[i],'PCAP'))[1] for i in range(lst.element.num_rows)])
#liq_density_kgPm3             = np.array([lst.history(('e',lst.element.row_name[i],'DL'))[1] for i in range(lst.element.num_rows)])
 
# #read connection column
#lst.connection.column_name
#['FLOH', 'FLOH/FLOF', 'FLOF', 'FLO(GAS)', 'VAPDIF', 'FLO(LIQ.)', 'VEL(GAS)', 'VEL(LIQ.)'] 
# liquid_flow_kgPs              = -1*np.array([lst.history(('c',lst.connection.row_name[i],'FLO(LIQ.)'))[1] for i in range(lst.connection.num_rows)])
# liquid_flow_mmPday            = liquid_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3/mPmm/dayPs
# liquid_flow_mmPday_x          = liquid_flow_mmPday[connection_direction==1]
# liquid_flow_mmPday_z          = liquid_flow_mmPday[connection_direction==3]

# #read generation column 
#lst.generation.column_name
#['GENERATION RATE', 'ENTHALPY', 'FF(GAS)', 'FF(LIQ.)', 'P(WB)']
water_generation_kgPs                 = np.array([lst.history(('g',i,'GENERATION RATE'))[1] for i in lst.generation.row_name])
#water_generation_mmPday               = water_generation_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3/mPmm/dayPs
#water_generation_vapor_mass_fraction  = np.array([lst.history(('g',i,'FF(GAS)' ))[1] for i in lst.generation.row_name])
#water_generation_liquid_mass_fraction = np.array([lst.history(('g',i,'FF(LIQ.)'))[1] for i in lst.generation.row_name])           # what is FF(LIQ) mean and how did it distribute to both?
#water_generation_vapor_kgPs           = water_generation_kgPs*water_generation_vapor_mass_fraction
#water_generation_liquid_kgPs          = water_generation_kgPs*water_generation_liquid_mass_fraction
