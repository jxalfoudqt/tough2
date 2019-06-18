
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from t2data import *

saturation=np.linspace(0,1,100)

name='sam1'
dat = t2data(name)
print dat.grid.rocktype
dat.parameter

porosity_ROCK1=dat.grid.rocktype['ROCK1'].porosity

capillarity_parameter_array_ROCK1=dat.grid.rocktype['ROCK1'].capillarity['parameters']
capillarity_type_ROCK1=dat.grid.rocktype['ROCK1'].capillarity['type']
relative_permeability_parameter_array_ROCK1=dat.grid.rocktype['ROCK1'].relative_permeability['parameters']
relative_permeability_type_ROCK1=dat.grid.rocktype['ROCK1'].relative_permeability['type']


fig=plt.figure()
ax3=plt.subplot(211)

if  capillarity_type_ROCK1==7:
    lamda_ROCK1=capillarity_parameter_array_ROCK1[0]
    liquid_residual_saturation_ROCK1=capillarity_parameter_array_ROCK1[1]
    P_zero=1./capillarity_parameter_array_ROCK1[2]	
    Pressure_max=capillarity_parameter_array_ROCK1[3]		
    saturated_liquid_saturation_ROCK1=capillarity_parameter_array_ROCK1[4]
    S_star=(saturation-liquid_residual_saturation_ROCK1)/(saturated_liquid_saturation_ROCK1-liquid_residual_saturation_ROCK1)
    capillary_pressure=1*P_zero*(S_star**(-1/lamda_ROCK1)-1)**(1-lamda_ROCK1)
    ax3.plot(saturation,capillary_pressure,'k-o',)
    plt.xlabel('saturation')
    plt.ylabel('capillary_pressure (LOG)')
    #plt.ylim(1.5,-0.1)
    #plt.xlim()
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax3.set_yscale('log')
	
	
	
	
ax1=plt.subplot(212)

if  relative_permeability_type_ROCK1==7:
    lamda_ROCK1=relative_permeability_parameter_array_ROCK1[0]
    liquid_residual_saturation_ROCK1=relative_permeability_parameter_array_ROCK1[1]
    saturated_liquid_saturation_ROCK1=relative_permeability_parameter_array_ROCK1[2]
    gas_residual_saturation_ROCK1=relative_permeability_parameter_array_ROCK1[3]
    S_star=(saturation-liquid_residual_saturation_ROCK1)/(saturated_liquid_saturation_ROCK1-liquid_residual_saturation_ROCK1)
    S_bar=(saturation-liquid_residual_saturation_ROCK1)/(1-gas_residual_saturation_ROCK1-liquid_residual_saturation_ROCK1)
    liquid_relative_permeability=S_star**0.5*(1-(1-S_star**(1/lamda_ROCK1))**lamda_ROCK1)**2
    liquid_relative_permeability[saturation>=saturated_liquid_saturation_ROCK1]=1
    gas_relative_permeability=(1-S_bar)**2*(1-S_bar**2)
    if gas_residual_saturation_ROCK1==0:
        gas_relative_permeability=1-liquid_relative_permeability_capillary_pressure

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
	
fig.suptitle(dat.grid.rocktype['ROCK1'])
plt.rcParams.update({'font.size': 10})
#fig.tight_layout()
plt.savefig("Capillary & SWCC for ROCK1.png",dpi=300) 






porosity_BOUN1=dat.grid.rocktype['BOUN1'].porosity

capillarity_parameter_array_BOUN1=dat.grid.rocktype['BOUN1'].capillarity['parameters']
capillarity_type_BOUN1=dat.grid.rocktype['BOUN1'].capillarity['type']
relative_permeability_parameter_array_BOUN1=dat.grid.rocktype['BOUN1'].relative_permeability['parameters']
relative_permeability_type_BOUN1=dat.grid.rocktype['BOUN1'].relative_permeability['type']


fig=plt.figure()
ax3=plt.subplot(211)

if  capillarity_type_BOUN1==7:
    lamda_BOUN1=capillarity_parameter_array_BOUN1[0]
    liquid_residual_saturation_BOUN1=capillarity_parameter_array_BOUN1[1]
    P_zero=1./capillarity_parameter_array_BOUN1[2]	
    Pressure_max=capillarity_parameter_array_BOUN1[3]		
    saturated_liquid_saturation_BOUN1=capillarity_parameter_array_BOUN1[4]
    S_star=(saturation-liquid_residual_saturation_BOUN1)/(saturated_liquid_saturation_BOUN1-liquid_residual_saturation_BOUN1)
    capillary_pressure=1*P_zero*(S_star**(-1/lamda_BOUN1)-1)**(1-lamda_BOUN1)
    ax3.plot(saturation,capillary_pressure,'k-o',)
    plt.xlabel('saturation')
    plt.ylabel('capillary_pressure (LOG)')
    #plt.ylim(1.5,-0.1)
    #plt.xlim()
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    ax3.set_yscale('log')
	
	
	
	
ax1=plt.subplot(212)

