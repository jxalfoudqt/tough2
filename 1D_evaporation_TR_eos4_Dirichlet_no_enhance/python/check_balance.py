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
  
print('Check mass balance\n')  
# ---Mass Balance---
element_volume_m3                 = np.array([blk.volume for blk in dat.grid.blocklist[1:]])
liquid_mass_element_kg            = np.array([element_volume_m3*liq_density_xt_mtx_kgPm3[1:,i]*liq_saturation_xt_mtx[1:,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
liquid_mass_kg                    = np.sum(liquid_mass_element_kg,axis=1) 
vapor_mass_element_kg             = np.array([vapor_mass_fraction_in_gas_xt_mtx[1:,i]*element_volume_m3*gas_density_xt_mtx_kgPm3[1:,i]*gas_saturation_xt_mtx[1:,i]*dat.grid.rocktype['SAND '].porosity for i in range(lst.num_times)])
vapor_mass_kg                     = np.sum(vapor_mass_element_kg,axis=1) 
total_water_mass_kg               = liquid_mass_kg+vapor_mass_kg                                    
water_mass_change_over_time_kg    = np.diff(total_water_mass_kg)

liquid_flow_top1_kgPs                      = liquid_flow_xt_mtx_kgPs[0]
vapor_flow_top1_kgPs                       = vapor_adv_xt_mtx_kgPs[0]  
vapor_diff_flow_top1_kgPs                  = vapor_diff_flow_xt_mtx_kgPs[0]
total_water_net_flux_kgPs                  = liquid_flow_top1_kgPs+vapor_diff_flow_top1_kgPs+vapor_flow_top1_kgPs
liquid_flow_amount_change_over_time_kg     = -liquid_flow_top1_kgPs[1:]*np.diff(lst.times)
vapor_diff_flow_amount_change_over_time_kg = -vapor_diff_flow_top1_kgPs[1:]*np.diff(lst.times)
vapor_flow_amount_change_over_time_kg      = -vapor_flow_top1_kgPs[1:]*np.diff(lst.times)
water_amount_change_over_time_kg           = -total_water_net_flux_kgPs[1:]*np.diff(lst.times)

print('water_mass_change_over_time_kg              ='+str(np.sum(water_mass_change_over_time_kg)))
print('liquid_water_mass_change_over_time_kg       ='+str(np.sum(liquid_flow_amount_change_over_time_kg)))
print('vapor_diff_water_amount_change_over_time_kg ='+str(np.sum(vapor_diff_flow_amount_change_over_time_kg)))
print('vapor_flow_water_amount_change_over_time_kg ='+str(np.sum(vapor_flow_amount_change_over_time_kg)))
print('water_amount_change_over_time_kg            ='+str(np.sum(water_amount_change_over_time_kg)))