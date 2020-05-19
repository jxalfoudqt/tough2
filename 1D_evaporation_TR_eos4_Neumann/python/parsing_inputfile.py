import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2listing import *
from t2data    import *
from t2incons  import *
from mpl_toolkits.mplot3d import Axes3D

liquid_density_kgPm3   = 1000
water_molecular_weight = 0.018
R_value                = 8.314
m2mm                   = 1000
day2s                  = 3600*24
T_kelven               = 273.15

title = 'flow.out'

# #--- read TOUGH2 input file ------------------------------------	

t = time.time()
dat = t2data(title)
# dat.grid.write_vtk('sam6_geo.vtu')

elapsed = time.time() - t
print('Parsing output Elapsed: %s minutes' %(elapsed/60))
# #--- plot generated mesh ------------------------------------	
    
#element_coordinate           = np.array([j.centre for j in dat.grid.blocklist])

connection_first_distance    = np.array([blk.distance[0] for blk in dat.grid.connectionlist])
connection_second_distance   = np.array([blk.distance[1] for blk in dat.grid.connectionlist])
ele_depth_m                  = np.cumsum(np.insert(connection_first_distance+connection_second_distance,0,0))
con_depth_m                 = np.cumsum(connection_first_distance+np.insert(connection_second_distance[:-1], 0, 0)) 

# geo = mulgrid().rectangular(element_coordinate[:,0], -2*np.array([element_coordinate[0,1]]), -2*np.array([element_coordinate[0,2]]))
# geo.write_vtk('geom.vtk')


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(element_coordinate[:,0], element_coordinate[:,1], element_coordinate[:,2], s=30, c='r', marker='.')
# ax.scatter(element_coordinate[0,0], element_coordinate[0,1], element_coordinate[0,2], s=10, c='b', marker='.')
# #ax.scatter(element_coordinate[-1,0], element_coordinate[-1,1], element_coordinate[-1,2], s=10, c='b', marker='^')
# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')
# #ax.set_xscale('log')
# fig.suptitle('mesh_element')
# plt.rcParams.update({'font.size': 10})
# #fig.tight_layout()
# plt.savefig("generated_mesh_grid.png",dpi=300) 

# initial_condition=np.array([dat.incon[str(j)][1] for j in dat.grid.blocklist])
# # initial_porosity=np.array([dat.incon[str(j)][0] for j in dat.grid.blocklist])

# fig=plt.figure()
# # ax1=plt.subplot(141)
# # ax1.plot(initial_porosity[:],ele_depth_m  ,'b-')
# # plt.xlabel('Por.')
# # plt.ylabel('x (m)')
# # # plt.ylabel('high (m)')
# # plt.ylim(1.5,-0.1)
# # # plt.xlim(np.nanmin(initial_porosity),np.nanmax(initial_porosity))
# # #ax1.set_yscale('log')

# ax2=plt.subplot(131)
# ax2.plot(initial_condition[:,0]/1000,ele_depth_m  ,'b-')
# plt.xlabel('Gas Pre. (Kpa)')
# # plt.ylabel('high (m)')
# plt.ylim(1.5,-0.1)
# # plt.xlim(np.nanmin(Liq_saturation)*100,np.nanmax(Liq_saturation)*100)
# #plt.yscale('log')

# ax3=plt.subplot(132)
# ax3.plot(100-(initial_condition[:,1]-10)*100,ele_depth_m  ,'b-')
# plt.xlabel('Liq. Sat. (%)')
# # plt.ylabel('high (m)')
# plt.ylim(1.5,-0.1)
# # plt.xlim(np.nanmin(Gas_flow),np.nanmax(Gas_flow))	
# # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
# #ax3.set_yscale('log')

# ax4=plt.subplot(133)
# ax4.plot(initial_condition[:,2],ele_depth_m  ,'b-')
# plt.xlabel('Tem. (Degree)')
# # plt.ylabel('high (m)')
# plt.ylim(1.5,-0.1)
# plt.xlim(12.95, 13.05)	
# # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
# #ax4.set_yscale('log')

# plt.rcParams.update({'font.size': 7})
# # fig.tight_layout()
# plt.savefig('figure/output_100.png',dpi=300) 