if  relative_permeability_type_BOUN1==7:
    lamda_BOUN1=relative_permeability_parameter_array_BOUN1[0]
    liquid_residual_saturation_BOUN1=relative_permeability_parameter_array_BOUN1[1]
    saturated_liquid_saturation_BOUN1=relative_permeability_parameter_array_BOUN1[2]
    gas_residual_saturation_BOUN1=relative_permeability_parameter_array_BOUN1[3]
    S_star=(saturation-liquid_residual_saturation_BOUN1)/(saturated_liquid_saturation_BOUN1-liquid_residual_saturation_BOUN1)
    S_bar=(saturation-liquid_residual_saturation_BOUN1)/(1-gas_residual_saturation_BOUN1-liquid_residual_saturation_BOUN1)
    liquid_relative_permeability=S_star**0.5*(1-(1-S_star**(1/lamda_BOUN1))**lamda_BOUN1)**2
    liquid_relative_permeability[saturation>=saturated_liquid_saturation_BOUN1]=1
    gas_relative_permeability=(1-S_bar)**2*(1-S_bar**2)
    if gas_residual_saturation_BOUN1==0:
        gas_relative_permeability=1-liquid_relative_permeability_capillary_pressure

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
	
fig.suptitle(dat.grid.rocktype['BOUN1'])
plt.rcParams.update({'font.size': 10})
#fig.tight_layout()
plt.savefig("Capillary & SWCC for BOUN1.png",dpi=300) 







# os.system("itough2 sam1p2i sam1 4") 

# porosity=0.45
# area=0.007854
# liq_density_kgPm3=1000
# water_molecular_weight=0.018
# R_value=8.314
# m2mm=1000
# day2s=3600*24
# T_kelven=273.15

# time_idx=0
# vapor_mass_idx=1
# liq_mass_idx=2
# darcy_vapor_velocity_idx=np.arange(3,18,1)
# darcy_liquid_velocity_idx=np.arange(18,33,1)
# Liq_sat_idx=np.arange(33,49,1)
# Temperature_idx=np.arange(49,65,1)
# capillary_pressure_idx=np.arange(65,81,1)
# gas_pressure_idx=np.arange(81,97,1)

# name='sam1p2i'
# file_read = open(name+''+'.col', 'r')
# lines = file_read.read().split('\n')
# file_write = open(name+''+'.txt', "w")
# for i in range(2,len(lines),1):
    # file_write.write(lines[i]+'\n')
# file_write.close()
# data_new= loadtxt(name+''+'.txt', comments="#", delimiter=",", unpack=False)

# connection=np.arange(0,1.41,0.1)
# element=np.arange(-0.05,1.46,0.1)
# time_min=data_new[:,time_idx]
# vapor_mass_kg=data_new[:,vapor_mass_idx]
# liq_mass_kg=data_new[:,liq_mass_idx]
# Liq_sat=data_new[:,Liq_sat_idx]
# Temperature_degree=data_new[:,Temperature_idx]
# capillary_pressure_pa=data_new[:,capillary_pressure_idx]
# gas_pressure_pa=data_new[:,gas_pressure_idx]
# vapor_pore_velocity_mmPday=data_new[:,darcy_vapor_velocity_idx]/area/liq_density_kgPm3*m2mm*day2s
# liq_pore_velocity_mmPday=data_new[:,darcy_liquid_velocity_idx]/area/liq_density_kgPm3*m2mm*day2s


# vapor_pressure_statuated_pa=611*np.exp(17.27*Temperature_degree/(Temperature_degree+T_kelven-35.85))
# relative_humidity=np.exp(water_molecular_weight*capillary_pressure_pa/liq_density_kgPm3/R_value/(Temperature_degree+T_kelven))
# vapor_pressure_pa=vapor_pressure_statuated_pa*relative_humidity
# liq_pressure_pa=gas_pressure_pa+capillary_pressure_pa

