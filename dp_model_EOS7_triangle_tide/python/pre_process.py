from t2listing import *
import numpy as np
from t2data import *


# #--- set up variables ---------------------------------
liquid_density_kgPm3        = 1000
brine_default_density_kgPm3 = 1185.1
water_molecular_weight      = 0.018
R_value                     = 8.3145
mPmm                        = 1.e-3
dayPs                       = 1./(3600*24)
T_kelven                    = 273.15
T_initial                   = 25.0
p_atm_pa                    = 101.3e3
simulation_time_s           = 40*3600*24
max_no_time_steps           = 6000 


# #--- set up the title ---------------------------------
dat       = t2data()
dat.title = 'dp_model_flow'


# #--- set up the model ---------------------------------
length_x = 40.
nblks_x  = 80
length_z = 6.
nblks_z  = 12
dx       = [length_x / nblks_x] * nblks_x
dz       = [length_z / nblks_z] * nblks_z
dy       = [0.5]
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
     'texp'           : 1.8,	
     'timestep'       : [1.0],
     'print_block'    : 'cb  9',
     'default_incons' : [p_atm_pa, 0, 10.99, T_initial, None],
     'relative_error' : 1.e-6,
     'print_interval' : max_no_time_steps/20,
     'max_timestep'   : simulation_time_s/max_no_time_steps})  # the maximum length of time step in second
     

# #Set MOPs:
dat.parameter['option'][1] = 1
dat.parameter['option'][7] = 0
dat.parameter['option'][11] = 0
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
Residual_saturation      = 0.045
r1.relative_permeability = {'type': 7, 'parameters': [0.627, Residual_saturation, 1., 0.054]}
r1.capillarity           = {'type': 7, 'parameters': [0.627, Residual_saturation-1.e-5, 5.e-4, 1.e8, 1.]}
dat.grid.add_rocktype(r1)

r2 = rocktype('BOUN1',
           nad           = 2,
           porosity      = 0.99,
           density       = 2650.,
           permeability  = [2.e-6, 2.e-6, 2.e-6],
           conductivity  = 2.51,
           specific_heat = 1.e5)
r2.relative_permeability = {'type': 1, 'parameters': [0.1, 0., 1., 0.1]}
r2.capillarity           = {'type': 1, 'parameters': [0., 0., 1.0]}
dat.grid.add_rocktype(r2)

r3 = rocktype('BOUN2',
           nad           = 2,
           porosity      = 0.99,
           density       = 2650.,
           permeability  = [2.e-6, 2.e-6, 2.e-6],
           conductivity  = 2.51,
           specific_heat = 1.e5)
r3.compressibility       = 1.e-10
r3.relative_permeability = {'type': 1, 'parameters': [0.1, 0., 1., 0.1]}
r3.capillarity           = {'type': 1, 'parameters': [0., 0., 1.0]}
dat.grid.add_rocktype(r2)

# #assign rocktype and parameter values:
conarea = dx[0] * dy[0]
for blk in dat.grid.blocklist:
    blk.rocktype = r1
    blk.ahtx     = conarea                                   # interface area for heat exchange
	
# #add boundary condition block at each end:
bvol    = 1.e50
condist = 1.e-10
for i in range(nblks_z):
    b1 = t2block('zzz'+str(i+1), bvol, r2,
                ahtx      = conarea,                            # area for heat exchange
                centre    = np.array([0, dy[0]/2, -(length_z/nblks_z+i)/2])) # important for plotting
    dat.grid.add_block(b1)
    con1 = t2connection([b1, dat.grid.blocklist[i*nblks_x], b1],
                    distance  = [condist,0.5*dx[0]],
                    area      = conarea,
                    direction = 1,
                    dircos    = 0)
    dat.grid.add_connection(con1)

# for i in range(nblks_z-8):
    # b2 = t2block('zzz'+str(nblks_z+i+1), bvol, dat.grid.rocktype['BOUND'])
    # b2.volume=1.e50
    # dat.grid.add_block(b2)
    # con2 = t2connection([dat.grid.blocklist[nblks_x-1+(i+8)*nblks_x], b2],
                    # distance = [0.5*dx[nblks_x-1], condist], area = conarea, direction=1)
    # dat.grid.add_connection(con2)
    # dat.grid.connectionlist[-1].dircos=0
    # dat.grid.blocklist[-1].ahtx=conarea
    # dat.grid.blocklist[-1].centre=np.array([length_x,0.25,-(length_z/nblks_z+i+8)/2])

# # #Set initial condition:
# mean_water_level_m=3
# for i in range(nblks_z-8):
    # dat.incon[str(dat.grid.blocklist[-(i+1)])] = [None, [p_atm_pa-liquid_density_kgPm3*dat.parameter['gravity']*(dat.grid.blocklist[-(i+1)].centre[2]+mean_water_level_m), 1, 10.01, T_initial]]
# for i in range(nblks_z-1):
    # dat.incon[str(dat.grid.blocklist[-(i+1+nblks_z-8)])] = [None, [p_atm_pa-liquid_density_kgPm3*dat.parameter['gravity']*(dat.grid.blocklist[-(i+1+nblks_z-8)].centre[2]), 0, 10.01, T_initial]]

b2 = t2block('zzz'+str(nblks_z+1), bvol, r3,
            ahtx      = conarea,                          
            centre    = np.array([length_x,dy[0]/2,-(length_z/nblks_z+8)/2]))
dat.grid.add_block(b2)
con2 = t2connection([dat.grid.blocklist[nblks_x-1+8*nblks_x], b2],
            distance  = [0.5*dx[nblks_x-1], condist], 
            area      = conarea,
            direction = 1,
            dircos    = 0)
dat.grid.add_connection(con2)


# #Set initial condition:
mean_water_level_m=3
dat.incon[str(dat.grid.blocklist[-1])] = \
         [None, [p_atm_pa-liquid_density_kgPm3*dat.parameter['gravity']*(dat.grid.blocklist[-1].centre[2]+mean_water_level_m), 1, 0, T_initial]]
for i in range(nblks_z-1):
    dat.incon[str(dat.grid.blocklist[-(i+2)])] = \
	         [None, [p_atm_pa-liquid_density_kgPm3*dat.parameter['gravity']*(dat.grid.blocklist[-(i+2)].centre[2]), 0, 10.01, T_initial]]

# # set upper right trangle block:
j=0
while j<9:
    i=j*10
    while i<nblks_x:
        dat.grid.blocklist[j*80+i].rocktype=r2
        i+=1
    j+=1

# # #add generator:
# time_variation_s       = np.arange(10*24*3600,dat.parameter['tstop'],(dat.parameter['tstop']-10*24*3600)/100.)
# pressure_zero          = dat.incon[str(dat.grid.blocklist[-1])][1][0]
# pressure_pa            = pressure_zero*(1+(np.sin(np.linspace(0,20*np.pi,len(time_variation_s)))+1)*0.1)
# flow_rate_kgPs         = liquid_density_kgPm3*bvol*r3.porosity*r3.compressibility*pressure_zero*0.1*np.cos(np.linspace(0,20*np.pi,len(time_variation_s)))
# gen = t2generator(name = 'INF 1', block = 'zzz13', ltab=len(time_variation_s),
                  # rate=flow_rate_kgPs, time= time_variation_s, type = 'COM1')		
# dat.add_generator(gen)

# # #set react:                                                            
# dat.add_react(mopr=[None,2,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])                    # only run tough2 no toughreact


# #--- write TOUGH2 input file ------------------------------------	
dat.write(dat.title[:19])
print("file generated\n")