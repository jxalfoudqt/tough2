from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D

liquid_density_kgPm3=1000
water_molecular_weight=0.018
r_value=8.314
m2mm=1000
day2s=3600*24
t_kelven=273.15
pa2kpa=1000

# --- post-process the output ---------------------------
lst = t2listing('sam6_0.listing')
dat = t2data('sam6')

connection_first_distance           = np.array([blk.distance[0] for blk in dat.grid.connectionlist])
connection_second_distance          = np.array([blk.distance[1] for blk in dat.grid.connectionlist])
element_value                       = np.cumsum(np.insert(connection_first_distance+connection_second_distance,0,0))
connection_value                    = np.cumsum(connection_first_distance+np.insert(connection_second_distance[:-1], 0, 0)) 
                                    
element_volume_m3                   = np.array([blk.volume for blk in dat.grid.blocklist[1:-1]])
                                    
gas_density_kgPm3                   = np.array([lst.history(('e',lst.element.row_name[i],'DG'))[1] for i in range(lst.element.num_rows)])
liq_density_kgPm3                   = np.array([lst.history(('e',lst.element.row_name[i],'DL'))[1] for i in range(lst.element.num_rows)])
gas_saturation                      = np.array([lst.history(('e',lst.element.row_name[i],'SG'))[1] for i in range(lst.element.num_rows)])
liq_saturation                      = np.array([lst.history(('e',lst.element.row_name[i],'SL'))[1] for i in range(lst.element.num_rows)])
gas_pressure_pa                     = np.array([lst.history(('e',lst.element.row_name[i],'P'))[1] for i in range(lst.element.num_rows)])
air_pressure_pa                     = np.array([lst.history(('e',lst.element.row_name[i],'PAIR'))[1] for i in range(lst.element.num_rows)])
capillary_pressure_pa               = np.array([lst.history(('e',lst.element.row_name[i],'PCAP'))[1] for i in range(lst.element.num_rows)])
temperature_degree                  = np.array([lst.history(('e',lst.element.row_name[i],'T'))[1] for i in range(lst.element.num_rows)])
vapor_mass_fraction_in_gas          = 1-np.array([lst.history(('e',lst.element.row_name[i],'XAIRG'))[1] for i in range(lst.element.num_rows)])
                                    
liquid_flow_kgPs                    = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(LIQ.)'))[1] for i in range(lst.connection.num_rows)])
liquid_flow_mmPday                  = liquid_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3*m2mm*day2s
gas_flow_kgPs                       = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(GAS)'))[1] for i in range(lst.connection.num_rows)])
gas_flow_mmPday                     = gas_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3*m2mm*day2s
vapor_diff_flow_kgPs                = np.array([lst.history(('c',lst.connection.row_name[i],'VAPDIF'))[1] for i in range(lst.connection.num_rows)])
vapor_diff_flow_mmPday              = vapor_diff_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3*m2mm*day2s
                                    
vapor_flow_mmPday                   = (vapor_mass_fraction_in_gas[1:]+vapor_mass_fraction_in_gas[:-1])/2*gas_flow_mmPday
vapor_flow_kgPs                     = (vapor_mass_fraction_in_gas[1:]+vapor_mass_fraction_in_gas[:-1])/2*gas_flow_kgPs
vapor_adv_flow_mmPday               = vapor_flow_mmPday-vapor_diff_flow_mmPday
vapor_Pressure_pa                   = gas_pressure_pa-air_pressure_pa
                                    
liquid_flow_top_mmPday              = liquid_flow_mmPday[0]
gas_flow_top_mmPday                 = gas_flow_mmPday[0]
vapor_flow_top_mmPday               = vapor_flow_mmPday[0]
vapor_adv_flow_top_mmPday           = vapor_adv_flow_mmPday[0]
vapor_diff_flow_top_mmPday          = vapor_diff_flow_mmPday[0]
                                    
gas_relative_permeability           = np.array([lst.history(('p',lst.primary.row_name[i],'K(GAS)'))[1] for i in range(lst.primary.num_rows)])
liq_relative_permeability           = np.array([lst.history(('p',lst.primary.row_name[i],'K(LIQ.)'))[1] for i in range(lst.primary.num_rows)])
                                    
# GAS_H                               = np.array([lst.history(('p',lst.primary.row_name[i],'H(GAS)'))[1] for i in range(lst.primary.num_rows)])
# Liq_H                               = np.array([lst.history(('p',lst.primary.row_name[i],'H(LIQ.)'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_change          = np.array([lst.history(('p',lst.primary.row_name[i],'DX1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_change         = np.array([lst.history(('p',lst.primary.row_name[i],'DX2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_change          = np.array([lst.history(('p',lst.primary.row_name[i],'DX3'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_var             = np.array([lst.history(('p',lst.primary.row_name[i],'X1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_var            = np.array([lst.history(('p',lst.primary.row_name[i],'X2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_var             = np.array([lst.history(('p',lst.primary.row_name[i],'X3'))[1] for i in range(lst.primary.num_rows)])
                                    
liquid_mass_element_kg              = np.array([element_volume_m3*liq_density_kgPm3[1:-1,i]*liq_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
liquid_mass_kg                      = np.sum(liquid_mass_element_kg,axis=1) 
vapor_mass_element_kg               = np.array([vapor_mass_fraction_in_gas[1:-1,i]*element_volume_m3*gas_density_kgPm3[1:-1,i]*gas_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
vapor_mass_kg                       = np.sum(vapor_mass_element_kg,axis=1) 
liquid_flow_bottom_kgPs             = liquid_flow_kgPs[-1]
vapor_flow_bottom_kgPs              = vapor_flow_kgPs[-1]
liquid_flow_top_kgPs                = liquid_flow_kgPs[0]
vapor_flow_top_kgPs                 = vapor_flow_kgPs[0]                                    
total_water_mass_kg                 = liquid_mass_kg+vapor_mass_kg                                    
water_mass_change_over_time_kg      = np.diff(total_water_mass_kg)
total_water_net_flux_kgPs           = liquid_flow_bottom_kgPs+vapor_flow_bottom_kgPs-liquid_flow_top_kgPs-vapor_flow_top_kgPs
water_amount_change_over_time_kg    = total_water_net_flux_kgPs[1:]*np.diff(lst.times)