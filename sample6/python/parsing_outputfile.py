
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

connection_first_distance       = np.array([blk.distance[0] for blk in dat.grid.connectionlist])
connection_second_distance      = np.array([blk.distance[1] for blk in dat.grid.connectionlist])
element_value                   = np.cumsum(np.insert(connection_first_distance+connection_second_distance,0,0))
connection_value                = np.cumsum(connection_first_distance+np.insert(connection_second_distance[:-1], 0, 0)) 
                                
element_volume_m3               = np.array([blk.volume for blk in dat.grid.blocklist[1:-1]])
                                
Gas_Density_kgPm3               = np.array([lst.history(('e',lst.element.row_name[i],'DG'))[1] for i in range(lst.element.num_rows)])
Liq_Density_kgPm3               = np.array([lst.history(('e',lst.element.row_name[i],'DL'))[1] for i in range(lst.element.num_rows)])
Gas_saturation                  = np.array([lst.history(('e',lst.element.row_name[i],'SG'))[1] for i in range(lst.element.num_rows)])
Liq_saturation                  = np.array([lst.history(('e',lst.element.row_name[i],'SL'))[1] for i in range(lst.element.num_rows)])
Gas_Pressure_pa                 = np.array([lst.history(('e',lst.element.row_name[i],'P'))[1] for i in range(lst.element.num_rows)])
Air_Pressure_pa                 = np.array([lst.history(('e',lst.element.row_name[i],'PAIR'))[1] for i in range(lst.element.num_rows)])
Capillary_Pressure_pa           = np.array([lst.history(('e',lst.element.row_name[i],'PCAP'))[1] for i in range(lst.element.num_rows)])
Temperature_degree              = np.array([lst.history(('e',lst.element.row_name[i],'T'))[1] for i in range(lst.element.num_rows)])
Vapor_mass_fraction_in_gas      = 1-np.array([lst.history(('e',lst.element.row_name[i],'XAIRG'))[1] for i in range(lst.element.num_rows)])
                                
Liquid_flow_kgPs                = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(LIQ.)'))[1] for i in range(lst.connection.num_rows)])
Liquid_flow_mmPday              = Liquid_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3*m2mm*day2s
Gas_flow_kgPs                   = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(GAS)'))[1] for i in range(lst.connection.num_rows)])
Gas_flow_mmPday                 = Gas_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3*m2mm*day2s
Vapor_diff_flow_kgPs            = np.array([lst.history(('c',lst.connection.row_name[i],'VAPDIF'))[1] for i in range(lst.connection.num_rows)])
Vapor_diff_flow_mmPday          = Vapor_diff_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3*m2mm*day2s
                                
Vapor_flow_mmPday               = (Vapor_mass_fraction_in_gas[1:]+Vapor_mass_fraction_in_gas[:-1])/2*Gas_flow_mmPday
Vapor_flow_kgPs                 = (Vapor_mass_fraction_in_gas[1:]+Vapor_mass_fraction_in_gas[:-1])/2*Gas_flow_kgPs
Vapor_adv_flow_mmPday           = Vapor_flow_mmPday-Vapor_diff_flow_mmPday
Vapor_Pressure_pa               = Gas_Pressure_pa-Air_Pressure_pa

Liquid_flow_topsoil_mmPday      = Liquid_flow_mmPday[0]
Gas_flow_topsoil_mmPday         = Gas_flow_mmPday[0]
Vapor_flow_topsoil_mmPday       = Vapor_flow_mmPday[0]
Vapor_adv_flow_topsoil_mmPday   = Vapor_adv_flow_mmPday[0]
Vapor_diff_flow_topsoil_mmPday  = Vapor_diff_flow_mmPday[0]

Liquid_flow_bottom_kgPs         = Liquid_flow_kgPs[-1]
Vapor_flow_bottom_kgPs          = Vapor_flow_kgPs[-1]
Liquid_flow_top_kgPs            = Liquid_flow_kgPs[0]
Vapor_flow_top_kgPs             = Vapor_flow_kgPs[0]
                                
Gas_relative_permeability_      = np.array([lst.history(('p',lst.primary.row_name[i],'K(GAS)'))[1] for i in range(lst.primary.num_rows)])
Liq_relative_permeability       = np.array([lst.history(('p',lst.primary.row_name[i],'K(LIQ.)'))[1] for i in range(lst.primary.num_rows)])

# GAS_H                           = np.array([lst.history(('p',lst.primary.row_name[i],'H(GAS)'))[1] for i in range(lst.primary.num_rows)])
# Liq_H                           = np.array([lst.history(('p',lst.primary.row_name[i],'H(LIQ.)'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_change      = np.array([lst.history(('p',lst.primary.row_name[i],'DX1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_change     = np.array([lst.history(('p',lst.primary.row_name[i],'DX2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_change      = np.array([lst.history(('p',lst.primary.row_name[i],'DX3'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_var         = np.array([lst.history(('p',lst.primary.row_name[i],'X1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_var        = np.array([lst.history(('p',lst.primary.row_name[i],'X2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_var         = np.array([lst.history(('p',lst.primary.row_name[i],'X3'))[1] for i in range(lst.primary.num_rows)])
                             
Gas_mass_element                = np.array([element_volume_m3*Gas_Density_kgPm3[1:-1,i]*Gas_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
Gas_mass                        = np.sum(Gas_mass_element,axis=1) 
Liquid_mass_element             = np.array([element_volume_m3*Liq_Density_kgPm3[1:-1,i]*Liq_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
Liquid_mass                     = np.sum(Liquid_mass_element,axis=1) 
Vapor_mass_element              = np.array([Vapor_mass_fraction_in_gas[1:-1,i]*element_volume_m3*Gas_Density_kgPm3[1:-1,i]*Gas_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
Vapor_mass                      = np.sum(Vapor_mass_element,axis=1) 


Net_water_mass=np.diff(Liquid_mass+Vapor_mass)
Total_water_flux=(Liquid_flow_bottom_kgPs+Vapor_flow_bottom_kgPs-Liquid_flow_top_kgPs-Vapor_flow_top_kgPs)
Net_water_flux=Total_water_flux[1:]*np.diff(lst.times)
