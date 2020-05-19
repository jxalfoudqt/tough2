
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from t2incons import *
from mpl_toolkits.mplot3d import Axes3D

liquid_density_kgPm3=1000
brine_density_kgPm3=1185.1
water_molecular_weight=0.018
R_value=8.314
m2mm=1000
day2s=3600*24
T_kelven=273.15

# #--- read TOUGH2 input file ------------------------------------	
dat = t2data('rf1')

# #--- plot generated mesh ------------------------------------	
if dat.meshmaker[0][0]=='xyz':
    length_x = dat.meshmaker[0][1][1]['del']*dat.meshmaker[0][1][1]['no']
    nblks_x = dat.meshmaker[0][1][1]['no']
    length_y = dat.meshmaker[0][1][2]['del']*dat.meshmaker[0][1][2]['no']
    nblks_y = dat.meshmaker[0][1][2]['no']
    length_z = dat.meshmaker[0][1][3]['del']*dat.meshmaker[0][1][3]['no']
    nblks_z = dat.meshmaker[0][1][3]['no']
    dx = [length_x / nblks_x] * nblks_x
    dy = [length_y / nblks_y] * nblks_y
    dz = [length_z / nblks_z] * nblks_z
    geo = mulgrid().rectangular(dx, dy, dz)
    dat.grid = t2grid().fromgeo(geo)

element_coordinate           = np.array([j.centre for j in dat.grid.blocklist])

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(element_coordinate[:,0], element_coordinate[:,1], element_coordinate[:,2], s=90, c='r', marker='s')
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# fig.suptitle('mesh_element')
# plt.rcParams.update({'font.size': 10})
# #fig.tight_layout()
# plt.savefig("generated_mesh_grid.png",dpi=300) 

i=1
while i<nblks_z+1:
    j=1
    while j<nblks_y+1:
        k=1
        while k<nblks_x+1:
            dat.grid.blocklist[(k-1)+(j-1)*5+(i-1)*5*5]='A'+str(i)+str(j)+str(0)+str(k)
            k+=1
        j+=1
    i+=1


# for i in range(len(dat.grid.blocklist)):
    # dat.incon[str(dat.grid.blocklist[i])] = [None, dat.parameter['default_incons']]
	
# for i in range(5):
    # dat.incon['A110'+str(i+1)] = [None, incon_origin['A1101'][1]]
	
# initial_condition=np.array([dat.incon[str(j)][1] for j in dat.grid.blocklist])
# initial_porosity=np.array([dat.incon[str(j)][0] for j in dat.grid.blocklist])

# fig=plt.figure()
# ax1=plt.subplot(141)
# ax1.plot(initial_porosity[:],element_value,'b-')
# plt.xlabel('Por.')
# plt.ylabel('x (m)')
# # plt.ylabel('high (m)')
# plt.ylim(7,1.5)
# # plt.xlim(np.nanmin(initial_porosity),np.nanmax(initial_porosity))
# #ax1.set_yscale('log')

# ax2=plt.subplot(142)
# ax2.plot(initial_condition[:,0]/1000,element_value,'b-')
# plt.xlabel('Gas Pre. (Kpa)')
# # plt.ylabel('high (m)')
# plt.ylim(7,1.5)
# # plt.xlim(np.nanmin(Liq_saturation)*100,np.nanmax(Liq_saturation)*100)
# #plt.yscale('log')

# ax3=plt.subplot(143)
# ax3.plot(100-initial_condition[1:,1]*100,element_value[1:],'b-')
# plt.xlabel('Liq. Sat. (%)')
# # plt.ylabel('high (m)')
# plt.ylim(7,1.5)
# # plt.xlim(np.nanmin(Gas_flow),np.nanmax(Gas_flow))	
# # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
# #ax3.set_yscale('log')

# ax4=plt.subplot(144)
# ax4.plot(initial_condition[:,2]/1000,element_value,'b-')
# plt.xlabel('Air Pre. (%)')
# # plt.ylabel('high (m)')
# plt.ylim(7,1.5)
# # plt.xlim(np.nanmin(Gas_flow),np.nanmax(Gas_flow))	
# # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
# #ax4.set_yscale('log')

# plt.rcParams.update({'font.size': 7})
# # fig.tight_layout()
# plt.savefig('figure/output_100.png',dpi=300) 


