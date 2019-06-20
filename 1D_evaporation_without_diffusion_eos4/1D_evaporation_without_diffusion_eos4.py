
from t2data import *
from t2listing import *
import os

# #--- set up the model ---------------------------------

length = 1.5
nblks = 15
dz = [length / nblks] * nblks
dy = dx = [0.1]
geo = mulgrid().rectangular(dx, dy, dz)
geo.write('1D_evaporation_without_diffusion_eos4_geo.dat')

# #Create TOUGH2 input data file:
dat = t2data()
dat.title = '1D_evaporation_without_diffusion_eos4'
dat.grid = t2grid().fromgeo(geo)
dat.parameter.update(
    {'max_timesteps': 1.e3,
     'max_timestep': 1.e4,
     'timestep': [1000.0],
     'tstop': 3.e3,
     'const_timestep': 1000.,
     'print_interval': 1000.,
     'gravity': 9.81,
     'print_level': 2,
     'default_incons': [101.3e3, 10.9999, 20.0, None]})

dat.start = True

# #Set MOPs:
dat.parameter['option'][1] = 1
dat.parameter['option'][7] = 9
dat.parameter['option'][16] = 4
dat.parameter['option'][19] = 2
dat.parameter['option'][21] = 3

# #Set relative permeability and capillarity functions:
#dat.relative_permeability = {'type': 7, 'parameters': [0.627, 0.045, 1., 0.054]}
#dat.capillarity = {'type': 7, 'parameters': [0.627, 0.045, 5.e-4, 1.e5, 1.]}


# #Add another rocktype, with parameters:
r1 = rocktype('SAND ', nad=2, porosity=0.45,density=2650.,permeability = [2.e-12, 2.e-12, 2.e-12])
dat.grid.add_rocktype(r1)
r1.relative_permeability = {'type': 7, 'parameters': [0.627, 0.045, 1., 0.054]}
r1.capillarity = {'type': 7, 'parameters': [0.627, 0.045, 5.e-4, 1.e5, 1.]}

	
r2 = rocktype('BOUND', nad=2,porosity=0.99,density=2650., permeability = [2.e-12, 2.e-12, 2.e-12])
dat.grid.add_rocktype(r2)
r2.relative_permeability = {'type': 7, 'parameters': [0.627, 0.045, 1., 0.054]}
r2.capillarity = {'type': 7, 'parameters': [0.627, 0.045, 5.e-4, 1.e5, 1.]}


# #add boundary condition block at each end:
bvol = 0.0
conarea = dx[0] * dy[0]
condist = 1.e-10


for blk in dat.grid.blocklist:
    blk.rocktype = r1
    blk.ahtx=conarea


b1 = t2block('bdy01', bvol, r2)
b1.volume=1.e50

dat.grid.add_block(b1)
con1 = t2connection([dat.grid.blocklist[0],b1],
                    distance = [0.5*dz[0], condist], area = conarea, direction=3)
dat.grid.add_connection(con1)


# b2 = t2block('bdy02', bvol, dat.grid.rocktype['dfalt'])
# dat.grid.add_block(b2)
# con2 = t2connection([dat.grid.blocklist[nblks-1], b2],
                    # distance = [0.5*dz[nblks-1], condist], area = conarea)
# dat.grid.add_connection(con2)

dat.grid.connectionlist[-1].dircos=-1
dat.grid.blocklist[-1].ahtx=conarea

# #Set initial condition:

for i in range(len(dat.grid.blocklist)):
    dat.incon[str(dat.grid.blocklist[i])] = [None, [101.3e3+500*(2*i+1), 10.0001, 20.0]]
dat.incon['bdy01'] = [None, [101.3e3, 10.9999, 20.0]]

dat.write('1D_evaporation_without_diffusion_eos4.dat')


# #--- run the model ------------------------------------

os.system("tough2 -to 1D_evaporation_without_diffusion_eos4.listing 1D_evaporation_without_diffusion_eos4.dat 4")


# # --- post-process the output ---------------------------

import matplotlib.pyplot as plt
lst = t2listing('1D_evaporation_without_diffusion_eos4.listing')
lst.last()
# #omit boundary blocks from the plot results:
z = [blk.centre[2] for blk in dat.grid.blocklist[:nblks]]
SL = lst.element['SL'][:nblks]

fig=plt.figure()
plt.subplot(241)
plt.plot(SL, z,'o-')
plt.ylabel('z (m)'); plt.xlabel('Liq. saturation')
fig.suptitle('time: %6.2e s' %lst.time)
plt.rcParams.update({'font.size': 7})
#fig.tight_layout()
plt.savefig('out_'+str(lst.time)+'s.png',dpi=300) 
