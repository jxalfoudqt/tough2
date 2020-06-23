from t2listing import *
import numpy as np
from t2data import *


# #--- set up variables ---------------------------------
liquid_density_kgPm3        = 999.22
brine_default_density_kgPm3 = 1185.1
water_molecular_weight      = 0.018
R_value                     = 8.3145
mPmm                        = 1.e-3
dayPs                       = 1./(3600*24)
T_kelven                    = 273.15
T_initial                   = 15.0
p_atm_pa                    = 101.3e3
simulation_time_s           = 365*3600*24.
max_no_time_steps           = 9999
 
# #--- set up the title ---------------------------------
dat       = t2data()
dat.title = 'NB_for_TDB'


# #--- set up the model ---------------------------------
length_x = 1.
nblks_x  = 1
dx       = [length_x / nblks_x] * nblks_x
dz = dy  = [1.]
geo      = mulgrid().rectangular(dx, dy, dz)
#geo.write(dat.title+'.dat')

# #Create TOUGH2 input data file:
dat.grid = t2grid().fromgeo(geo)
dat.parameter.update(
    {'max_timesteps'  : max_no_time_steps,
     'const_timestep' : -1,
     'tstop'          : simulation_time_s,
     'gravity'        : 9.81,
     'print_level'    : 2,
     'max_iterations' : 99,
     'texp'           : 1.8,	
     'timestep'       : [1.0],
    # 'print_block'    : 'cb  9',
     'default_incons' : [p_atm_pa, 0, 10.99, T_initial, None],
     'relative_error' : relative_error_parameter[k],
     'print_interval' : max_no_time_steps/max_no_time_steps,
     'max_timestep'   : maximum_dt_parameter[q]})  # the maximum length of time step in second
     

# #Set MOPs:
dat.parameter['option'][1] = 1
dat.parameter['option'][7] = 0
dat.parameter['option'][9] = 1
dat.parameter['option'][11] = 0
dat.parameter['option'][12] = 0
dat.parameter['option'][16] = 4
dat.parameter['option'][19] = 2
dat.parameter['option'][21] = 3
dat.parameter['option'][22] = 1

# #Set start:
dat.start = True

# #Set diffusion:
#dat.diffusion=[[2.13e-5,     0.e-8],
#               [2.13e-5,     0.e-8]]

# #Set multi choice:	
dat.multi={'num_components'           : 3,
           'num_equations'            : 3,
           'num_phases'               : 2,
           'num_secondary_parameters' : 6}
		   
# # #Set SELEC:   
dat.selection={'float':[None],'integer':[2]}

# # #Set TIMES: 
# dat.output_times = {'num_times_specified': int(simulation_time_s*dayPs),
                    # 'time': list( np.arange(int(simulation_time_s*dayPs)) *sPday   )}

# #deleted prior rocktype: 
dat.grid.delete_rocktype('dfalt')

# #Add another rocktype, with relative permeability and capillarity functions & parameters:
# relative_humidity=0.1
# P_bound=np.log(relative_humidity)*liquid_density_kgPm3*R_value*(T_initial+T_kelven)/water_molecular_weight
# r2.relative_permeability = {'type': 1, 'parameters': [0.1,0.0,1.0,0.1,]}
# r2.capillarity = {'type': 1, 'parameters': [-P_bound, 0., 1.0]}	
r1 = rocktype('SAND ',
           nad           = 2,
           porosity      = 0.45,
           density       = 2650.,
           permeability  = [2.e-12, 2.e-12, 2.e-12],
           conductivity  = 2.51,
           specific_heat = 920)
r1.tortuosity            = 0
r1.compressibility       = 0
Residual_saturation      = 0.045
r1.relative_permeability = {'type': 7, 'parameters': [0.627, Residual_saturation, 1., 0.054]}
r1.capillarity           = {'type': 7, 'parameters': [0.627, Residual_saturation-1.e-5, 5.e-4, 1.e8, 1.]}
dat.grid.add_rocktype(r1)

r3 = rocktype('BOUN2',
           nad           = 2,
           porosity      = porosity_parameter[o],
           density       = 2650.,
           permeability  = [2.e-6, 2.e-6, 2.e-6],
           conductivity  = 2.51,
           specific_heat = 1.e5)
r3.compressibility       = compressibility_parameter[s]
r3.relative_permeability = {'type': 1, 'parameters': [0.1, 0., 1., 0.1]}
r3.capillarity           = {'type': 1, 'parameters': [0., 0., 1.0]}
dat.grid.add_rocktype(r3)

# #assign rocktype and parameter values:
conarea = dx[0] * dy[0]
for blk in dat.grid.blocklist:
    blk.rocktype = r1
    blk.ahtx     = conarea                                   # interface area for heat exchange
	
# #add boundary condition block at each end:
bvol    = volume_parameter[p]
condist = 1.e-10

b2 = t2block('zzz13', bvol, r3,
            ahtx      = conarea,                          
            centre    = np.array([length_x,dy[0]/2,-dz[0]/2]))
dat.grid.add_block(b2)
con2 = t2connection([dat.grid.blocklist[nblks_x-1], b2],
            distance  = [0.5*dx[nblks_x-1], condist], 
            area      = conarea,
            direction = 1,
            dircos    = 0)
dat.grid.add_connection(con2)


# #Set initial condition:
dat.incon[str(dat.grid.blocklist[-1])] = \
         [None, [p_atm_pa-liquid_density_kgPm3*dat.parameter['gravity']*(dat.grid.blocklist[-1].centre[2]), 0, 0, T_initial]]

# #add generator:
max_bdy_point_numbers  = 10000.
water_compressibility  = 4.55351e-10
time_variation_s       = np.arange(0, dat.parameter['tstop'],  dat.parameter['tstop']/max_bdy_point_numbers)
time_variation_par     = 2*np.pi/3600/24 
pressure_zero          = dat.incon[str(dat.grid.blocklist[-1])][1][0]
pressure_pa            = pressure_zero*np.sin(time_variation_par*time_variation_s)*0.05+pressure_zero
flow_rate_kgPs         = liquid_density_kgPm3*bvol*(r3.porosity)*(r3.compressibility+water_compressibility)*pressure_zero*np.cos(time_variation_par*time_variation_s)*time_variation_par*0.05
#flow_rate_kgPs         = liquid_density_kgPm3*bvol*r3.porosity*r3.compressibility*pressure_zero*np.cos(time_variation_s)
#flow_rate_kgPs         = liquid_density_kgPm3*bvol*((1-r3.porosity)*r3.compressibility-r3.porosity*water_compressibility)*pressure_zero*np.cos(time_variation_par*time_variation_s)*time_variation_par
gen = t2generator(name = 'INF 1', block = 'zzz13', ltab=len(time_variation_s),
                  rate=flow_rate_kgPs, time= time_variation_s, type = 'COM1')		
dat.add_generator(gen)

# # #set react:                                                            
# dat.add_react(mopr=[None,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])                    # only run tough2 no toughreact


# #--- write TOUGH2 input file ------------------------------------	
dat.write(dat.title)
print("file generated\n")