dat.grid.rocktype.pop('dfalt', None)
saturation=np.logspace(-10,0,150)
capillary_pressure=np.empty(len(saturation))
capillary_pressure[:]=np.nan
# #--- plot SWCC and Cap. Pre. ------------------------------------	
for i in dat.grid.rocktype:
    if i== 'SAND ':
        capillarity_parameter=dat.grid.rocktype[str(i)].capillarity['parameters']
        capillarity_type=dat.grid.rocktype[str(i)].capillarity['type']
        relative_permeability_parameter=dat.grid.rocktype[str(i)].relative_permeability['parameters']
        relative_permeability_type=dat.grid.rocktype[str(i)].relative_permeability['type']
        
        fig=plt.figure()
        ax3=plt.subplot(121)
        if  capillarity_type==1:
            capillary_pressure=1*capillarity_parameter[0]*(capillarity_parameter[2]-saturation)/(capillarity_parameter[2]-capillarity_parameter[1])
            capillary_pressure[saturation<=capillarity_parameter[1]]=1*capillarity_parameter[0]
            capillary_pressure[saturation>=capillarity_parameter[2]]=0
     
        if  capillarity_type==7:
            lamda=capillarity_parameter[0]
            liquid_residual_saturation=capillarity_parameter[1]
            P_zero_point=1./capillarity_parameter[2]	
            P_zero=np.linspace(P_zero_point-1500,P_zero_point+1500,5)
            Pressure_max=capillarity_parameter[3]		
            saturated_liquid_saturation=capillarity_parameter[4]
            saturation2=np.linspace(0,liquid_residual_saturation,50)
            #saturation1=np.linspace(liquid_residual_saturation,saturated_liquid_saturation,100)
            saturation1=np.linspace(liquid_residual_saturation+1.e-5,1,100)
            #saturation2=np.linspace(0,liquid_residual_saturation,100)
            S_star=(saturation1-liquid_residual_saturation)/(saturated_liquid_saturation-liquid_residual_saturation)
            capillary_pressure1=np.array([1*P_zero[j]*(S_star**(-1/lamda)-1)**(1-lamda) for j in range(len(P_zero))])    
            SBAR = 1.e-5/(saturated_liquid_saturation-liquid_residual_saturation)
            PCE = np.array([P_zero[j]*(SBAR**(-1/lamda)-1)**(1-lamda) for j in range(len(P_zero))])
            ENVG =1./(1-lamda)
            PCSLOPE = np.array([-P_zero[j]/lamda/ENVG/(saturated_liquid_saturation-liquid_residual_saturation)*(SBAR**(-1/lamda)-1)**((1-ENVG)/ENVG)*SBAR**(-(1+lamda)/lamda) for j in range(len(P_zero))])
            capillary_pressure2=np.array([PCE[j]+PCSLOPE[j]*(saturation2-liquid_residual_saturation-1.e-5) for j in range(len(P_zero))])
        j=2
        ax3.plot(saturation1,capillary_pressure1[j],'r.-',saturation2,capillary_pressure2[j],'.-')
        plt.text(0.2, 10.e4*10**(j/1.5),'P_zero='+str(P_zero[j]))
        plt.xlabel('saturation')
        plt.ylabel('capillary_pressure')
        plt.ylim(10,1.e10)
        plt.xlim(-0.1,1.1)
        #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax3.set_yscale('log')

        # for j in range(len(P_zero)):
            # ax3.plot(saturation1,capillary_pressure1[j],'.-',saturation2,capillary_pressure2[j],'.-')
            # plt.text(0.2, 10.e4*10**(j/1.5),'P_zero='+str(P_zero[j])+'; PCE=10**'+str(round(np.log10(PCE[j]),2))+'; PCSLOPE=-10**'+str(round(np.log10(-1*PCSLOPE[j]),2)))
        # plt.xlabel('saturation')
        # plt.ylabel('capillary_pressure')
        # plt.ylim(10,1.e10)
        # plt.xlim(-0.1,1.1)
        # #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        # ax3.set_yscale('log')
     	
        ax1=plt.subplot(122)
        if  relative_permeability_type==1:
            saturation=np.array([relative_permeability_parameter[0],relative_permeability_parameter[2]])
            liquid_relative_permeability=np.array([0,1])
            gas_relative_permeability=np.array([1,0])
     
        if  relative_permeability_type==7:
            lamda=relative_permeability_parameter[0]
            liquid_residual_saturation=relative_permeability_parameter[1]
            saturated_liquid_saturation=relative_permeability_parameter[2]
            gas_residual_saturation=relative_permeability_parameter[3]
            saturation=np.append(saturation1,saturation2)          
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
        # ax2=ax1.twinx()
        # ax2.plot(saturation,gas_relative_permeability,'r-o',)
        # plt.xlabel('saturation')
        # plt.ylabel('gas_relative_permeability')
        # plt.ylim(0,1)
        #plt.xlim()
        #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        #ax2.set_yscale('log')
        # ax2.spines['right'].set_color('red')
        # ax2.yaxis.label.set_color('red')
        # ax2.tick_params(axis='y', colors='red')	
        	
        fig.suptitle(dat.grid.rocktype[str(i)])
        plt.rcParams.update({'font.size': 10})
        #fig.tight_layout()
        plt.savefig("figure/Capillary_&_SWCC_for_"+str(i)+".png",dpi=300) 