
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D

liquid_density_kgPm3=1000
brine_density_kgPm3=1185.1
water_molecular_weight=0.018
R_value=8.3145
mPmm=1.e-3
dayPs=1./(3600*24)
T_kelven=273.15

dat = t2data()
dat.title = 'dp_model_flow'

# #--- set up the model ---------------------------------
length_x = 10.
nblks_x = 100
length_z = 5.
nblks_z = 50
dx = [length_x / nblks_x] * nblks_x
dz = [length_z / nblks_z] * nblks_z
dy = [0.1]
geo = mulgrid().rectangular(dx, dy, dz)
geo.write(dat.title+'.dat')

# #Create TOUGH2 input data file:
dat.grid = t2grid().fromgeo(geo)
dat.parameter.update(
    {'max_timesteps': 1.e3,
     'const_timestep': -1,
     'tstop': 1.5e6,
     'gravity': 9.81,
     'print_level': 2,
     'texp': 1.8,	
     'timestep': [1.0],
     'default_incons': [101.3e3, 0, 0.99, 13.0, None]})
	 
dat.parameter['print_interval']=dat.parameter['max_timesteps']/20
dat.parameter['max_timestep']=dat.parameter['tstop']/dat.parameter['max_timesteps']

dat.start = True
dat.diffusion=[[2.13e-5,     0.e-8],   [2.13e-5,     0.e-8]]
dat.multi={'num_components': 3, 'num_equations': 4, 'num_phases': 2, 'num_secondary_parameters': 8}

# #Set MOPs:
dat.parameter['option'][1] = 1
dat.parameter['option'][7] = 0
dat.parameter['option'][11] = 0
dat.parameter['option'][16] = 4
dat.parameter['option'][19] = 2
dat.parameter['option'][21] = 3

# #Add another rocktype, with relative permeability and capillarity functions & parameters:
r1 = rocktype('SAND ', nad=2, porosity=0.45,density=2650.,permeability = [2.e-12, 2.e-12, 2.e-12],conductivity=2.51,specific_heat=920)
r1.tortuosity=0
dat.grid.add_rocktype(r1)
r1.relative_permeability = {'type': 7, 'parameters': [0.627, 0.045, 1., 0.054]}
r1.capillarity = {'type': 7, 'parameters': [0.627, 0.045, 5.e-4, 1.e8, 1.]}
	
conarea = dx[0] * dy[0]

# #assign rocktype and parameter values:
for blk in dat.grid.blocklist:
    blk.rocktype = r1
    blk.ahtx=conarea


# #Set initial condition:
j=0
while j<50:
    i=0
    while i<80:
        dat.incon[str(dat.grid.blocklist[i+j*100])] = [None, [101.3e3+dat.grid.blocklist[i+j*100].centre[2]*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
        i+=1
    j+=1

j=1
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+20])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*1)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+21])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*1)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=2
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+22])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*2)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+23])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*2)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=3
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+24])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*3)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+25])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*3)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=4
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+26])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*4)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+27])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*4)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=5
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+28])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*5)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+29])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*5)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=6
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+30])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*6)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+31])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*6)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=7
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+32])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*7)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+33])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*7)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=8
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+34])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*8)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+35])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*8)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=9
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+36])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*9)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+37])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*9)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=10
while j<50:
    dat.incon[str(dat.grid.blocklist[j*100+38])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*10)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    dat.incon[str(dat.grid.blocklist[j*100+39])] = [None, [101.3e3+(dat.grid.blocklist.centre[2]-(length_z/nblks_z)*10)*(-1)*liquid_density_kgPm3*dat.parameter['gravity'], 0, 10.01, 13.0]]
    j+=1

j=30
while j<50:
    i=80
    while i<100:
        dat.incon[str(dat.grid.blocklist[i+j*100])] = [None, [101.3e3+(dat.grid.blocklist[i+j*100].centre[2]-length_z/nblks_z*30)*(-1)*brine_density_kgPm3*dat.parameter['gravity'], 1, 10.01, 13.0]]
        i+=1
    j+=1
	
# #deleted block:
j=0
while j<30:
    i=20
    while i<100-2*j:
        dat.grid.delete_block(str(dat.grid.blocklist[20*(j+1)+(j+1)*j]))
        i+=1
    j+=1
	
# # #add generator:
# flow_rate_mmPday=-5
# flow_rate_kgPs=flow_rate_mmPday*conarea*liquid_density_kgPm3*mPmm*dayPs
# gen = t2generator(name = 'INF 1', block = dat.grid.blocklist[0].name,
                  # gx = flow_rate_kgPs, type = 'COM1')
# dat.add_generator(gen)


# #--- write TOUGH2 input file ------------------------------------	
dat.write(dat.title)