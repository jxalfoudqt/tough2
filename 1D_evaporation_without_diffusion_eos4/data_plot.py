for name in dir():
    if not name.startswith('_'):
        del globals()[name]

import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from numpy import loadtxt

os.remove("sam1p2i.col")
os.remove("sam1.out")
os.system("itough2 sam1p2i sam1 4") 


print ('Now parsing the result\n')

porosity               = 0.45
area                   = 0.007854
liq_density_kgPm3      = 1000
water_molecular_weight = 0.018
R_value                = 8.314
m2mm                   = 1000
day2s                  = 3600*24
T_kelven               = 273.15

time_idx                  = 0
vapor_mass_idx            = 1
liq_mass_idx              = 2
darcy_vapor_velocity_idx  = np.arange(3,18,1)
darcy_liquid_velocity_idx = np.arange(18,33,1)
Liq_sat_idx               = np.arange(33,49,1)
Temperature_idx           = np.arange(49,65,1)
capillary_pressure_idx    = np.arange(65,81,1)
gas_pressure_idx          = np.arange(81,97,1)

name              = 'sam1p2i'
file_read         = open(name+''+'.col', 'r')
lines             = file_read.read().split('\n')
file_read.close()
file_write        = open(name+''+'.txt', "w")
for i in range(2,len(lines),1):
    file_write.write(lines[i]+'\n')
file_write.close()
data_new= loadtxt(name+''+'.txt', comments="#", delimiter=",", unpack=False)

connection                 = np.arange(0,1.41,0.1)
element                    = np.arange(-0.05,1.46,0.1)
time_min                   = data_new[:,time_idx]
vapor_mass_kg              = data_new[:,vapor_mass_idx]
liq_mass_kg                = data_new[:,liq_mass_idx]
Liq_sat                    = data_new[:,Liq_sat_idx]
Temperature_degree         = data_new[:,Temperature_idx]
capillary_pressure_pa      = data_new[:,capillary_pressure_idx]
gas_pressure_pa            = data_new[:,gas_pressure_idx]
vapor_pore_velocity_mmPday = data_new[:,darcy_vapor_velocity_idx]/area/liq_density_kgPm3*m2mm*day2s
liq_pore_velocity_mmPday   = data_new[:,darcy_liquid_velocity_idx]/area/liq_density_kgPm3*m2mm*day2s
#gas_molecular_weight=air_molecular_weight*mass_fraction_of_air_in_gas+water_molecular_weight*(1-mass_fraction_of_air_in_gas)
#gas_density_kgPm3=gas_pressure_pa*gas_molecular_weight/R_value/(Temperature_degree+T_kelven)

vapor_pressure_statuated_pa = 611*np.exp(17.27*Temperature_degree/(Temperature_degree+T_kelven-35.85))
relative_humidity           = np.exp(water_molecular_weight*capillary_pressure_pa/liq_density_kgPm3/R_value/(Temperature_degree+T_kelven))
vapor_pressure_pa           = vapor_pressure_statuated_pa*relative_humidity
liq_pressure_pa             = gas_pressure_pa+capillary_pressure_pa


liq_residual_saturation  = 0.045
lamda                    = 0.627
liq_saturated_saturation = 1
gas_residual_saturation  = 0.054
P_max_reciprocal         = 0.345E-03
instrinsic_perm          = 2.000E-12

S_star            = (Liq_sat-liq_residual_saturation)/(liq_saturated_saturation-liq_residual_saturation)
liq_relative_perm = S_star**(0.5)*(1-(1-S_star**(1/lamda))**lamda)**2
liq_perm          = liq_relative_perm*instrinsic_perm
liq_perm[:]       = instrinsic_perm**30

S_bar             = (Liq_sat-liq_residual_saturation)/(1-liq_residual_saturation-gas_residual_saturation)
gas_relative_perm = (1-S_bar)**2*(1-S_bar**2)
gas_perm          = gas_relative_perm*instrinsic_perm


