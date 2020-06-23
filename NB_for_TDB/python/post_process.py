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

# # # delete existing png to avoid old png mixing with new ones
# if os.path.exists('figure'):
    # fig_path  = os.path.join(os.getcwd(),'figure')
    # fig_files = os.listdir(fig_path)
    # count=0
    # for item in fig_files:
        # if item.endswith(".png"):
            # count+=1
            # os.remove(os.path.join( fig_path , item))
    # print("Existing "+ str(count)+ " png file" + " deleted\n")
# else:
    # print("figure directory does not exist and created.\n")
    # os.makedirs('figure')



print("plotting result\n")
fig=plt.figure()
ax1 = plt.subplot(411)
plt.plot(lst.times[:-1]/3600/24,np.diff(lst.times),'k-', label='output' )
plt.legend(loc="center right",prop={'size':10})
plt.ylabel('dt (s)')
plt.xlabel('time (day)')
plt.xlim(0,np.max(lst.times/86400))

pressure_pa_calculated = pressure_zero*(np.sin(time_variation_par*lst.times)*0.05+1)
ax1 = plt.subplot(412)
plt.plot(lst.times/3600/24,gas_pressure_pa[-1]/1000,'k-', label='Simulation' )
plt.plot(lst.times/3600/24,pressure_pa_calculated/1000,'r-', label='Analytical')
plt.legend(loc="center right",prop={'size':10})
plt.ylabel('output P (Kpa)')
plt.xlabel('output time (day)')
plt.xlim(0,np.max(lst.times/86400))

ax1 = plt.subplot(413)
plt.plot(time_variation_s/3600/24,pressure_pa/1000,'r-', label='Input')
plt.plot(lst.times/3600/24,gas_pressure_pa[-1]/1000,'k-', label='output' )
plt.legend(loc="center right",prop={'size':10})
plt.ylabel('zzz13 P (Kpa)')
plt.xlabel('time (day)')

ax1 = plt.subplot(414)
plt.plot(lst.times/3600/24,gas_pressure_pa[-2]/1000,'k-', label='a 1' )
plt.legend(loc="center right",prop={'size':10})
plt.xlabel('time (day)')
plt.ylabel('P (Kpa')
plt.xlim(0,np.max(lst.times/86400))

# ax1 = plt.subplot(515)
# plt.plot(lst.times,liq_saturation[-1],'r-', label='Output' )
# plt.ylabel('liq Sat')
# plt.xlabel('time (s)')
# plt.ylim(0.9, 1.1)

plt.rcParams.update({'font.size':10})
fig.tight_layout()
plt.savefig('figure/output_V'+str(np.log10(bvol))+'_compressibility'+str(np.log10(r3.compressibility))+'_Relative_error'+str(np.log10(dat.parameter['relative_error']))
            +'_gene_points'+str(max_bdy_point_numbers)+'_posority'+str(r3.porosity)+'_max(dt)'+str(dat.parameter['max_timestep'])+'.png',dpi=300) 


# fig=plt.figure()
# ax1 = plt.subplot(411)
# plt.plot(lst.times[:-1]/3600/24,np.diff(lst.times),'k-', label='output' )
# plt.legend(loc="center right",prop={'size':10})
# plt.ylabel('dt (s)')
# plt.xlabel('time (s)')
# plt.xlim(345,365)

# ax1 = plt.subplot(412)
# plt.plot(lst.times/3600/24,pressure_pa_calculated/1000,'r-', label='Analytical')
# plt.plot(lst.times/3600/24,gas_pressure_pa[-1]/1000,'k-', label='Simulation' )
# plt.legend(loc="center right",prop={'size':10})
# plt.ylabel('output P (Kpa)')
# plt.xlabel('output time (day)')
# plt.xlim(345,365)

# ax1 = plt.subplot(413)
# plt.plot(time_variation_s/3600/24,pressure_pa/1000,'r-', label='Input')
# plt.plot(lst.times/3600/24,gas_pressure_pa[-1]/1000,'k-', label='output' )
# plt.legend(loc="center right",prop={'size':10})
# plt.ylabel('zzz13 P (Kpa)')
# plt.xlabel('time (day)')
# plt.xlim(345,365)

# ax1 = plt.subplot(414)
# plt.plot(time_variation_s/3600/24,flow_rate_kgPs,'k-',label='Input')
# plt.plot(lst.times/3600/24,water_generation_kgPs[0],'r-',label='Output')
# plt.xlabel('time (day)')
# plt.ylabel('Gene (kg/s)')
# plt.xlim(345,365)

# plt.rcParams.update({'font.size':10})
# fig.tight_layout()
# plt.savefig('figure/output_last10period_V'+str(np.log10(bvol))+'_compressibility'+str(np.log10(r3.compressibility))+'_Relative_error'+str(np.log10(dat.parameter['relative_error']))
            # +'_gene_points'+str(max_bdy_point_numbers)+'_porosity'+str(r3.porosity)+'_max(dt)'+str(dat.parameter['max_timestep'])+'.png',dpi=300) 
# #plt.close('all')