# i=0
# while i<len(data_new):
    # fig=plt.figure()
    # ax5=plt.subplot(241)
    # ax5.plot(vapor_pore_velocity_mmPday[i],connection[::-1],'k-o',)
    # plt.xlabel('VAP Dar. vel. (mm/day)')
    # plt.ylabel('high (m)')
    # #ax5.spines['top'].set_color('red')
    # plt.ylim(1.5,-0.1)
    # plt.xlim(np.nanmin(vapor_pore_velocity_mmPday),np.nanmax(vapor_pore_velocity_mmPday))
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    # #ax5.set_xscale('log')
    # ax6=ax5.twiny()
    # ax6.plot(liq_pore_velocity_mmPday[i],connection[::-1],'r-o')
    # plt.xlabel('Liq. Dar. vel. (mm/day)')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1)
    # plt.xlim(np.nanmin(liq_pore_velocity_mmPday),np.nanmax(liq_pore_velocity_mmPday))
    # #x6.set_xscale('log')
    # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    # ax6.spines['top'].set_color('red')
    # ax6.xaxis.label.set_color('red')
    # ax6.tick_params(axis='x', colors='red')	 

    # plt.subplot(242)
    # plt.plot(Liq_sat[i]*100,element[::-1],'b-o')
    # plt.xlabel('Liq. sat. (%)')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1)
    # plt.xlim(np.nanmin(Liq_sat)*100,np.nanmax(Liq_sat)*100)
	
    # ax7=plt.subplot(243)
    # ax7.plot(gas_pressure_pa[i]/1000,element[::-1],'k-o')
    # plt.xlabel('Gas pre. (Kpa)')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1) 
    # plt.xlim(np.nanmin(gas_pressure_pa)/1000,np.nanmax(gas_pressure_pa)/1000)	
    # ax8=ax7.twiny()	
    # ax8.plot(capillary_pressure_pa[i]/1000,element[::-1],'r-o')
    # plt.xlabel('Cap. pre. (Kpa)')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1) 
    # plt.xlim(np.nanmin(capillary_pressure_pa)/1000,np.nanmax(capillary_pressure_pa)/1000)	
    # ax8.spines['top'].set_color('red')	
    # ax8.xaxis.label.set_color('red')
    # ax8.tick_params(axis='x', colors='red')	 	

    # ax11=plt.subplot(244)
    # ax11.plot(vapor_pressure_pa[i],element[::-1],'k-o')
    # plt.xlabel('Vap pre. ')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1) 
    # plt.xlim(np.nanmin(vapor_pressure_pa),np.nanmax(vapor_pressure_pa))	
    # ax12=ax11.twiny()	
    # ax12.plot(liq_pressure_pa[i]/1000,element[::-1],'r-o')
    # plt.xlabel('Liq. pre.(Kpa)')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1) 
    # plt.xlim(np.nanmin(liq_pressure_pa)/1000,np.nanmax(liq_pressure_pa)/1000)	
    # ax12.spines['top'].set_color('red')	
    # ax12.xaxis.label.set_color('red')
    # ax12.tick_params(axis='x', colors='red')	 	
	
    # ax1=plt.subplot(413)
    # ax1.plot(time_min[:i+1],vapor_mass_kg[:i+1],'k-o')
    # plt.ylabel('Vap. mass (kg)')
    # plt.ylim(np.min(vapor_mass_kg),np.max(vapor_mass_kg))
    # plt.xlim(0,np.max(time_min))
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0),useLocale=0)
    # #ax1.spines['left'].set_color('blue')
    # ax2 = ax1.twinx() 
    # ax2.plot(time_min[:i+1],liq_mass_kg[:i+1],'r-o',)
    # plt.ylim(np.min(liq_mass_kg),np.max(liq_mass_kg))
    # plt.xlim(0,np.max(time_min))
    # plt.ylabel('Liq. mass (kg)')
    # plt.xlabel('Time (min)')
    # ax2.spines['right'].set_color('red')
    # ax2.yaxis.label.set_color('red')
    # ax2.tick_params(axis='y', colors='red')	 	
	
    # ax3=plt.subplot(414)
    # ax3.plot(time_min[:i+1],vapor_pore_velocity_mmPday[:i+1,-1],'k-o')
    # plt.ylabel('VAP Dar. vel. (mm/day)')
    # plt.ylim(np.min(vapor_pore_velocity_mmPday[:,-1]),np.max(vapor_pore_velocity_mmPday[:,-1]))
    # plt.xlim(0,np.max(time_min))
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # ax4 = ax3.twinx() 
    # ax4.plot(time_min[:i+1],liq_pore_velocity_mmPday[:i+1,-1],'r-o',)
    # plt.ylim(np.min(liq_pore_velocity_mmPday[:,-1]),np.max(liq_pore_velocity_mmPday[:,-1]))
    # plt.xlim(0,np.max(time_min))
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.ylabel('Liq. Dar. vel. (mm/day)')
    # plt.xlabel('Time (min)')
    # ax4.spines['right'].set_color('red')
    # ax4.yaxis.label.set_color('red')
    # ax4.tick_params(axis='y', colors='red')		
    # # plt.subplot(414)
    # # plt.plot(total_pore_velocity[:i+1,-1],time[:i+1],'b-o')
    # # #plt.ylim(0,7)
    # # plt.xlim(0,200)
    # # plt.ylabel('Liq. mass (kg)')
    # # plt.xlabel('time (min)')		

    # fig.suptitle("Time="+str(round(time_min[i],2))+" min")
    # plt.rcParams.update({'font.size': 7})
    # fig.tight_layout()
    # plt.savefig("results_time"+str(i+100)+".png",dpi=300)   
    # i+=1

#os.system("/usr/bin/ffmpeg -r 4/1 -start_number 100 -i results_time%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4") 