i=0
while i<len(data_new):
    print ('plotting the' + str(i) + 'result' )
    fig=plt.figure()

    ax5=plt.subplot(241)
    ax5.plot(vapor_pore_velocity_mmPday[i],connection[::-1],'k-o',)
    plt.xlabel('VAP Dar. vel. (mm/day)')
    plt.ylabel('high (m)')
    #ax5.spines['top'].set_color('red')
    plt.ylim(1.5,-0.1)
    plt.xlim(np.nanmin(vapor_pore_velocity_mmPday),np.nanmax(vapor_pore_velocity_mmPday))
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #ax5.set_xscale('log')
    ax6=ax5.twiny()
    ax6.plot(liq_pore_velocity_mmPday[i],connection[::-1],'r-o')
    plt.xlabel('Liq. Dar. vel. (mm/day)')
    # plt.ylabel('high (m)')
    plt.ylim(1.5,-0.1)
    plt.xlim(np.nanmin(liq_pore_velocity_mmPday),np.nanmax(liq_pore_velocity_mmPday))
    #x6.set_xscale('log')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax6.spines['top'].set_color('red')
    ax6.xaxis.label.set_color('red')
    ax6.tick_params(axis='x', colors='red')	 

    plt.subplot(242)
    plt.plot(Liq_sat[i]*100,element[::-1],'b-o')
    plt.xlabel('Liq. sat. (%)')
    # plt.ylabel('high (m)')
    plt.ylim(1.5,-0.1)
    plt.xlim(np.nanmin(Liq_sat)*100,np.nanmax(Liq_sat)*100)
	
    ax7=plt.subplot(243)
    ax7.plot(gas_pressure_pa[i]/1000,element[::-1],'k-o')
    plt.xlabel('Gas pre. (Kpa)')
    # plt.ylabel('high (m)')
    plt.ylim(1.5,-0.1) 
    plt.xlim(np.nanmin(gas_pressure_pa)/1000,np.nanmax(gas_pressure_pa)/1000)	
    ax8=ax7.twiny()	
    ax8.plot(capillary_pressure_pa[i]/1000,element[::-1],'r-o')
    plt.xlabel('Cap. pre. (Kpa)')
    # plt.ylabel('high (m)')
    plt.ylim(1.5,-0.1) 
    plt.xlim(np.nanmin(capillary_pressure_pa)/1000,np.nanmax(capillary_pressure_pa)/1000)	
    ax8.spines['top'].set_color('red')	
    ax8.xaxis.label.set_color('red')
    ax8.tick_params(axis='x', colors='red')	 	

    ax11=plt.subplot(244)
    ax11.plot(vapor_pressure_pa[i],element[::-1],'k-o')
    plt.xlabel('Vap pre. ')
    # plt.ylabel('high (m)')
    plt.ylim(1.5,-0.1) 
    plt.xlim(np.nanmin(vapor_pressure_pa),np.nanmax(vapor_pressure_pa))	
    ax12=ax11.twiny()	
    ax12.plot(liq_pressure_pa[i]/1000,element[::-1],'r-o')
    plt.xlabel('Liq. pre.(Kpa)')
    # plt.ylabel('high (m)')
    plt.ylim(1.5,-0.1) 
    plt.xlim(np.nanmin(liq_pressure_pa)/1000,np.nanmax(liq_pressure_pa)/1000)	
    ax12.spines['top'].set_color('red')	
    ax12.xaxis.label.set_color('red')
    ax12.tick_params(axis='x', colors='red')	 	
	
    ax1=plt.subplot(413)
    ax1.plot(time_min[:i+1],vapor_mass_kg[:i+1],'k-o')
    plt.ylabel('Vap. mass (kg)')
    plt.ylim(np.min(vapor_mass_kg),np.max(vapor_mass_kg))
    plt.xlim(0,np.max(time_min))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0),useLocale=0)
    #ax1.spines['left'].set_color('blue')
    ax2 = ax1.twinx() 
    ax2.plot(time_min[:i+1],liq_mass_kg[:i+1],'r-o',)
    plt.ylim(np.min(liq_mass_kg),np.max(liq_mass_kg))
    plt.xlim(0,np.max(time_min))
    plt.ylabel('Liq. mass (kg)')
    plt.xlabel('Time (min)')
    ax2.spines['right'].set_color('red')
    ax2.yaxis.label.set_color('red')
    ax2.tick_params(axis='y', colors='red')	 	
	
    ax3=plt.subplot(414)
    ax3.plot(time_min[:i+1],vapor_pore_velocity_mmPday[:i+1,-1],'k-o')
    plt.ylabel('VAP Dar. vel. (mm/day)')
    plt.ylim(np.min(vapor_pore_velocity_mmPday[:,-1]),np.max(vapor_pore_velocity_mmPday[:,-1]))
    plt.xlim(0,np.max(time_min))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax4 = ax3.twinx() 
    ax4.plot(time_min[:i+1],liq_pore_velocity_mmPday[:i+1,-1],'r-o',)
    plt.ylim(np.min(liq_pore_velocity_mmPday[:,-1]),np.max(liq_pore_velocity_mmPday[:,-1]))
    plt.xlim(0,np.max(time_min))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.ylabel('Liq. Dar. vel. (mm/day)')
    plt.xlabel('Time (min)')
    ax4.spines['right'].set_color('red')
    ax4.yaxis.label.set_color('red')
    ax4.tick_params(axis='y', colors='red')		
    # plt.subplot(414)
    # plt.plot(total_pore_velocity[:i+1,-1],time[:i+1],'b-o')
    # #plt.ylim(0,7)
    # plt.xlim(0,200)
    # plt.ylabel('Liq. mass (kg)')
    # plt.xlabel('time (min)')		

    fig.suptitle("Time="+str(round(time_min[i],2))+" min")
    plt.rcParams.update({'font.size': 7})
    fig.tight_layout()
    plt.savefig("results_time"+str(i+0)+"relative_k_8.png",dpi=300)   
    i+=1
#plt.close('all')
#os.system("/usr/bin/ffmpeg -r 4/1 -start_number 100 -i results_time%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4") 
