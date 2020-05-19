import numpy as np
from t2listing import *
from t2data import *


# #--- set up variables ---------------------------------
liquid_density_kgPm3   = 1000
water_molecular_weight = 0.018
R_value                = 8.3145
mPmm                   = 1.e-3
dayPs                  = 1./(3600*24)
sPday                  = 3600*24.
T_init_c               = 25.0
T_kelven               = 273.15
p_atm_pa               = 101.3e3
simulation_time_s      = 100*3600*24
max_no_time_steps      = 1000 


# #--- set up the title ---------------------------------
inp       = t2data()
inp.title = 'flow.inp'


# #--- set up the model ---------------------------------
length = 1.
nblks  = 50
dz     = [length / nblks] * nblks
dy     = dx  = [0.1]
geo    = mulgrid().rectangular(dx, dy, dz)
#geo   = mulgrid().rectangular(dx, dy, dz, atmos_type = 0)

# #Create TOUGH2 input data file:
inp.grid = t2grid().fromgeo(geo)
inp.parameter.update(
    {'max_timesteps'  : max_no_time_steps,                   # maximum number of time steps, 9999 in TR means max_timesteps do not restrict the simulation time
     'const_timestep' : -1,
     'tstop'          : simulation_time_s,
     'gravity'        : 9.81,
     'print_level'    : 2,                                   #-3 SO far TR can not handle print level >2
     'texp'           : 2.41e-05,                            # default vapour diffusion coefficient. note this is not 1e-9m2/s for solute
     'timestep'       : [1.0],
     'be'             : 2.334,
     'default_incons' : [p_atm_pa, 10.99, T_init_c, None],
     'relative_error' : 1.e-6,
     'print_interval' : max_no_time_steps/max_no_time_steps,
     'max_timestep'   : simulation_time_s/max_no_time_steps  # the maximum length of time step in second
     })

# #Set MOPs:
inp.parameter['option'][1]  = 1
inp.parameter['option'][7]  = 0
inp.parameter['option'][9]  = 1
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
inp.multi={ 'num_components'           : 2,                  # warning, the key needs to be exactly the same, no extra spacings
            'num_equations'            : 3,
            'num_phases'               : 2,
            'num_secondary_parameters' : 8}

# # #Set TIMES: 
# inp.output_times = {'num_times_specified': int(simulation_time_s*dayPs),
                    # 'time': list( np.arange(int(simulation_time_s*dayPs)) *sPday   )}

# #deleted prior rocktype: 
inp.grid.delete_rocktype('dfalt')

# #Add rocktype, with relative permeability and capillarity functions & parameters:
r1 = rocktype('SAND ', 
           nad           = 2,
           porosity      = 0.45,
           density       = 2650.,
           permeability  = [2.e-12, 2.e-12, 2.e-12],
           conductivity  = 2.51,
           specific_heat = 920)
Residual_saturation      = 0.045
r1.relative_permeability = {'type': 7, 'parameters': [0.627, Residual_saturation, 1., 0.054]}
r1.capillarity           = {'type': 7, 'parameters': [0.627, Residual_saturation-1.e-5, 5.e-4, 1.e8, 1.]}
inp.grid.add_rocktype(r1)
	
r2 = rocktype('BOUND',
           nad           = 2,
           porosity      = 0.99,
           density       = 2650.,
           permeability  = [2.e-12, 2.e-12, 2.e-12],
           conductivity  = 2.51,
           specific_heat = 1.e5)
r2.relative_permeability = {'type': 1, 'parameters': [0.1,0.0,1.0,0.1,]}
r2.capillarity           = {'type': 1, 'parameters': [0., 0., 1.0]}
inp.grid.add_rocktype(r2)

# #assign rocktype and parameter values:
conarea = dx[0] * dy[0]
for blk in inp.grid.blocklist:
    blk.rocktype = r1
    blk.ahtx     = conarea                                   # interface area for heat exchange
	
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
           [None, [p_atm_pa - inp.grid.blocklist[i+1].centre[2]*(-1)*liquid_density_kgPm3*inp.parameter['gravity'], 10.01, T_init_c]]

# for num,key in enumerate(inp.grid.blocklist):
    # if str(key)[:3]=='  a':
        # inp.incon[str(key)] = \
                # [None, [p_atm_pa - inp.grid.block[str(key)].centre[2]*liquid_density_kgPm3*inp.parameter['gravity'], 10.01, T_init_c]]

inp.incon['bdy01']       = [None, [p_atm_pa, 0.99, T_init_c]]      # what does 0.99 mean?
inp.incon['  a 1'][1][1] = 10.99                                   # why is this needed?

# #add generator:
flow_rate_mmPday = -5.
flow_rate_kgPs   = flow_rate_mmPday*conarea*liquid_density_kgPm3*mPmm*dayPs
gen              = t2generator(name  = 'INF 1', 
                               block = '  a 1',      #inp.grid.blocklist[1].name,
                               gx   = flow_rate_kgPs,
                               type = 'COM1')
inp.add_generator(gen)

# # #set react:                                                            
# inp.add_react(mopr=[None,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])                    # only run tough2 no toughreact


# #--- write TOUGH2 input file (obsolete)------------------------------------	
inp.write(inp.title)
print("file " + inp.title +" generated\n")