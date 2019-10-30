
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D

liquid_density_kgPm3=1000
water_molecular_weight=0.018
R_value=8.3145
mPmm=1.e-3
dayPs=1./(3600*24)
T_kelven=273.15

dat = t2data()
dat.title = '1D_evaporation_eos4'

# #--- set up the model ---------------------------------
length = 1.
nblks = 50
dz = [length / nblks] * nblks
dy = dx = [0.1]
geo = mulgrid().rectangular(dx, dy, dz)
geo.write(dat.title+'.dat')

# #Create TOUGH2 input data file:
dat.grid = t2grid().fromgeo(geo)
dat.parameter.update(
    {'max_timesteps': 8.e3,
     'const_timestep': -1,
     'tstop': 7.e10,
     'gravity': 9.81,
     'print_level': -3,
     'texp': 2.41e-05,	
     'timestep': [1.0],
     'be': 2.334,
     'default_incons': [101.3e3, 10.99, 13.0, None]})
	 
dat.parameter['print_interval']=dat.parameter['max_timesteps']/50.
dat.parameter['max_timestep']=dat.parameter['tstop']/dat.parameter['max_timesteps']

dat.start = True
dat.diffusion=[[2.13e-5,     0.e-8],   [2.13e-5,     0.e-8]]
dat.multi={'num_components': 2, 'num_equations': 3, 'num_phases': 2, 'num_secondary_parameters': 8}

# #Set MOPs:
dat.parameter['option'][1] = 1
dat.parameter['option'][7] = 0
dat.parameter['option'][11] = 0
dat.parameter['option'][16] = 4
dat.parameter['option'][19] = 2
dat.parameter['option'][21] = 3

# #Add another rocktype, with relative permeability and capillarity functions & parameters:
r1 = rocktype('SAND ', nad=2, porosity=0.45,density=2650.,permeability = [2.e-12, 2.e-12, 2.e-12],conductivity=2.51,specific_heat=920)
dat.grid.add_rocktype(r1)
r1.relative_permeability = {'type': 7, 'parameters': [0.627, 0.045, 1., 0.054]}
r1.capillarity = {'type': 7, 'parameters': [0.627, 0.045, 5.e-4, 1.e8, 1.]}
	
r2 = rocktype('BOUND', nad=2,porosity=0.99,density=2650., permeability = [2.e-12, 2.e-12, 2.e-12],conductivity=2.51,specific_heat=1.e5)
dat.grid.add_rocktype(r2)
#r2.relative_permeability = {'type': 1, 'parameters': [0.1, 0., 1., 0.1]}
#r2.capillarity = {'type': 1, 'parameters': [0., 0., 1.0]}

r2.relative_permeability = {'type': 1, 'parameters': [0.1,0.0,1.0,0.1,]}
r2.capillarity = {'type': 1, 'parameters': [0., 0., 1.0]}

bvol = 0.0
conarea = dx[0] * dy[0]
condist = 1.e-10
  
# #assign rocktype and parameter values:
for blk in dat.grid.blocklist:
    blk.rocktype = r1
    blk.ahtx=conarea
	
# #add boundary condition block at each end:
b1 = t2block('bdy01', bvol, r2)
b1.volume=1.e50
dat.grid.add_block(b1)

con1 = t2connection([dat.grid.blocklist[0],b1],
                    distance = [0.5*dz[0],condist], area = conarea, direction=3)
dat.grid.add_connection(con1)

# b2 = t2block('bdy02', bvol, dat.grid.rocktype['BOUND'])
# dat.grid.add_block(b2)
# con2 = t2connection([dat.grid.blocklist[nblks-1], b2],
                    # distance = [0.5*dz[nblks-1], condist], area = conarea, direction=3)
# dat.grid.add_connection(con2)

dat.grid.connectionlist[-1].dircos=-1
dat.grid.blocklist[-1].ahtx=conarea

# #Set initial condition:
for i in range(len(dat.grid.blocklist)-1):
    dat.incon[str(dat.grid.blocklist[i])] = [None, [101.3e3+dat.grid.blocklist[i].centre[2]*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 10.01, 25.0]]
dat.incon['bdy01'] = [None, [101.3e3, 1.0, 25.0]]

# #add generator:
flow_rate_mmPday=-5
flow_rate_kgPs=flow_rate_mmPday*conarea*liquid_density_kgPm3*mPmm*dayPs
gen = t2generator(name = 'INF 1', block = dat.grid.blocklist[0].name,
                  gx = flow_rate_kgPs, type = 'COM1')
dat.add_generator(gen)


# #--- write TOUGH2 input file ------------------------------------	
dat.grid.blocklist.insert(0,dat.grid.blocklist[-1])
del dat.grid.blocklist[-1]
dat.grid.connectionlist.insert(0,dat.grid.connectionlist[-1])
del dat.grid.connectionlist[-1]
dat.write(dat.title)