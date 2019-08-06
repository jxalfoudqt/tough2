
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
water_molecular_weight=0.018
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
                                        
element_volume_m3                       = np.array([blk.volume for blk in dat.grid.blocklist[1:-1]])
                                        
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
                                        
water_generation_kgPs                   = np.array([lst.history(('g',lst.generation.row_name[i],'GENERATION RATE'))[1] for i in range(lst.generation.num_rows)])
water_generation_mmPday                 = water_generation_kgPs/dat.grid.connectionlist[0].area/liquid_density_kgPm3/mPmm/dayPs
water_generation_vapor_mass_fraction    = np.array([lst.history(('g',lst.generation.row_name[i],'FF(GAS)'))[1] for i in range(lst.generation.num_rows)])
water_generation_liquid_mass_fraction   = np.array([lst.history(('g',lst.generation.row_name[i],'FF(LIQ.)'))[1] for i in range(lst.generation.num_rows)])
water_generation_vapor_mmPday           = water_generation_mmPday*water_generation_vapor_mass_fraction
water_generation_liquid_mmPday          = water_generation_mmPday*water_generation_liquid_mass_fraction
                                        
vapor_flow_mmPday                       = vapor_mass_fraction_in_gas[1:]*gas_flow_mmPday
vapor_flow_kgPs                         = vapor_mass_fraction_in_gas[1:]*gas_flow_kgPs
vapor_adv_flow_mmPday                   = vapor_flow_mmPday-vapor_diff_flow_mmPday
                                        
liquid_flow_top_mmPday                  = liquid_flow_mmPday[0]
gas_flow_top_mmPday                     = gas_flow_mmPday[0]
vapor_flow_top_mmPday                   = vapor_flow_mmPday[0]
vapor_adv_flow_top_mmPday               = vapor_adv_flow_mmPday[0]
vapor_diff_flow_top_mmPday              = vapor_diff_flow_mmPday[0]
                                        
liquid_flow_second_mmPday               = liquid_flow_mmPday[1]
gas_flow_second_mmPday                  = gas_flow_mmPday[1]
vapor_flow_second_mmPday                = vapor_flow_mmPday[1]
vapor_adv_flow_second_mmPday            = vapor_adv_flow_mmPday[1]
vapor_diff_flow_second_mmPday           = vapor_diff_flow_mmPday[1]
                                        
#gas_relative_permeability               = np.array([lst.history(('p',lst.primary.row_name[i],'K(GAS)'))[1] for i in range(lst.primary.num_rows)])
#liq_relative_permeability               = np.array([lst.history(('p',lst.primary.row_name[i],'K(LIQ.)'))[1] for i in range(lst.primary.num_rows)])
                                        
# GAS_H                                   = np.array([lst.history(('p',lst.primary.row_name[i],'H(GAS)'))[1] for i in range(lst.primary.num_rows)])
# Liq_H                                   = np.array([lst.history(('p',lst.primary.row_name[i],'H(LIQ.)'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_change              = np.array([lst.history(('p',lst.primary.row_name[i],'DX1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_change             = np.array([lst.history(('p',lst.primary.row_name[i],'DX2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_change              = np.array([lst.history(('p',lst.primary.row_name[i],'DX3'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_var                 = np.array([lst.history(('p',lst.primary.row_name[i],'X1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_var                = np.array([lst.history(('p',lst.primary.row_name[i],'X2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_var                 = np.array([lst.history(('p',lst.primary.row_name[i],'X3'))[1] for i in range(lst.primary.num_rows)])
                                        
liquid_mass_element_kg                  = np.array([element_volume_m3*liq_density_kgPm3[1:-1,i]*liq_saturation[1:-1,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
liquid_mass_kg                          = np.sum(liquid_mass_element_kg,axis=1) 
vapor_mass_element_kg                   = np.array([vapor_mass_fraction_in_gas[1:-1,i]*element_volume_m3*gas_density_kgPm3[1:-1,i]*gas_saturation[1:-1,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
vapor_mass_kg                           = np.sum(vapor_mass_element_kg,axis=1) 
liquid_flow_bottom_kgPs                 = liquid_flow_kgPs[-1]
vapor_flow_bottom_kgPs                  = vapor_flow_kgPs[-1]
liquid_flow_top_kgPs                    = liquid_flow_kgPs[1]
vapor_flow_top_kgPs                     = vapor_flow_kgPs[1]                                    
total_water_mass_kg                     = liquid_mass_kg+vapor_mass_kg                                    
water_mass_change_over_time_kg          = np.diff(total_water_mass_kg)
total_water_net_flux_kgPs               = liquid_flow_bottom_kgPs+vapor_flow_bottom_kgPs-liquid_flow_top_kgPs-vapor_flow_top_kgPs
water_amount_change_over_time_kg        = total_water_net_flux_kgPs[1:]*np.diff(lst.times)
print 'water_mass_change_over_time_kg='+str(np.sum(water_mass_change_over_time_kg))
print 'water_amount_change_over_time_kg='+str(np.sum(water_amount_change_over_time_kg))

vapor_mass_fraction_in_gas_gradient     = np.gradient(vapor_mass_fraction_in_gas[:,10],axis=0)/(1./50)
diffusion_coefficient                   = 2.13e-5*(1.01325e5/(gas_pressure_pa[:,10]))*((temperature_degree[:,10]+273.15)/273.15)**1.8
diffusion_calculation                   = -0.45**(10./3)*(gas_saturation[:,10])**(10./3)*gas_density_kgPm3[:,10]*diffusion_coefficient*vapor_mass_fraction_in_gas_gradient
diffusion_calculation_relative_error    = np.abs((diffusion_calculation[1:]+vapor_diff_flow_kgPs[:,10])/vapor_diff_flow_kgPs[:,10])


vapor_pressure_pa                                = gas_pressure_pa-air_pressure_pa
vapor_density_kgPm3                              = gas_density_kgPm3*vapor_mass_fraction_in_gas
relative_humidity_percent                        = np.exp(capillary_pressure_pa*9.81*water_molecular_weight/R_value/(temperature_degree+T_kelven))
vapor_saturated_pressure_pa                      = 611*np.exp(17.27*(temperature_degree+T_kelven-T_kelven)/(temperature_degree+T_kelven-35.85))
vapor_pressure_pa_calculated                     = vapor_saturated_pressure_pa*relative_humidity_percent
vapor_density_kgPm3_calculated                   = vapor_pressure_pa_calculated*water_molecular_weight/(R_value*temperature_degree)
vapor_mass_fraction_in_gas_gradient_chenming     = np.gradient(vapor_pressure_pa_calculated,axis=0)/(1./50)
diffusion_coefficient_chenming                   = 2.29e-5*((temperature_degree+273.15)/273.15)**1.75
diffusion_calculation_chenming                   = diffusion_coefficient_chenming*(1-0.45*liq_saturation)*(1-0.45*liq_saturation)**(7./3)*vapor_mass_fraction_in_gas_gradient_chenming
diffusion_calculation_relative_error_chenming    = np.abs((diffusion_calculation_chenming[1:]+vapor_diff_flow_kgPs)/vapor_diff_flow_kgPs)