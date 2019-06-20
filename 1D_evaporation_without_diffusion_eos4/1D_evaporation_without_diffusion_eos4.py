
from t2data import *
from t2listing import *
import os

#--- set up the model ---------------------------------

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
    {'max_timesteps': 3.e3,
     'max_timestep': 1.e4,
     'timestep': [1000.0],
     'tstop': 3.e3,
     'const_timestep': 1000.,
     'print_interval': 9999.,
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


# --- post-process the output ---------------------------

import matplotlib.pyplot as plt


liq_density_kgPm3=1000
water_molecular_weight=0.018
R_value=8.314
m2mm=1000
day2s=3600*24
T_kelven=273.15

lst = t2listing('1D_evaporation_without_diffusion_eos4.listing')
lst.last()
# #omit boundary blocks from the plot results:
element = [blk.centre[2] for blk in dat.grid.blocklist[:nblks]]
Liq_saturation       = lst.element['SL'][:nblks]
Gas_Pressure         = lst.element['P'][:nblks]
Capillary_Pressure   = lst.element['PCAP'][:nblks]

connection=np.array(element)+0.5*dz[0]
Liquid_flow_raw      = lst.connection['FLO(LIQ.)']/conarea/liq_density_kgPm3*m2mm*day2s
Liquid_flow          =np.insert(Liquid_flow_raw,0, Liquid_flow_raw[-1])
Gas_flow_raw         = lst.connection['FLO(GAS)']/conarea/liq_density_kgPm3*m2mm*day2s
Gas_flow             =np.insert(Gas_flow_raw,0, Gas_flow_raw[-1])
Vap_diffusion        = lst.connection['VAPDIF']/conarea/liq_density_kgPm3*m2mm*day2s

fig=plt.figure()
ax1=plt.subplot(241)
ax1.plot(Gas_Pressure/1000, element,'k-o')
plt.ylabel('z (m)'); plt.xlabel('Gas. Pre. (Kpa)')
#ax1.spines['top'].set_color('red')
plt.ylim(-1.5,0.1)
plt.xlim(np.nanmin(Gas_Pressure/1000),np.nanmax(Gas_Pressure/1000))
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#ax1.set_xscale('log')
ax2=ax1.twiny()
ax2.plot(Capillary_Pressure/1000,element,'r-o')
plt.xlabel('Cap. pre. (Kpa)')
# plt.ylabel('high (m)')
plt.ylim(-1.5,0.1)
plt.xlim(np.nanmin(Capillary_Pressure/1000),np.nanmax(Capillary_Pressure/1000))
#x1.set_xscale('log')
#plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax2.spines['top'].set_color('red')
ax2.xaxis.label.set_color('red')
ax2.tick_params(axis='x', colors='red')	 

plt.subplot(242)
plt.plot(Liq_saturation*100,element,'b-o')
plt.xlabel('Liq. sat. (%)')
# plt.ylabel('high (m)')
plt.ylim(-1.5,0.1)
plt.xlim(np.nanmin(Liq_saturation)*100,np.nanmax(Liq_saturation)*100)

# plt.subplot(243)
# plt.plot(Liq_saturation*100,element,'b-o')
# plt.xlabel('Liq. sat. (%)')
# # plt.ylabel('high (m)')
# plt.ylim(-1.5,0)
# plt.xlim(np.nanmin(Liq_saturation)*100,np.nanmax(Liq_saturation)*100)
		
ax3=plt.subplot(244)
ax3.plot(Gas_flow[:-1],connection,'k-o')
plt.xlabel('Gas Flo. (mm/day)')
# plt.ylabel('high (m)')
plt.ylim(-1.5,0.1) 
plt.xlim(np.nanmin(Gas_flow),np.nanmax(Gas_flow))	
ax4=ax3.twiny()	
ax4.plot(Liquid_flow[:-1],connection,'r-o')
plt.xlabel('Liq. Flo. (mm/day)')
# plt.ylabel('high (m)')
plt.ylim(-1.5,0.1) 
plt.xlim(np.nanmin(Liquid_flow),np.nanmax(Liquid_flow))	
ax4.spines['top'].set_color('red')	
ax4.xaxis.label.set_color('red')
ax4.tick_params(axis='x', colors='red')	 	

fig.suptitle('time: %6.2e s' %lst.time)
plt.rcParams.update({'font.size': 7})
#fig.tight_layout()
plt.savefig('out_'+str(lst.time)+'s.png',dpi=300) 
