from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D
 
  
element_volume_m3                 = np.array([blk.volume for blk in dat.grid.blocklist[1:]])
# ---Mass Balance---
liquid_mass_element_kg            = np.array([element_volume_m3[1:]*liq_density_xt_mtx_kgPm3[2:,i]*liq_saturation_xt_mtx[2:,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
liquid_mass_kg                    = np.sum(liquid_mass_element_kg,axis=1) 
vapor_mass_element_kg             = np.array([vapor_mass_fraction_in_gas_xt_mtx[2:,i]*element_volume_m3[1:]*gas_density_xt_mtx_kgPm3[2:,i]*gas_saturation_xt_mtx[2:,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
vapor_mass_kg                     = np.sum(vapor_mass_element_kg,axis=1) 
total_water_mass_kg               = liquid_mass_kg+vapor_mass_kg                                    
water_mass_change_over_time_kg    = np.diff(total_water_mass_kg)

liquid_flow_top1_kgPs             = liquid_flow_xt_mtx_kgPs[1]
vapor_flow_top1_kgPs              = vapor_adv_xt_mtx_kgPs[1]  
vapor_diff_flow_top1_kgPs         = vapor_diff_flow_xt_mtx_kgPs[1]
total_water_net_flux_kgPs         = -liquid_flow_top1_kgPs-vapor_diff_flow_top1_kgPs-vapor_flow_top1_kgPs
water_amount_change_over_time_kg  = total_water_net_flux_kgPs[1:]*np.diff(lst.times)
print('water_mass_change_over_time_kg='+str(np.sum(water_mass_change_over_time_kg)))
print('water_amount_change_over_time_kg='+str(np.sum(water_amount_change_over_time_kg)))