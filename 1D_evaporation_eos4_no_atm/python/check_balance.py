
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D
                                       
# liquid_mass_element_kg                  = np.array([element_volume_m3*liq_density_kgPm3[1:-1,i]*liq_saturation[1:-1,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
# liquid_mass_kg                          = np.sum(liquid_mass_element_kg,axis=1) 
# vapor_mass_element_kg                   = np.array([vapor_mass_fraction_in_gas[1:-1,i]*element_volume_m3*gas_density_kgPm3[1:-1,i]*gas_saturation[1:-1,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
# vapor_mass_kg                           = np.sum(vapor_mass_element_kg,axis=1) 
# liquid_flow_bottom_kgPs                 = liquid_flow_kgPs[-1]
# vapor_flow_bottom_kgPs                  = vapor_flow_kgPs[-1]
# liquid_flow_top_kgPs                    = liquid_flow_kgPs[1]
# vapor_flow_top_kgPs                     = vapor_flow_kgPs[1]                                    
# total_water_mass_kg                     = liquid_mass_kg+vapor_mass_kg                                    
# water_mass_change_over_time_kg          = np.diff(total_water_mass_kg)
# total_water_net_flux_kgPs               = liquid_flow_bottom_kgPs+vapor_flow_bottom_kgPs-liquid_flow_top_kgPs-vapor_flow_top_kgPs
# water_amount_change_over_time_kg        = total_water_net_flux_kgPs[1:]*np.diff(lst.times)
# print 'water_mass_change_over_time_kg='+str(np.sum(water_mass_change_over_time_kg))
# print 'water_amount_change_over_time_kg='+str(np.sum(water_amount_change_over_time_kg))

dz                                               = 1./50
Standard_atmospheric_pressure_pa                 = 1.01325e5
porosity                                         = 0.45
# re-production of models
vapor_mass_fraction_in_gas_gradient              = np.gradient(vapor_mass_fraction_in_gas,axis=0)/dz
diffusion_coefficient                            = 2.13e-5*(Standard_atmospheric_pressure_pa/(gas_pressure_pa))*((temperature_degree+T_kelven)/T_kelven)**1.8
diffusion_calculation                            = -porosity**(4./3)*(gas_saturation)**(10./3)*gas_density_kgPm3*diffusion_coefficient*vapor_mass_fraction_in_gas_gradient*dat.grid.connectionlist[0].area
diffusion_calculation_relative_error             = np.abs((diffusion_calculation[1:]+vapor_diff_flow_kgPs)/vapor_diff_flow_kgPs)


#
vapor_pressure_pa                                = gas_pressure_pa-air_pressure_pa
vapor_density_kgPm3                              = gas_density_kgPm3*vapor_mass_fraction_in_gas

# our own method
relative_humidity_percent                        = np.exp(capillary_pressure_pa*9.81*water_molecular_weight/R_value/(temperature_degree+T_kelven))
vapor_saturated_pressure_pa                      = 611*np.exp(17.27*(temperature_degree+T_kelven-T_kelven)/(temperature_degree+T_kelven-35.85))
vapor_pressure_pa_calculated                     = vapor_saturated_pressure_pa*relative_humidity_percent
vapor_density_kgPm3_calculated                   = vapor_pressure_pa_calculated*water_molecular_weight/(R_value*temperature_degree)
vapor_density_gradient_chenming                  = np.gradient(vapor_density_kgPm3_calculated,axis=0)/dz
diffusion_coefficient_chenming                   = 2.29e-5*((temperature_degree+T_kelven)/T_kelven)**1.8
diffusion_calculation_chenming                   = porosity**(4./3)*(gas_saturation)**(10./3)*gas_density_kgPm3*diffusion_coefficient_chenming*vapor_density_gradient_chenming*dat.grid.connectionlist[0].area
diffusion_calculation_relative_error_chenming    = np.abs((diffusion_calculation_chenming[1:]+vapor_diff_flow_kgPs)/vapor_diff_flow_kgPs)

i=9
fig=plt.figure()
ax1=plt.subplot(141)
ax1.plot(diffusion_calculation[1:,i],connection_value,'b-',-vapor_diff_flow_kgPs[:,i],connection_value,'k-')
plt.xlabel('vapor_diff_flow (kgPs)')
plt.ylabel('x (m)')
plt.ylim(1.1,-0.1)
# plt.xlim(np.nanmin(initial_porosity),np.nanmax(initial_porosity))
ax1.set_xscale('log')

ax1=plt.subplot(142)
ax1.plot(-vapor_diff_flow_kgPs[:,i],connection_value,'k-',diffusion_calculation_chenming[1:,i],connection_value,'r-')
plt.xlabel('vapor_diff_flow (kgPs)')
#plt.ylabel('x (m)')
plt.ylim(1.1,-0.1)
# plt.xlim(np.nanmin(initial_porosity),np.nanmax(initial_porosity))
ax1.set_xscale('log')

ax1=plt.subplot(143)
ax1.plot(vapor_pressure_pa_calculated[:,i],element_value,'r-',vapor_pressure_pa[:,i],element_value,'k-')
plt.xlabel('vapor_pre (Pa)')
#plt.ylabel('x (m)')
plt.ylim(1.1,-0.1)
# plt.xlim(np.nanmin(initial_porosity),np.nanmax(initial_porosity))
#ax1.set_xscale('log')

ax1=plt.subplot(144)
ax1.plot(vapor_density_kgPm3_calculated[:,i],element_value,'r-',vapor_density_kgPm3[:,i],element_value,'k-')
plt.xlabel('vapor_density (kgPm3)')
#plt.ylabel('x (m)')
plt.ylim(1.1,-0.1)
# plt.xlim(np.nanmin(initial_porosity),np.nanmax(initial_porosity))
#ax1.set_xscale('log')
plt.rcParams.update({'font.size': 8})
fig.tight_layout()
plt.savefig('figure/diffusion_balance_check.png',dpi=300) 