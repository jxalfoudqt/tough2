
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

# #--- read TOUGH2 input file ------------------------------------	
dat = t2data('1D_evaporation_without_diffusion_eos4.dat')
dat.grid.rocktype.pop('dfalt', None)

saturation=np.linspace(0,1,100)
capillary_pressure=np.empty(len(saturation))
capillary_pressure[:]=np.nan
# #--- plot SWCC and Cap. Pre. ------------------------------------	
for i in dat.grid.rocktype:
    capillarity_parameter=dat.grid.rocktype[str(i)].capillarity['parameters']
    capillarity_type=dat.grid.rocktype[str(i)].capillarity['type']
    relative_permeability_parameter=dat.grid.rocktype[str(i)].relative_permeability['parameters']
    relative_permeability_type=dat.grid.rocktype[str(i)].relative_permeability['type']
    
    fig=plt.figure()
    ax3=plt.subplot(211)
    if  capillarity_type==1:
        capillary_pressure=-1*capillarity_parameter[0]*(capillarity_parameter[2]-saturation)/(capillarity_parameter[2]-capillarity_parameter[1])
        capillary_pressure[saturation<=capillarity_parameter[1]]=-1*capillarity_parameter[0]
        capillary_pressure[saturation>=capillarity_parameter[2]]=0

    if  capillarity_type==7:
        lamda=capillarity_parameter[0]
        liquid_residual_saturation=capillarity_parameter[1]
        P_zero=1./capillarity_parameter[2]	
        Pressure_max=capillarity_parameter[3]		
        saturated_liquid_saturation=capillarity_parameter[4]
        S_star=(saturation-liquid_residual_saturation)/(saturated_liquid_saturation-liquid_residual_saturation)
        capillary_pressure=1*P_zero*(S_star**(-1/lamda)-1)**(1-lamda)

		
    ax3.plot(saturation,capillary_pressure,'k-o',)
    plt.xlabel('saturation')
    plt.ylabel('capillary_pressure (LOG)')
    #plt.ylim(1.5,-0.1)
    #plt.xlim()
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #ax3.set_yscale('log')
 	
    ax1=plt.subplot(212)
    if  relative_permeability_type==1:
        saturation=np.array([relative_permeability_parameter[0],relative_permeability_parameter[2]])
        liquid_relative_permeability=np.array([0,1])
        gas_relative_permeability=np.array([1,0])

    if  relative_permeability_type==7:
        lamda=relative_permeability_parameter[0]
        liquid_residual_saturation=relative_permeability_parameter[1]
        saturated_liquid_saturation=relative_permeability_parameter[2]
        gas_residual_saturation=relative_permeability_parameter[3]
        S_star=(saturation-liquid_residual_saturation)/(saturated_liquid_saturation-liquid_residual_saturation)
        S_bar=(saturation-liquid_residual_saturation)/(1-gas_residual_saturation-liquid_residual_saturation)
        liquid_relative_permeability=S_star**0.5*(1-(1-S_star**(1/lamda))**lamda)**2
        liquid_relative_permeability[saturation>=saturated_liquid_saturation]=1
        gas_relative_permeability=(1-S_bar)**2*(1-S_bar**2)
        if gas_residual_saturation==0:
            gas_relative_permeability=1-liquid_relative_permeability
    
    ax1.plot(saturation,liquid_relative_permeability,'k-o',)
    plt.xlabel('saturation')
    plt.ylabel('liquid_relative_permeability)')
    plt.ylim(0,1)
    #plt.xlim()
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #ax1.set_yscale('log')
    ax2=ax1.twinx()
    ax2.plot(saturation,gas_relative_permeability,'r-o',)
    plt.xlabel('saturation')
    plt.ylabel('gas_relative_permeability')
    plt.ylim(0,1)
    #plt.xlim()
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #ax2.set_yscale('log')
    ax2.spines['right'].set_color('red')
    ax2.yaxis.label.set_color('red')
    ax2.tick_params(axis='y', colors='red')	
    	
    fig.suptitle(dat.grid.rocktype[str(i)])
    plt.rcParams.update({'font.size': 10})
    #fig.tight_layout()
    plt.savefig("Capillary_&_SWCC_for_"+str(i)+".png",dpi=300) 
	
	
# # #--- plot generated mesh ------------------------------------	
    
# element_location=np.array([j.centre for j in dat.grid.blocklist])

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(element_location[:,0], element_location[:,1], element_location[:,2], s=60, c='r', marker='s')
# #ax.scatter(element_location[0,0], element_location[0,1], element_location[0,2], s=10, c='b', marker='v')
# ax.scatter(element_location[-1,0], element_location[-1,1], element_location[-1,2], s=10, c='b', marker='^')
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# fig.suptitle('mesh_element')
# plt.rcParams.update({'font.size': 10})
# #fig.tight_layout()
# plt.savefig("generated_mesh_grid.png",dpi=300) 