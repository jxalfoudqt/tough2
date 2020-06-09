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

# # delete existing png to avoid old png mixing with new ones
if os.path.exists('figure'):
    fig_path  = os.path.join(os.getcwd(),'figure')
    fig_files = os.listdir(fig_path)
    count=0
    for item in fig_files:
        if item.endswith(".png"):
            count+=1
            os.remove(os.path.join( fig_path , item))
    print("Existing "+ str(count)+ " png file" + " deleted\n")
else:
    print("figure directory does not exist and created.\n")
    os.makedirs('figure')

# # plotting results
x1               = np.arange(min(element_value_x),length_x+length_x/nblks_x,length_x/nblks_x)
z1               = -1*np.arange(-1*max(element_value_z),length_z+length_z/nblks_z,length_z/nblks_z)
xi,zi            = np.meshgrid(x1,z1)
x1_flux          = np.arange(min(element_value_x)+length_x/nblks_x*0.5,length_x,length_x/nblks_x)
z1_flux          = -1*np.arange(-1*max(element_value_z)+length_z/nblks_z/2,length_z,length_z/nblks_z)
xi_flux,zi_flux  = np.meshgrid(x1_flux,z1_flux)

i=0
while i<lst.num_times:
    print("plotting " + str(i) + " / " + str(lst.num_times) + " result\n")
    # fig=plt.figure(figsize=(14,20))
    # fig.subplots_adjust(hspace=.30,wspace=.2)
    # fig.subplots_adjust(left=0.07, right=0.93, top=0.93, bottom=0.05)
    fig=plt.figure()

    gas_pressure_pa_grid=griddata((element_value_x,element_value_z),
	                                            gas_pressure_pa[:,i]/1000,(xi,zi),method='linear')
    level_1=np.linspace(np.nanmin(gas_pressure_pa_grid),np.nanmax(gas_pressure_pa_grid),11)
    ax1 = plt.subplot(311)
    plt.plot(element_value_x,element_value_z,'k.')
    cs2 = plt.contourf(x1, z1, gas_pressure_pa_grid, level_1, cmap=plt.cm.jet)
    fig.colorbar(cs2, orientation='vertical',fraction=0.02,pad=0.05)
    plt.ylabel('y (m)')
    plt.xlabel('x (m) gas_pressure_Kpa')
    plt.ylim(-length_z,0)
    plt.xlim(0,length_x)

    liq_saturation_grid=griddata((element_value_x,element_value_z),liq_saturation[:,i],(xi,zi),method='linear')
    level_2=np.linspace(0,1.,11)
    ax2=plt.subplot(312)
    cs=plt.contourf(x1, z1, liq_saturation_grid, level_2, cmap=plt.cm.jet)
    fig.colorbar(cs, orientation='vertical',fraction=0.02,pad=0.05)
    plt.ylabel('y (m)')
    plt.xlabel('x (m) liq_saturation')
    plt.ylim(-length_z,0)
    plt.xlim(0,length_x)
	
    brine_mass_fraction_in_liquid_grid=griddata((element_value_x,element_value_z),
	                                            brine_mass_fraction_in_liquid[:,i],(xi,zi),method='linear')
    level_1=np.linspace(0,1.,11)
    ax1 = plt.subplot(313)
    plt.plot(element_value_x,element_value_z,'k.')
    cs2 = plt.contourf(x1, z1, brine_mass_fraction_in_liquid_grid, level_1, cmap=plt.cm.jet)
    fig.colorbar(cs2, orientation='vertical',fraction=0.02,pad=0.05)
    plt.ylabel('y (m)')
    plt.xlabel('x (m) brine_mass_fraction_in_liquid')
    plt.ylim(-length_z,0)
    plt.xlim(0,length_x)


    fig.suptitle('time: %6.2e s' %lst.times[i])
    plt.rcParams.update({'font.size':10})
    fig.tight_layout()
    plt.savefig('figure/output_'+str(i+101)+'.png',dpi=300) 
    i+=2
#plt.close('all')