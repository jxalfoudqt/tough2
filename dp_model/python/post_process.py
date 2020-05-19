
from t2listing import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

if not os.path.exists('figure'):
        os.makedirs('figure')

x1=np.arange(np.min(element_value_x),np.max(element_value_x)+0.5,0.5)
y1=np.arange(np.min(element_value_z),np.max(element_value_z)+0.25,0.25)	
xi,yi=np.meshgrid(x1,y1)
	
i=0
cm = plt.cm.get_cmap('cool')
while i<lst.num_times:
    #fig=plt.figure()
    fig=plt.figure(figsize=(20,14))
    fig.subplots_adjust(hspace=.30,wspace=.2)
    fig.subplots_adjust(left=0.07, right=0.93, top=0.93, bottom=0.05)

    gas_pressure_pa_grid=griddata((element_value_x,element_value_z), gas_pressure_pa[:-10,i],(xi,yi),method='linear')
    ax1 = plt.subplot(311)
    cs1 = ax1.contourf(x1, y1, gas_pressure_pa_grid/1000., 10, cmap=cm)
    plt.colorbar(cs1)
    plt.xlabel('x (m)')
    plt.ylabel('z (m)')
    plt.yticks(np.arange(-4, -0.5, 1))
    plt.title('gas_pressure_pa (kpa)')
	
    # capillary_pressure_pa_grid=griddata((element_value_x,element_value_z), capillary_pressure_pa[:-2,i],(xi,yi),method='linear')
    # ax1 = plt.subplot(322)
    # cs1 = ax1.contourf(x1, y1, capillary_pressure_pa_grid/1000., 10, cmap=cm)
    # plt.colorbar(cs1)
    # plt.xlabel('x (m)'),0.e-8
    # plt.ylabel('z (m)')
    # plt.yticks(np.arange(-0.4, -0.05, 0.1))
    # plt.title('capillary_pressure (kpa)')
    
    levels_3=np.linspace(0,1,11)
    liq_saturation_grid=griddata((element_value_x,element_value_z), liq_saturation[:-10,i],(xi,yi),method='linear')
    ax1 = plt.subplot(312)
    cs1 = ax1.contourf(x1, y1, liq_saturation_grid, levels_3, cmap=cm)
    plt.colorbar(cs1)
    plt.xlabel('x (m)')
    plt.ylabel('z (m)')
    plt.yticks(np.arange(-4, -0.5, 1))
    plt.title('liq_saturation (%)')
	
    brine_mass_fraction_in_liq_grid=griddata((element_value_x,element_value_z), brine_mass_fraction_in_liq[:-10,i],(xi,yi),method='linear')
    brine_mass_fraction_in_liq_grid[brine_mass_fraction_in_liq_grid>1]=1
    brine_mass_fraction_in_liq_grid[brine_mass_fraction_in_liq_grid<0]=0
    ax1 = plt.subplot(313)
    cs1 = ax1.contourf(x1, y1, brine_mass_fraction_in_liq_grid, levels_3, cmap=cm)
    plt.colorbar(cs1)
    plt.xlabel('x (m)')
    plt.ylabel('z (m)')
    plt.yticks(np.arange(-4, -0.5, 1))
    plt.title('brine_mass_fraction (%)')



	
    fig.suptitle('time: %6.2e s' %lst.times[i])
    plt.rcParams.update({'font.size':12})
    #fig.tight_layout()
    plt.savefig('figure/output_'+str(i+101)+'.png',dpi=300) 
    i+=9

#plt.close('all')