
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D
 

# ---Mass Balance---
liquid_mass_element_kg                  = np.array([element_volume_m3*liq_density_kgPm3[2:,i]*liq_saturation[2,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
liquid_mass_kg                          = np.sum(liquid_mass_element_kg,axis=1) 
vapor_mass_element_kg                   = np.array([vapor_mass_fraction_in_gas[2:,i]*element_volume_m3*gas_density_kgPm3[2:,i]*gas_saturation[2:,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
vapor_mass_kg                           = np.sum(vapor_mass_element_kg,axis=1) 
liquid_flow_top2_kgPs                   = liquid_flow_kgPs[1]
vapor_flow_top2_kgPs                    = vapor_flow_kgPs[1]  
vapor_diff_flow_top2_kgPs               = vapor_diff_flow_kgPs[1]
total_water_mass_kg                     = liquid_mass_kg+vapor_mass_kg                                    
water_mass_change_over_time_kg          = np.diff(total_water_mass_kg)
total_water_net_flux_kgPs               = -liquid_flow_top2_kgPs-vapor_diff_flow_top2_kgPs-vapor_flow_top2_kgPs
water_amount_change_over_time_kg        = total_water_net_flux_kgPs[1:]*np.diff(lst.times)
print 'water_mass_change_over_time_kg='+str(np.sum(water_mass_change_over_time_kg))
print 'water_amount_change_over_time_kg='+str(np.sum(water_amount_change_over_time_kg))


print total_water_out_from_sink_mmPday  = -liquid_flow_top_mmPday-vapor_flow_top_mmPday-vapor_diff_flow_top_mmPday+liquid_flow_second_mmPday+vapor_flow_second_mmPday+vapor_diff_flow_second_mmPday
print water_generation_mmPday
