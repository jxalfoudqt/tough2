
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
Pa2Kpa=1000

# --- post-process the output ---------------------------
lst = t2listing('sam6_0.listing')
dat=t2data('sam6')

element_coordinate         = np.array([j.centre for j in dat.grid.blocklist])
connection_first_distance  = np.array([blk.distance[0] for blk in dat.grid.connectionlist])
connection_second_distance = np.array([blk.distance[1] for blk in dat.grid.connectionlist])
element_location_raw       = connection_first_distance+connection_second_distance
element_location_new       = np.insert(element_location_raw, 0, element_coordinate[1,0]-element_location_raw[0])
element_value              = np.cumsum(element_location_new)    
connection_location_raw    = connection_first_distance[1:]+connection_second_distance[:-1]
connection_location_new    = np.insert(connection_location_raw, 0, element_coordinate[1,0]-connection_second_distance[0])
connection_value           = np.cumsum(connection_location_new) 
element_volume             = np.array([blk.volume for blk in dat.grid.blocklist[1:-1]])

Gas_Density                = np.array([lst.history(('e',lst.element.row_name[i],'DG'))[1] for i in range(lst.element.num_rows)])
Liq_Density                = np.array([lst.history(('e',lst.element.row_name[i],'DL'))[1] for i in range(lst.element.num_rows)])
Gas_saturation             = np.array([lst.history(('e',lst.element.row_name[i],'SG'))[1] for i in range(lst.element.num_rows)])
Liq_saturation             = np.array([lst.history(('e',lst.element.row_name[i],'SL'))[1] for i in range(lst.element.num_rows)])
Gas_Pressure               = np.array([lst.history(('e',lst.element.row_name[i],'P'))[1] for i in range(lst.element.num_rows)])
Capillary_Pressure         = np.array([lst.history(('e',lst.element.row_name[i],'PCAP'))[1] for i in range(lst.element.num_rows)])
Temperature                = np.array([lst.history(('e',lst.element.row_name[i],'T'))[1] for i in range(lst.element.num_rows)])
Liquid_flow_raw            = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(LIQ.)'))[1] for i in range(lst.connection.num_rows)])/dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
Gas_flow_raw               = np.array([lst.history(('c',lst.connection.row_name[i],'FLO(GAS)'))[1] for i in range(lst.connection.num_rows)])/dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
Liquid_flow_topsoil        = Liquid_flow_raw[0]
Gas_flow_topsoil           = Gas_flow_raw[0]

Gas_mass=np.empty(lst.num_times)
Gas_mass[:]=np.nan   
liquid_mass=np.empty(lst.num_times)
liquid_mass[:]=np.nan
i=0
while i<lst.num_times:
    Gas_mass[i]     = np.sum(element_volume*Gas_Density[1:-1,i]*Gas_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity,axis=0)
    liquid_mass[i]  = np.sum(element_volume*Liq_Density[1:-1,i]*Liq_saturation[1:-1,i]*dat.grid.rocktype['MATRI'].porosity,axis=0)
    i+=1

