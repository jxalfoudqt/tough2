
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D
 

# # ---Mass Balance---
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


# # ---SWCC---
rocktype_main='POMED'
capillarity_parameter=dat.capillarity['parameters']
capillarity_type=dat.capillarity['type']
if  capillarity_type==7:
    lamda=capillarity_parameter[0]
    liquid_residual_saturation=capillarity_parameter[1]
    P_zero=1./capillarity_parameter[2]	
    Pressure_max=capillarity_parameter[3]		
    saturated_liquid_saturation=capillarity_parameter[4]
    S_star=(liq_saturation-liquid_residual_saturation)/(saturated_liquid_saturation-liquid_residual_saturation)
    capillary_pressure_calculated_Pa=1*P_zero*(S_star**(-1/lamda)-1)**(1-lamda)



i=0
while i==0:#<lst.num_times:

    #---Vapor Diffusion balance---
    dz                                               = np.gradient(element_value)
    Standard_atmospheric_pressure_pa                 = 1.01325e5
    porosity_value                                   = dat.grid.rocktype[rocktype_main].porosity
    gravity_value                                    = dat.parameter['gravity']
    
    vapor_mass_fraction_in_gas_gradient              = np.gradient(vapor_mass_fraction_in_gas[:,i])/dz
    diffusion_coefficient                            = dat.diffusion[0][0]*(Standard_atmospheric_pressure_pa/(gas_pressure_pa[:,i]))*((temperature_degree[:,i]+T_kelven)/T_kelven)**dat.parameter['be']
    diffusion_calculation                            = -porosity_value**(4./3)*(gas_saturation[:,i])**(10./3)*gas_density_kgPm3[:,i]*diffusion_coefficient*vapor_mass_fraction_in_gas_gradient*np.insert(connection_area_m2,0,0)
    
    
    #---vapor_pressure---
    vapor_pressure_pa                                = gas_pressure_pa[:,i]-air_pressure_pa[:,i]
    relative_humidity_percent                        = np.exp(capillary_pressure_pa[:,i]*9.81*water_molecular_weight/R_value/(temperature_degree[:,i]+T_kelven))
    vapor_saturated_pressure_pa                      = 611*np.exp(17.27*(temperature_degree[:,i]+T_kelven-T_kelven)/(temperature_degree[:,i]+T_kelven-35.85))
    vapor_pressure_pa_calculated                     = vapor_saturated_pressure_pa*relative_humidity_percent
    
    
    #---vapor_density---
    vapor_density_kgPm3                              = gas_density_kgPm3[:,i]*vapor_mass_fraction_in_gas[:,i]
    vapor_density_kgPm3_calculated                   = vapor_saturated_pressure_pa*water_molecular_weight/(R_value*temperature_degree[:,i]+T_kelven)
    
    
    #---our own method---
    vapor_density_gradient_calculated                = np.gradient(vapor_density_kgPm3)/dz
    diffusion_coefficient_calculated                 = 2.29e-5*((temperature_degree[:,i]+T_kelven)/T_kelven)**dat.parameter['be']
    diffusion_calculation_calculated                 = porosity_value**(4./3)*(gas_saturation[:,i])**(10./3)*diffusion_coefficient_calculated*vapor_density_gradient_calculated*np.insert(connection_area_m2,0,0)
    
    vapor_density_gradient_chenming                  = np.gradient(vapor_density_kgPm3_calculated)/dz
    diffusion_coefficient_chenming                   = 2.29e-5*((temperature_degree[:,i]+T_kelven)/T_kelven)**dat.parameter['be']
    diffusion_calculation_chenming                   = porosity_value**(4./3)*(gas_saturation[:,i])**(10./3)*diffusion_coefficient_chenming*vapor_density_gradient_chenming*np.insert(connection_area_m2,0,0)

    
    fig=plt.figure()
    ax1=plt.subplot(241)
    ax1.plot(-vapor_diff_flow_kgPs[:,i],connection_value,'k-',diffusion_calculation[1:],connection_value,'b-')
    plt.xlabel('vapor_diff_flow (kgPs)')
    plt.ylabel('x (m)')
    plt.ylim(1.e2,-10)
    #ax1.set_yscale('log')
    #plt.xlim(0,10.e-5)
    #ax1.set_xscale('log')
    
    ax1=plt.subplot(242)
    ax1.plot(-vapor_diff_flow_kgPs[:,i],connection_value,'k-',diffusion_calculation_chenming[1:],connection_value,'r-',diffusion_calculation_calculated[1:],connection_value,'b-')
    plt.xlabel('vapor_diff_flow (kgPs)')
    plt.ylim(1.e2,-10)
    #ax1.set_yscale('log')
    # plt.xlim(np.nanmin(initial_porosity),np.nanmax(initial_porosity))
    ax1.set_xscale('log')
    
    ax1=plt.subplot(243)
    ax1.plot(vapor_pressure_pa_calculated/100000,element_value,'b-',vapor_pressure_pa/100000,element_value,'k-')
    plt.xlabel('vapor_pre (*10^5Pa)')
    plt.ylim(1.e2,-10)
    #ax1.set_yscale('log')
    plt.xlim(-0.2,2)
    # ax1.set_xscale('log')
    
    ax1=plt.subplot(244)
    ax1.plot(-capillary_pressure_pa[:,i]/10000000,element_value,'r-',capillary_pressure_calculated_Pa[:,i]/10000000,element_value,'k-')
    plt.xlabel('Cap. Pre. (*10^7Pa)')
    plt.ylim(1.e2,-10)
    #ax1.set_yscale('log')
    plt.xlim(-10,40)
    #ax1.set_xscale('log')
	
    ax1=plt.subplot(245)
    ax1.plot(vapor_density_kgPm3_calculated,element_value,'r-',vapor_density_kgPm3,element_value,'k-')
    plt.xlabel('Vap density (kgPm3)')
    plt.ylim(1.e2,-10)
    #ax1.set_yscale('log')
    plt.xlim(-0.1,1.2)
    # ax1.set_xscale('log')
	
    plt.rcParams.update({'font.size': 8})
    fig.tight_layout()
    plt.savefig('figure/diffusion_balance_check'+str(i+1)+'.png',dpi=300) 
    i+=1