from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D


# #--- set up variables ---------------------------------
liquid_density_kgPm3        = 1000
water_molecular_weight      = 0.018
R_value                     = 8.3145
mPmm                        = 1.e-3
dayPs                       = 1./(3600*24)
sPday                       = 3600*24.
T_init_c                    = 13.0
T_kelven                    = 273.15
p_atm_pa                    = 101.3e3
simulation_time_s           = 100*3600*24
max_no_time_steps           = 3000 
brine_density_kgPm3         = 1185.1

# #--- set up the title ---------------------------------
inp       = t2data()
inp.title = 'flow.inp'


# #--- set up the model ---------------------------------
length = 1.
nblks = 50
dz = [length / nblks] * nblks
dy = dx = [0.1]
geo = mulgrid().rectangular(dx, dy, dz)

# #Create TOUGH2 input data file:
inp.grid = t2grid().fromgeo(geo)
inp.parameter.update(
    {'max_timesteps'  : max_no_time_steps,
     'const_timestep' : -1,
     'tstop'          : simulation_time_s,
     'gravity'        : 9.81,
     'print_level'    : 2,
     'texp'           : 1.8,	
     'timestep'       : [1.0],
     'be'             : 2.334,
     'default_incons' : [p_atm_pa, 0, 10.99, T_init_c, None],
     'relative_error' : 1.e-6,
     'print_interval' : max_no_time_steps/20,
     'max_timestep'   : simulation_time_s/max_no_time_steps  # the maximum length of time step in second
     })
# #Set MOPs:
inp.parameter['option'][1] = 1
inp.parameter['option'][7] = 0
inp.parameter['option'][11] = 0
inp.parameter['option'][16] = 4
inp.parameter['option'][19] = 2
inp.parameter['option'][21] = 3

# #Set start:
inp.start = True

# #Set diffusion:
inp.diffusion=[[2.13e-5,     0.e-8],
               [2.13e-5,     0.e-8]]
			   
# #Set multi choice:				   
inp.multi={'num_components'           : 3, 
           'num_equations'            : 4, 
           'num_phases'               : 2, 
           'num_secondary_parameters' : 8}

# # #Set SELEC:   
inp.selection={'float':[None],'integer':[2]}

# # #Set TIMES: 
# inp.output_times = {'num_times_specified': int(simulation_time_s*dayPs),
                    # 'time': list( np.arange(int(simulation_time_s*dayPs)) *sPday   )}

# #deleted prior rocktype: 
inp.grid.delete_rocktype('dfalt')


# #Add another rocktype, with relative permeability and capillarity functions & parameters:					
relative_humidity        = 0.1
P_bound                  = np.log(relative_humidity)*liquid_density_kgPm3*R_value*(T_init_c+T_kelven)/water_molecular_weight
r1                       = rocktype('SAND ',
                           nad           = 2, 
                           porosity      = 0.45,
                           density       = 2650.,
                           permeability  = [2.e-12, 2.e-12, 2.e-12],
                           conductivity  = 2.51,
                           specific_heat = 920)
Residual_saturation      = 0.045
r1.relative_permeability = {'type': 7, 'parameters': [0.627, Residual_saturation, 1., 0.054]}
r1.capillarity           = {'type': 7, 'parameters': [0.627, Residual_saturation-1.e-5, 5.e-4, -P_bound, 1.]}
inp.grid.add_rocktype(r1)
	
r2                       = rocktype('BOUND',
                           nad           = 2,
                           porosity      = 0.99,
                           density       = 2650., 
                           permeability  = [2.e-12, 2.e-12, 2.e-12],
                           conductivity  = 2.51,
                           specific_heat = 1.e5)
r2.relative_permeability = {'type': 1, 'parameters': [0.1,0.0,1.0,0.1,]}
r2.capillarity           = {'type': 1, 'parameters': [-P_bound, 0., 1.0]}
inp.grid.add_rocktype(r2)

# #assign rocktype and parameter values:
conarea = dx[0] * dy[0]
for blk in inp.grid.blocklist:
    blk.rocktype = r1
    blk.ahtx     = conarea
	
# #add boundary condition block at each end:
bvol    = 1.e50
condist = 1.e-10
b1 = t2block('bdy01', bvol, r2,
             ahtx      = conarea,                            # area for heat exchange
             centre    = np.array([ dx[0]/2,dy[0]/2,0   ])   # important for plotting
             ) 
inp.grid.blocklist.insert(0,b1)
con1 = t2connection([inp.grid.block['  a 1'],b1],
                    distance  = [0.5*dz[0],condist],
                    area      = conarea, 
                    direction = 3,                           # which to read permeability
                    dircos    = -1)                          # ISOT not BETX
inp.grid.connectionlist.insert(0,con1)

# #Set initial condition:
for i in range(len(inp.grid.blocklist)-1):
    inp.incon[str(inp.grid.blocklist[i+1])] = \
	    [None, [p_atm_pa-inp.grid.blocklist[i+1].centre[2]*liquid_density_kgPm3*inp.parameter['gravity'], 0.2, 10.01, T_init_c]]
inp.incon['bdy01'] = [None, [p_atm_pa, 0.0001, 0.9999, T_init_c]]

# # #set react:                                                            
# inp.add_react(mopr=[None,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])                    # only run tough2 no toughreact


# #--- write TOUGH2 input file (obsolete)------------------------------------	
inp.write(inp.title)
print("file " + inp.title +" generated\n")