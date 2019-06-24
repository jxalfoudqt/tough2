
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


# # --- post-process the output ---------------------------
lst = t2listing('sam6_0.listing')
dat=t2data('sam6')
nblks=-1
i=0
while i<lst.num_times:
    
    element              = [blk.centre[0] for blk in dat.grid.blocklist[:]]
    Liq_saturation       = lst.element['SL'][:]
    Gas_Pressure         = lst.element['P'][:]
    Capillary_Pressure   = lst.element['PCAP'][:]
    connection_change    = [blk.distance[1] for blk in dat.grid.connectionlist[:]]
    connection           = np.array(element[1:])-connection_change
    Liquid_flow_raw      = lst.connection['FLO(LIQ.)']/ dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
    Liquid_flow          = np.insert(Liquid_flow_raw,0, Liquid_flow_raw[-1])
    Gas_flow_raw         = lst.connection['FLO(GAS)']/ dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
    Gas_flow             = np.insert(Gas_flow_raw,0, Gas_flow_raw[-1])
    Vap_diffusion        = lst.connection['VAPDIF']/ dat.grid.connectionlist[0].area/liq_density_kgPm3*m2mm*day2s
    
    fig=plt.figure()
    ax1=plt.subplot(141)
    ax1.plot(Gas_Pressure/1000, element,'b1-')
    plt.ylabel('x (m)'); plt.xlabel('Gas. Pre. (Kpa)')
    #ax1.spines['top'].set_color('red')
    plt.ylim(7,0)
    plt.xlim(np.nanmin(Gas_Pressure/1000),np.nanmax(Gas_Pressure/1000))
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #ax1.set_xscale('log')
    ax2=ax1.twiny()
    ax2.plot(Capillary_Pressure/1000,element,'r1-')
    plt.xlabel('Cap. pre. (Kpa)')
    # plt.ylabel('high (m)')
    plt.ylim(7,0)
    plt.xlim(np.nanmin(Capillary_Pressure/1000),np.nanmax(Capillary_Pressure/1000))
    #ax1.set_xscale('log')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax2.spines['top'].set_color('red')
    ax2.xaxis.label.set_color('red')
    ax2.tick_params(axis='x', colors='red')	 
    
    plt.subplot(142)
    plt.plot(Liq_saturation*100,element,'b1-')
    plt.xlabel('Liq. sat. (%)')
    # plt.ylabel('high (m)')
    plt.ylim(7,0)
    plt.xlim(np.nanmin(Liq_saturation)*100,np.nanmax(Liq_saturation)*100)
    
    ax3=plt.subplot(143)
    ax3.plot(Liquid_flow_raw,connection,'b1-')
    plt.xlabel('Liq Flo. (mm/day)')
    # plt.ylabel('high (m)')
    plt.ylim(7,0)
    plt.xlim(np.nanmin(Liquid_flow_raw),np.nanmax(Liquid_flow_raw))	
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
	
    ax3=plt.subplot(144)
    ax3.plot(Gas_flow_raw,connection,'b1-')
    plt.xlabel('Gas Flo. (mm/day)')
    # plt.ylabel('high (m)')
    plt.ylim(7,0)
    plt.xlim(np.nanmin(Gas_flow_raw),np.nanmax(Gas_flow_raw))	
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))	
    # ax4=ax3.twiny()	
    # ax4.plot(Liquid_flow_raw,connection,'r1-')
    # plt.xlabel('Liq. Flo. (mm/day)')
    # # plt.ylabel('high (m)')
    # plt.ylim(7,0)
    # plt.xlim(np.nanmin(Liquid_flow_raw),np.nanmax(Liquid_flow_raw))	
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    # ax4.spines['top'].set_color('red')	
    # ax4.xaxis.label.set_color('red')
    # ax4.tick_params(axis='x', colors='red')	 	
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))    
    fig.suptitle('time: %6.2e s' %lst.time)
    plt.rcParams.update({'font.size': 7})
    #fig.tight_layout()
    plt.savefig('output_'+str(i+101)+'.png',dpi=300) 
    lst.next()
    i+=1

#plt.close('all')