i=0
while i<lst.num_times:

    # Liquid_flow_raw            = lst.connection['FLO(LIQ.)']/dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
    # Liquid_flow                = np.insert(Liquid_flow_raw,0, Liquid_flow_raw[-1])
    # Gas_flow_raw               = lst.connection['FLO(GAS)']/dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
    # Gas_flow                   = np.insert(Gas_flow_raw,0, Gas_flow_raw[-1])

    fig=plt.figure()
    ax1=plt.subplot(242)
    ax1.plot(Gas_Pressure[:,i]/Pa2Kpa, element_value,'b1-')
    plt.xlabel('Gas. Pre. (Kpa)')
    #ax1.spines['top'].set_color('red')
    plt.ylim(7,1.5)
    plt.xlim(50,400)
    #plt.xlim(np.min(Gas_Pressure/Pa2Kpa),np.max(Gas_Pressure/Pa2Kpa))
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #ax1.set_yscale('log')
    ax2=ax1.twiny()
    ax2.plot(Capillary_Pressure[:,i]/Pa2Kpa,element_value,'r1-')
    plt.xlabel('Cap. pre. (Kpa)')
    # plt.ylabel('high (m)')
    plt.ylim(7,1.5)
    plt.xlim(-5.e4,1.e3)
    #plt.xlim(np.min(Capillary_Pressure/Pa2Kpa),np.max(Capillary_Pressure/Pa2Kpa))
    #ax2.set_yscale('log')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax2.spines['top'].set_color('red')
    ax2.xaxis.label.set_color('red')
    ax2.tick_params(axis='x', colors='red')	 
    
    ax11=plt.subplot(241)
    ax11.plot(Liq_saturation[:,i]*100,element_value,'b1-')
    plt.ylabel('x (m)')
    plt.xlabel('Liq. sat. (%)')
    # plt.ylabel('high (m)')
    plt.ylim(7,1.5)
    plt.xlim(-5,105)
    #ax11.set_yscale('log')   
	
    ax13=plt.subplot(244)
    ax13.plot(Temperature[:,i],element_value,'b1-')
    plt.xlabel('Tem. (Degree)')
    # plt.ylabel('high (m)')
    plt.ylim(7,1.5)
    plt.xlim(12.95,13.05)
    #plt.xlim(np.min(Temperature),np.max(Temperature))
    #ax13.set_yscale('log')
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
	
    ax3=plt.subplot(243)
    ax3.plot(Gas_flow_raw[:,i],connection_value,'b1-')
    plt.xlabel('Gas Dar. vel. (mm/day)')
    # plt.ylabel('high (m)')
    plt.ylim(7,1.5)
    plt.xlim(-1.2e-1,1.e-2)
    #plt.xlim(np.min(Gas_flow_raw),np.max(Gas_flow_raw))
    #ax3.set_yscale('log')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))	
    ax4=ax3.twiny()	
    ax4.plot(Liquid_flow_raw[:,i],connection_value,'r1-')
    plt.xlabel('Liq. Dar. vel. (mm/day)')
    # plt.ylabel('high (m)')
    plt.ylim(7,1.5)
    plt.xlim(-5.,1.1e2)
    #plt.xlim(np.nanmin(Liquid_flow_raw),np.nanmax(Liquid_flow_raw))	
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax4.spines['top'].set_color('red')	
    ax4.xaxis.label.set_color('red')
    ax4.tick_params(axis='x', colors='red')	 	
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
	
    ax5=plt.subplot(413)
    ax5.plot(lst.times[:i+1],Gas_mass[:i+1],'k1-')
    plt.ylabel('Gas. mass (kg)')
    #plt.xlabel('Time (s)')
    plt.ylim(0,5.e-2)
    #plt.ylim(np.min(Gas_mass),np.max(Gas_mass))
    plt.xlim(0,np.max(lst.times))
    ax5.set_xscale('log')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0),useLocale=0)
    #ax1.spines['left'].set_color('blue')
    ax6 = ax5.twinx() 
    ax6.plot(lst.times[:i+1],liquid_mass[:i+1],'r1-',)
    plt.ylim(1300,1340)
    #plt.ylim(np.min(liquid_mass),np.max(liquid_mass))
    plt.xlim(0,np.max(lst.times))
    plt.ylabel('Liq. mass (kg)')
    #plt.xlabel('Time (s)')
    ax6.set_xscale('log')
    ax6.spines['right'].set_color('red')
    ax6.yaxis.label.set_color('red')
    #ax6.tick_params(axis='y', colors='red')	 	
	
    ax7=plt.subplot(414)
    ax7.plot(lst.times[:i+1],Gas_flow_topsoil[:i+1],'k1-')
    plt.ylabel('Gas Dar. vel. (mm/day)')
    plt.xlabel('Time (s)')
    plt.ylim(-1.1e-1,0.1e-1)
    #plt.ylim(np.min(Gas_flow_topsoil),np.max(Gas_flow_topsoil))
    plt.xlim(0,np.max(lst.times))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax7.set_xscale('log')
    ax8 = ax7.twinx() 
    ax8.plot(lst.times[:i+1],Liquid_flow_topsoil[:i+1],'r1-',)
    plt.ylim(-1.e1,1.1e2)
    #plt.ylim(np.min(Liquid_flow_topsoil),np.max(Liquid_flow_topsoil))
    plt.xlim(0,np.max(lst.times))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.ylabel('Liq. Dar. vel. (mm/day)')
    plt.xlabel('Time (s)')
    ax8.set_xscale('log')
    ax8.spines['right'].set_color('red')
    ax8.yaxis.label.set_color('red')
    ax8.tick_params(axis='y', colors='red')		
	
    fig.suptitle('time: %6.2e s' %lst.times[i])
    plt.rcParams.update({'font.size': 7})
    #fig.tight_layout()
    plt.savefig('figure/output_'+str(i+101)+'.png',dpi=300) 
    i+=1

#plt.close('all')