# dat.grid.rocktype.pop('dfalt', None)
# saturation=np.linspace(0,1,100)
# capillary_pressure=np.empty(len(saturation))
# capillary_pressure[:]=np.nan
# # #--- plot SWCC and Cap. Pre. ------------------------------------	
# for i in dat.grid.rocktype:
    # capillarity_parameter=dat.grid.rocktype[str(i)].capillarity['parameters']
    # capillarity_type=dat.grid.rocktype[str(i)].capillarity['type']
    # relative_permeability_parameter=dat.grid.rocktype[str(i)].relative_permeability['parameters']
    # relative_permeability_type=dat.grid.rocktype[str(i)].relative_permeability['type']
    
    # fig=plt.figure()
    # ax3=plt.subplot(211)
    # if  capillarity_type==1:
        # capillary_pressure=-1*capillarity_parameter[0]*(capillarity_parameter[2]-saturation)/(capillarity_parameter[2]-capillarity_parameter[1])
        # capillary_pressure[saturation<=capillarity_parameter[1]]=-1*capillarity_parameter[0]
        # capillary_pressure[saturation>=capillarity_parameter[2]]=0

    # if  capillarity_type==7:
        # lamda=capillarity_parameter[0]
        # liquid_residual_saturation=capillarity_parameter[1]
        # P_zero=1./capillarity_parameter[2]	
        # Pressure_max=capillarity_parameter[3]		
        # saturated_liquid_saturation=capillarity_parameter[4]
        # S_star=(saturation-liquid_residual_saturation)/(saturated_liquid_saturation-liquid_residual_saturation)
        # capillary_pressure=1*P_zero*(S_star**(-1/lamda)-1)**(1-lamda)

		
    # ax3.plot(saturation,capillary_pressure,'k-o',)
    # plt.xlabel('saturation')
    # plt.ylabel('capillary_pressure (LOG)')
    # #plt.ylim(1.5,-0.1)
    # #plt.xlim()
    # #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    # #ax3.set_yscale('log')
 	
    # ax1=plt.subplot(212)
    # if  relative_permeability_type==1:
        # saturation=np.array([relative_permeability_parameter[0],relative_permeability_parameter[2]])
        # liquid_relative_permeability=np.array([0,1])
        # gas_relative_permeability=np.array([1,0])

    # if  relative_permeability_type==7:
        # lamda=relative_permeability_parameter[0]
        # liquid_residual_saturation=relative_permeability_parameter[1]
        # saturated_liquid_saturation=relative_permeability_parameter[2]
        # gas_residual_saturation=relative_permeability_parameter[3]
        # S_star=(saturation-liquid_residual_saturation)/(saturated_liquid_saturation-liquid_residual_saturation)
        # S_bar=(saturation-liquid_residual_saturation)/(1-gas_residual_saturation-liquid_residual_saturation)
        # liquid_relative_permeability=S_star**0.5*(1-(1-S_star**(1/lamda))**lamda)**2
        # liquid_relative_permeability[saturation>=saturated_liquid_saturation]=1
        # gas_relative_permeability=(1-S_bar)**2*(1-S_bar**2)
        # if gas_residual_saturation==0:
            # gas_relative_permeability=1-liquid_relative_permeability

    # ax1.plot(saturation,liquid_relative_permeability,'k-o',)
    # plt.xlabel('saturation')
    # plt.ylabel('liquid_relative_permeability)')
    # plt.ylim(0,1)
    # #plt.xlim()
    # #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    # #ax1.set_yscale('log')
    # ax2=ax1.twinx()
    # ax2.plot(saturation,gas_relative_permeability,'r-o',)
    # plt.xlabel('saturation')
    # plt.ylabel('gas_relative_permeability')
    # plt.ylim(0,1)
    # #plt.xlim()
    # #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    # #ax2.set_yscale('log')
    # ax2.spines['right'].set_color('red')
    # ax2.yaxis.label.set_color('red')
    # ax2.tick_params(axis='y', colors='red')	
    	
    # fig.suptitle(dat.grid.rocktype[str(i)])
    # plt.rcParams.update({'font.size': 10})
    # #fig.tight_layout()
    # plt.savefig("Capillary_&_SWCC_for_"+str(i)+".png",dpi=300)