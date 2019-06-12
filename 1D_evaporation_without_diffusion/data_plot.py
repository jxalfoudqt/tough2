import numpy as np
import pandas as pd
import re
import math
import matplotlib.pyplot as plt
import csv
import os
from collections import Counter

porosity=0.45
area=0.007854
liq_density_kgPm3=1000
air_molecular_weight=0.02897
water_molecular_weight=0.018
R_value=8.314
m2mm=1000
day2s=3600*24
T_kelven=273.15


time_idx=0
gas_mass_idx=1
liq_mass_idx=2
darcy_gas_velocity_idx=np.arange(3,18,1)
darcy_liquid_velocity_idx=np.arange(18,33,1)
Liq_sat_idx=np.arange(33,49,1)
mass_fraction_of_air_in_gas_idx=np.arange(49,65,1)
capillary_pressure_idx=np.arange(65,81,1)
gas_pressure_idx=np.arange(81,97,1)


x=100
y=97

name="sam1p2i"
all_the_text = open(name+''+'.col').read()
all_data=re.findall(r"\d+\.?\d*",all_the_text)
b=np.array([m.start() for m in re.finditer('-', all_the_text)])
bb=b/(22*y)
aa=(b-bb*(22*y))/22

cc=np.empty(len(aa)-1)
cc[:]=np.nan
i=0
while i<len(aa)-1:
    if aa[i+1]-aa[i]==0:
        cc[i]=aa[i]
    i+=1
#cc=np.array([item for item, count in Counter(aa).iteritems() if count > 1])

data=np.empty((x,y*2))
i=0
while i<x:
    j=0
    while j<y*2:
	    data[i,j]=float(all_data[i*y*2+j])
	    j+=1
    i+=1

data_1=data[:,::2]
data_2=data[:,1::2]
data_new=np.empty((x,y))
i=0
while i<x:
    j=0
    while j<y:
        if np.sum(i==bb)>=1 and np.sum(j==aa)>=1:
            data_new[i,j]=data_1[i,j]*math.pow(10,-data_2[i,j])
        else:
            data_new[i,j]=data_1[i,j]*math.pow(10,data_2[i,j])	   
        j+=1
    i+=1
	
connection=np.arange(0,1.41,0.1)
element=np.arange(-0.05,1.46,0.1)
time_min=data_new[:,time_idx]
gas_mass_kg=data_new[:,gas_mass_idx]
liq_mass_kg=data_new[:,liq_mass_idx]
Liq_sat=data_new[:,Liq_sat_idx]
mass_fraction_of_air_in_gas=data_new[:,mass_fraction_of_air_in_gas_idx]
gas_molecular_weight=air_molecular_weight*mass_fraction_of_air_in_gas+water_molecular_weight*(1-mass_fraction_of_air_in_gas)
Temperature_degree=20
capillary_pressure_pa=data_new[:,capillary_pressure_idx]*-1
gas_pressure_pa=data_new[:,gas_pressure_idx]
gas_density_kgPm3=gas_pressure_pa*gas_molecular_weight/R_value/(Temperature_degree+T_kelven)
gas_pore_velocity_mmPday=-1*data_new[:,darcy_gas_velocity_idx]/area/liq_density_kgPm3*m2mm*day2s
liq_pore_velocity_mmPday=data_new[:,darcy_liquid_velocity_idx]/area/liq_density_kgPm3*m2mm*day2s
total_pore_velocity=gas_pore_velocity_mmPday+liq_pore_velocity_mmPday


liq_residual_saturation=0.045
lamda=0.627
liq_saturated_saturation=1
gas_residual_saturation=0.054
P_max_reciprocal=0.345E-03
instrinsic_perm=2.000E-12

S_star=(Liq_sat-liq_residual_saturation)/(liq_saturated_saturation-liq_residual_saturation)
liq_relative_perm=S_star**(0.5)*(1-(1-S_star**(1/lamda))**lamda)**2
liq_perm=liq_relative_perm*instrinsic_perm

S_bar=(Liq_sat-liq_residual_saturation)/(1-liq_residual_saturation-gas_residual_saturation)
gas_relative_perm=(1-S_bar)**2*(1-S_bar**2)
gas_perm=gas_relative_perm*instrinsic_perm


i=0
while i<x:
    fig=plt.figure()
    ax5=plt.subplot(251)
    ax5.plot(gas_pore_velocity_mmPday[i],connection[::-1],'k-o',)
    plt.xlabel('GAS Dar. vel. (mm/day)')
    plt.ylabel('high (m)')
    #ax5.spines['top'].set_color('red')
    plt.ylim(1.5,-0.1)
    plt.xlim(np.nanmin(gas_pore_velocity_mmPday),np.nanmax(gas_pore_velocity_mmPday))
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

    # ax9=plt.subplot(242)
    # ax9.plot(gas_perm[i],element[::-1],'k-o')
    # plt.xlabel('GAS per. (m2/s)')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1) 
    # plt.xlim(np.nanmin(gas_perm),np.nanmax(gas_perm))	
    # ax9.set_xscale('log')
    # ax10=ax9.twiny()	
    # #plt.subplot(254)
    # ax10.plot(liq_perm[i],element[::-1],'r-o')
    # plt.xlabel('Liq per. (m2/s)')
    # # plt.ylabel('high (m)')
    # plt.ylim(1.5,-0.1) 
    # plt.xlim(np.nanmin(liq_perm),np.nanmax(liq_perm))
    # ax10.set_xscale('log')	
    # ax10.spines['top'].set_color('red')	
    # ax10.xaxis.label.set_color('red')
    # ax10.tick_params(axis='x', colors='red')		

    plt.subplot(253)
    plt.plot(Liq_sat[i]*100,element[::-1],'b-o')
    plt.xlabel('Liq. sat. (%)')
    # plt.ylabel('high (m)')
    plt.ylim(1.5,-0.1)
    plt.xlim(np.nanmin(Liq_sat)*100,np.nanmax(Liq_sat)*100)
	
    ax7=plt.subplot(254)
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

	
    ax1=plt.subplot(413)
    ax1.plot(time_min[:i+1],gas_mass_kg[:i+1],'k-o')
    plt.ylabel('GAS mass (kg)')
    plt.ylim(np.min(gas_mass_kg),np.max(gas_mass_kg))
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
    ax3.plot(time_min[:i+1],gas_pore_velocity_mmPday[:i+1,-1],'k-o')
    plt.ylabel('GAS Dar. vel. (mm/day)')
    plt.ylim(np.min(gas_pore_velocity_mmPday[:,-1]),np.max(gas_pore_velocity_mmPday[:,-1]))
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
    plt.savefig("results_time"+str(i+100)+".png",dpi=300)   
    i+=5

#os.system("/usr/bin/ffmpeg -r 4/1 -start_number 100 -i results_time%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4") 