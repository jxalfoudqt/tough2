
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D

liquid_density_kgPm3=1000
water_molecular_weight=0.018
kpaPpa=1.e-3
R_value=8.3145
mPmm=1.e-3
dayPs=1./(3600*24)
T_kelven=273.15

dat.title = '1D_evaporation_eos4'
# --- post-process the output ---------------------------
lst = t2listing(dat.title+'.listing')
dat = t2data(dat.title)

connection_first_distance               = np.array([blk.distance[0] for blk in dat.grid.connectionlist])
connection_second_distance              = np.array([blk.distance[1] for blk in dat.grid.connectionlist])
element_value                           = np.cumsum(np.insert(connection_first_distance+connection_second_distance,0,0))
connection_value                        = np.cumsum(connection_first_distance+np.insert(connection_second_distance[:-1], 0, 0)) 
                                        
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
liquid_flow_mmPday                      = liquid_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3/mPmm/dayPs
gas_flow_kgPs                           = -1*np.array([lst.history(('c',lst.connection.row_name[i],'FLO(GAS)'))[1] for i in range(lst.connection.num_rows)])
gas_flow_mmPday                         = gas_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3/mPmm/dayPs
vapor_diff_flow_kgPs                    = -1*np.array([lst.history(('c',lst.connection.row_name[i],'VAPDIF'))[1] for i in range(lst.connection.num_rows)])
vapor_diff_flow_mmPday                  = vapor_diff_flow_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3/mPmm/dayPs
  
# gas_advection_velocity_mPs              = -1*np.array([lst.history(('c',lst.connection.row_name[i],'VEL(GAS)'))[1] for i in range(lst.connection.num_rows)])
# gas_advection_velocity_kgPs             = gas_advection_velocity_mPs*gas_density_kgPm3[1:]*dat.grid.connectionlist[0].area*dat.grid.rocktype['SAND '].porosity
# gas_advection_velocity_mmPday           = gas_advection_velocity_mPs*dat.grid.rocktype['SAND '].porosity/mPmm/dayPs 
# liquid_advection_velocity_mPs           = -1*np.array([lst.history(('c',lst.connection.row_name[i],'VEL(LIQ.)'))[1] for i in range(lst.connection.num_rows)])
# liquid_advection_velocity_kgPs          = liquid_advection_velocity_mPs*liq_density_kgPm3[1:]*dat.grid.connectionlist[0].area*dat.grid.rocktype['SAND '].porosity
# liquid_advection_velocity_mmPday        = liquid_advection_velocity_mPs*dat.grid.rocktype['SAND '].porosity/mPmm/dayPs 
# vapor_advection_velocity_mmPday         = vapor_mass_fraction_in_gas[1:]*gas_advection_velocity_mmPday
# vapor_advection_velocity_kgPs           = vapor_mass_fraction_in_gas[1:]*gas_advection_velocity_kgPs
# vapor_adv_flow_top_mmPday               = vapor_advection_velocity_mmPday[0]       
# vapor_adv_flow_second_mmPday            = vapor_advection_velocity_mmPday[1]
 
vapor_flow_mmPday                       = vapor_mass_fraction_in_gas[1:]*gas_flow_mmPday
vapor_flow_kgPs                         = vapor_mass_fraction_in_gas[1:]*gas_flow_kgPs


liquid_flow_top_mmPday                  = liquid_flow_mmPday[0]
gas_flow_top_mmPday                     = gas_flow_mmPday[0]
vapor_flow_top_mmPday                   = vapor_flow_mmPday[0]
vapor_diff_flow_top_mmPday              = vapor_diff_flow_mmPday[0]

   
liquid_flow_second_mmPday               = liquid_flow_mmPday[1]
gas_flow_second_mmPday                  = gas_flow_mmPday[1]
vapor_flow_second_mmPday                = vapor_flow_mmPday[1]
vapor_diff_flow_second_mmPday           = vapor_diff_flow_mmPday[1]

water_flow_second_mmPday                =liquid_flow_second_mmPday+vapor_flow_second_mmPday+vapor_diff_flow_second_mmPday
total_water_flow_second_mm              =np.cumsum(water_flow_second_mmPday*np.insert(np.diff(lst.times),0,lst.times[0])*dayPs)
 
water_generation_kgPs                   = np.array([lst.history(('g',lst.generation.row_name[i],'GENERATION RATE'))[1] for i in range(lst.generation.num_rows)])
water_generation_mmPday                 = water_generation_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3/mPmm/dayPs
water_generation_vapor_mass_fraction    = np.array([lst.history(('g',lst.generation.row_name[i],'FF(GAS)'))[1] for i in range(lst.generation.num_rows)])
water_generation_liquid_mass_fraction   = np.array([lst.history(('g',lst.generation.row_name[i],'FF(LIQ.)'))[1] for i in range(lst.generation.num_rows)])
water_generation_vapor_mmPday           = water_generation_mmPday*water_generation_vapor_mass_fraction
water_generation_liquid_mmPday          = water_generation_mmPday*water_generation_liquid_mass_fraction

gas_relative_permeability               = np.array([lst.history(('p',lst.primary.row_name[i],'K(GAS)'))[1] for i in range(lst.primary.num_rows)])
liq_relative_permeability               = np.array([lst.history(('p',lst.primary.row_name[i],'K(LIQ.)'))[1] for i in range(lst.primary.num_rows)])

# GAS_H                                   = np.array([lst.history(('p',lst.primary.row_name[i],'H(GAS)'))[1] for i in range(lst.primary.num_rows)])
# Liq_H                                   = np.array([lst.history(('p',lst.primary.row_name[i],'H(LIQ.)'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_change              = np.array([lst.history(('p',lst.primary.row_name[i],'DX1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_change             = np.array([lst.history(('p',lst.primary.row_name[i],'DX2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_change              = np.array([lst.history(('p',lst.primary.row_name[i],'DX3'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_var                 = np.array([lst.history(('p',lst.primary.row_name[i],'X1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_var                = np.array([lst.history(('p',lst.primary.row_name[i],'X2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_var                 = np.array([lst.history(('p',lst.primary.row_name[i],'X3'))[1] for i in range(lst.primary.num_rows)])

