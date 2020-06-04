from t2listing import *
import numpy as np
from t2data import *


print('Parsing output file\n')
title = 'flow.out'
# #--- post-process the output ---------------------------
lst = t2listing(title)
dat = t2data('flow.inp')

# #read element column
#lst.element.column_name
#['P', 'T', 'SG', 'SL', 'XAIRG', 'XAIRL', 'PAIR', 'PCAP', 'DG', 'DL']
# XAIRG   ----   mass fraction of air in gas phase
# XAIRL   ----   mass fraction of air in liquid phase  ???? what does this mean?
# PAIR    ----   parial pressure of air ( i think it is air pressure)
# PCAP    ----   capillary pressure
# DL      ----   liquid density
# DG      ----   gas density
gas_saturation_xt_mtx             = np.array([lst.history(('e',i,'SG'  ))[1] for i in lst.element.row_name])
liq_saturation_xt_mtx             = np.array([lst.history(('e',i,'SL'  ))[1] for i in lst.element.row_name])
vapor_mass_fraction_in_gas_xt_mtx = 1-np.array([lst.history(('e',i,'XAIRG'))[1] for i in lst.element.row_name])
gas_density_xt_mtx_kgPm3          = np.array([lst.history(('e',i,'DG' ) )[1] for i in lst.element.row_name])          # two brackets is needed!
liq_density_xt_mtx_kgPm3          = np.array([lst.history(('e',i,'DL'  ))[1] for i in lst.element.row_name])

# #read connection column
#lst.connection.column_name
#['FLOH', 'FLOH/FLOF', 'FLOF', 'FLO(GAS)', 'VAPDIF', 'FLO(LIQ.)', 'VEL(GAS)', 'VEL(LIQ.)']
gas_flow_xt_mtx_kgPs           = -np.array([lst.history(('c',i,'FLO(GAS)'))[1] for i in lst.connection.row_name])
vapor_diff_flow_xt_mtx_kgPs    = -np.array([lst.history(('c',i,'VAPDIF'))[1] for i in lst.connection.row_name])    # c means connection, but why negative? negative may related to BETAX, which is -1 in this case
liquid_flow_xt_mtx_kgPs        = -np.array([lst.history(('c',i,'FLO(LIQ.)'))[1] for i in lst.connection.row_name])
vapor_adv_xt_mtx_kgPs          = vapor_mass_fraction_in_gas_xt_mtx[1:]*gas_flow_xt_mtx_kgPs
  
