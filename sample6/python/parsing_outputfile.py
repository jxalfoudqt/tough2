
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D

liq_density_kgPm3=1000
water_molecular_weight=0.018
R_value=8.314
m2mm=1000
day2s=3600*24
T_kelven=273.15
Pa2Kpa=1000

# --- post-process the output ---------------------------
lst = t2listing('sam6_0.listing')
dat=t2data('sam6')

connection_first_distance    = np.array([blk.distance[0] for blk in dat.grid.connectionlist])
connection_second_distance   = np.array([blk.distance[1] for blk in dat.grid.connectionlist])
element_value                = np.cumsum(np.insert(connection_first_distance+connection_second_distance,0,0))
connection_value             = np.cumsum(connection_first_distance+np.insert(connection_second_distance[:-1], 0, 0)) 
element_volume               = np.array([blk.volume for blk in dat.grid.blocklist[1:-1]])

Gas_Density                  = np.array([lst.history(('e',lst.element.row_name[i],'DG'))[1] for i in range(lst.element.num_rows)])
Liq_Density                  = np.array([lst.history(('e',lst.element.row_name[i],'DL'))[1] for i in range(lst.element.num_rows)])
Gas_saturation               = np.array([lst.history(('e',lst.element.row_name[i],'SG'))[1] for i in range(lst.element.num_rows)])
Liq_saturation               = np.array([lst.history(('e',lst.element.row_name[i],'SL'))[1] for i in range(lst.element.num_rows)])
Gas_Pressure                 = np.array([lst.history(('e',lst.element.row_name[i],'P'))[1] for i in range(lst.element.num_rows)])
Air_Pressure                 = np.array([lst.history(('e',lst.element.row_name[i],'PAIR'))[1] for i in range(lst.element.num_rows)])
Capillary_Pressure           = np.array([lst.history(('e',lst.element.row_name[i],'PCAP'))[1] for i in range(lst.element.num_rows)])
Temperature                  = np.array([lst.history(('e',lst.element.row_name[i],'T'))[1] for i in range(lst.element.num_rows)])
Vapor_mass_fraction_in_gas   = 1-np.array([lst.history(('e',lst.element.row_name[i],'XAIRG'))[1] for i in range(lst.element.num_rows)])
                             
Liquid_flow_kgPs             = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(LIQ.)'))[1] for i in range(lst.connection.num_rows)])
Liquid_flow_raw              = Liquid_flow_kgPs/dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
Gas_flow_kgPs                = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(GAS)'))[1] for i in range(lst.connection.num_rows)])
Gas_flow_raw                 = Gas_flow_kgPs/dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
Vapor_diff_flow_kgPs         = np.array([lst.history(('c',lst.connection.row_name[i],'VAPDIF'))[1] for i in range(lst.connection.num_rows)])
Vapor_diff_flow_raw          = Vapor_diff_flow_kgPs/dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s

Vapor_flow_raw               = (Vapor_mass_fraction_in_gas[1:]+Vapor_mass_fraction_in_gas[:-1])/2*Gas_flow_raw
Vapor_flow_raw_kgPs          = (Vapor_mass_fraction_in_gas[1:]+Vapor_mass_fraction_in_gas[:-1])/2*Gas_flow_kgPs
Vapor_flow_adv_raw           = Vapor_flow_raw-Vapor_diff_flow_raw
Air_flow_raw                 = (1-(Vapor_mass_fraction_in_gas[1:]+Vapor_mass_fraction_in_gas[:-1])/2)*Gas_flow_raw
Vapor_pressure               = Gas_Pressure-Air_Pressure

Liquid_flow_topsoil          = Liquid_flow_raw[0]
Gas_flow_topsoil             = Gas_flow_raw[0]
Vapor_flow_topsoil           = Vapor_flow_raw[0]
Vapor_flow_adv_topsoil       = Vapor_flow_adv_raw[0]
Vapor_diff_flow_topsoil      = Vapor_diff_flow_raw[0]
Air_flow_topsoil             = Air_flow_raw[0] 

Liquid_flow_bottom_kgPs      = Liquid_flow_kgPs[-1]
Vapor_flow_bottom_kgPs       = Vapor_flow_raw_kgPs[-1]
Liquid_flow_top_kgPs         = Liquid_flow_kgPs[0]
Vapor_flow_top_kgPs          = Vapor_flow_raw_kgPs[0]

Gas_permeability             = np.array([lst.history(('p',lst.primary.row_name[i],'K(GAS)'))[1] for i in range(lst.primary.num_rows)])
Liq_permeability             = np.array([lst.history(('p',lst.primary.row_name[i],'K(LIQ.)'))[1] for i in range(lst.primary.num_rows)])

# GAS_H                        = np.array([lst.history(('p',lst.primary.row_name[i],'H(GAS)'))[1] for i in range(lst.primary.num_rows)])
# Liq_H                        = np.array([lst.history(('p',lst.primary.row_name[i],'H(LIQ.)'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_change   = np.array([lst.history(('p',lst.primary.row_name[i],'DX1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_change  = np.array([lst.history(('p',lst.primary.row_name[i],'DX2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_change   = np.array([lst.history(('p',lst.primary.row_name[i],'DX3'))[1] for i in range(lst.primary.num_rows)])
# First_thermodynamic_var      = np.array([lst.history(('p',lst.primary.row_name[i],'X1'))[1] for i in range(lst.primary.num_rows)])
# Second_thermodynamic_var     = np.array([lst.history(('p',lst.primary.row_name[i],'X2'))[1] for i in range(lst.primary.num_rows)])
# Third_thermodynamic_var      = np.array([lst.history(('p',lst.primary.row_name[i],'X3'))[1] for i in range(lst.primary.num_rows)])
                             
Gas_mass_element             = np.array([element_volume*Gas_Density[1:-1,i]*Gas_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
Liquid_mass_element          = np.array([element_volume*Liq_Density[1:-1,i]*Liq_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
Vapor_mass_element           = np.array([Vapor_mass_fraction_in_gas[1:-1,i]*element_volume*Gas_Density[1:-1,i]*Gas_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
Air_mass_element             = np.array([(1-Vapor_mass_fraction_in_gas[1:-1,i])*element_volume*Gas_Density[1:-1,i]*Gas_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity for i in range(lst.num_times)])
Gas_mass                     = np.sum(Gas_mass_element,axis=1) 
Liquid_mass                  = np.sum(Liquid_mass_element,axis=1) 
Vapor_mass                   = np.sum(Vapor_mass_element,axis=1) 
Air_mass                     = np.sum(Air_mass_element,axis=1)

Net_water_mass=np.diff(Liquid_mass+Vapor_mass)
Total_water_flux=(Liquid_flow_bottom_kgPs+Vapor_flow_bottom_kgPs-Liquid_flow_top_kgPs-Vapor_flow_top_kgPs)
Net_water_flux=Total_water_flux[:-1]*np.diff(lst.times)