# # #read generation column 
#lst.generation.column_name
#['GENERATION RATE', 'ENTHALPY', 'FF(GAS)', 'FF(LIQ.)', 'P(WB)']
water_generation_kgPs                 = np.array([lst.history(('g',i,'GENERATION RATE'))[1] for i in lst.generation.row_name])
water_generation_vapor_mass_fraction  = np.array([lst.history(('g',i,'FF(GAS)' ))[1] for i in lst.generation.row_name])
water_generation_liquid_mass_fraction = np.array([lst.history(('g',i,'FF(LIQ.)'))[1] for i in lst.generation.row_name])           # what is FF(LIQ) mean and how did it distribute to both?
 
 
print('Check mass balance\n')  
# ---Mass Balance---
element_volume_m3                                  = np.array([blk.volume for blk in dat.grid.blocklist[1:]])
liquid_mass_element_kg                             = np.array([element_volume_m3[1:]*liq_density_xt_mtx_kgPm3[2:,i]*liq_saturation_xt_mtx[2:,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
liquid_mass_kg                                     = np.sum(liquid_mass_element_kg,axis=1) 
vapor_mass_element_kg                              = np.array([vapor_mass_fraction_in_gas_xt_mtx[2:,i]*element_volume_m3[1:]*gas_density_xt_mtx_kgPm3[2:,i]*gas_saturation_xt_mtx[2:,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
vapor_mass_kg                                      = np.sum(vapor_mass_element_kg,axis=1) 
total_water_mass_kg                                = liquid_mass_kg+vapor_mass_kg                                    
water_mass_change_over_time_kg                     = np.diff(total_water_mass_kg)

liquid_flow_top1_kgPs                              = liquid_flow_xt_mtx_kgPs[1]
vapor_flow_top1_kgPs                               = vapor_adv_xt_mtx_kgPs[1]  
vapor_diff_flow_top1_kgPs                          = vapor_diff_flow_xt_mtx_kgPs[1]
total_water_net_flux_kgPs                          = liquid_flow_top1_kgPs+vapor_diff_flow_top1_kgPs+vapor_flow_top1_kgPs
liquid_flow_amount_change_over_time_kg             = -liquid_flow_top1_kgPs[1:]*np.diff(lst.times)
vapor_diff_flow_amount_change_over_time_kg         = -vapor_diff_flow_top1_kgPs[1:]*np.diff(lst.times)
vapor_flow_amount_change_over_time_kg              = -vapor_flow_top1_kgPs[1:]*np.diff(lst.times)
water_amount_change_over_time_kg                   = -total_water_net_flux_kgPs[1:]*np.diff(lst.times)

print('water_mass_change_over_time_kg              ='+str(np.sum(water_mass_change_over_time_kg)))
print('liquid_water_mass_change_over_time_kg       ='+str(np.sum(liquid_flow_amount_change_over_time_kg)))
print('vapor_diff_water_amount_change_over_time_kg ='+str(np.sum(vapor_diff_flow_amount_change_over_time_kg)))
print('vapor_flow_water_amount_change_over_time_kg ='+str(np.sum(vapor_flow_amount_change_over_time_kg)))
print('water_amount_change_over_time_kg            ='+str(np.sum(water_amount_change_over_time_kg)))


print('Check mass balance for a 1\n')  
# ---Mass Balance---
liquid_mass_kg_a1                                          = np.array([element_volume_m3[0]*liq_density_xt_mtx_kgPm3[1,i]*liq_saturation_xt_mtx[1,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
vapor_mass_element_kg_a1                                   = np.array([vapor_mass_fraction_in_gas_xt_mtx[1,i]*element_volume_m3[0]*gas_density_xt_mtx_kgPm3[1,i]*gas_saturation_xt_mtx[1,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
total_water_mass_kg_a1                                     = liquid_mass_kg_a1+vapor_mass_element_kg_a1                                    
water_mass_change_over_time_kg_a1                          = np.diff(total_water_mass_kg_a1)
print('water_mass_change_over_time_kg_a1                   ='+str(np.sum(water_mass_change_over_time_kg_a1)))

liquid_flow_kgPs_a1toatm                                   = liquid_flow_xt_mtx_kgPs[0]
vapor_flow_kgPs_a1toatm                                    = vapor_adv_xt_mtx_kgPs[0]  
vapor_diff_flow_kgPs_a1toatm                               = vapor_diff_flow_xt_mtx_kgPs[0]
total_water_net_flux_kgPs_a1toatm                          = liquid_flow_kgPs_a1toatm+vapor_flow_kgPs_a1toatm+vapor_diff_flow_kgPs_a1toatm
liquid_flow_amount_change_over_time_kg_a1toatm             = liquid_flow_kgPs_a1toatm[1:]*np.diff(lst.times)
vapor_diff_flow_amount_change_over_time_kg_a1toatm         = vapor_flow_kgPs_a1toatm[1:]*np.diff(lst.times)
vapor_flow_amount_change_over_time_kg_a1toatm              = vapor_diff_flow_kgPs_a1toatm[1:]*np.diff(lst.times)
water_amount_change_over_time_kg_a1toatm                   = total_water_net_flux_kgPs_a1toatm[1:]*np.diff(lst.times)
#print('liquid_water_mass_change_over_time_kg_a1toatm       ='+str(np.sum(liquid_flow_amount_change_over_time_kg_a1toatm)))
#print('vapor_diff_water_amount_change_over_time_kg_a1toatm ='+str(np.sum(vapor_diff_flow_amount_change_over_time_kg_a1toatm)))
#print('vapor_flow_water_amount_change_over_time_kg_a1toatm ='+str(np.sum(vapor_flow_amount_change_over_time_kg_a1toatm)))
print('water_amount_change_over_time_kg_a1toatm            ='+str(np.sum(water_amount_change_over_time_kg_a1toatm)))
             
liquid_flow_kgPs_a2toa1                                    = liquid_flow_xt_mtx_kgPs[1]
vapor_flow_kgPs_a2toa1                                     = vapor_adv_xt_mtx_kgPs[1]  
vapor_diff_flow_kgPs_a2toa1                                = vapor_diff_flow_xt_mtx_kgPs[1]
total_water_net_flux_kgPs_a2toa1                           = liquid_flow_kgPs_a2toa1+vapor_flow_kgPs_a2toa1+vapor_diff_flow_kgPs_a2toa1   
liquid_flow_amount_change_over_time_kg_a2toa1              = liquid_flow_kgPs_a2toa1[1:]*np.diff(lst.times)
vapor_diff_flow_amount_change_over_time_kg_a2toa1          = vapor_flow_kgPs_a2toa1[1:]*np.diff(lst.times)
vapor_flow_amount_change_over_time_kg_a2toa1               = vapor_diff_flow_kgPs_a2toa1[1:]*np.diff(lst.times)
water_amount_change_over_time_kg_a2toa1                    = total_water_net_flux_kgPs_a2toa1[1:]*np.diff(lst.times)
#print('liquid_water_mass_change_over_time_kg_a2toa1        ='+str(np.sum(liquid_flow_amount_change_over_time_kg_a2toa1)))
#print('vapor_diff_water_amount_change_over_time_kg_a2toa1  ='+str(np.sum(vapor_diff_flow_amount_change_over_time_kg_a2toa1)))
#print('vapor_flow_water_amount_change_over_time_kg_a2toa1  ='+str(np.sum(vapor_flow_amount_change_over_time_kg_a2toa1)))
print('water_amount_change_over_time_kg_a2toa1             ='+str(np.sum(water_amount_change_over_time_kg_a2toa1)))


print('Check mass balance for generation\n')  
water_generation_vapor_kgPs                                = water_generation_kgPs*water_generation_vapor_mass_fraction
water_generation_liquid_kgPs                               = water_generation_kgPs*water_generation_liquid_mass_fraction
total_water_generation_kg                                  = water_generation_kgPs[0,1:]*np.diff(lst.times)
total_vapor_generation_kg                                  = water_generation_vapor_kgPs[0,1:]*np.diff(lst.times)
total_liquid_generation_kg                                 = water_generation_liquid_kgPs[0,1:]*np.diff(lst.times)
print('total_water_generation_kg                           ='+str(np.sum(total_water_generation_kg)))
print('total_vapor_generation_kg                           ='+str(np.sum(total_vapor_generation_kg)))
print('total_liquid_generation_kg                          ='+str(np.sum(total_liquid_generation_kg)))