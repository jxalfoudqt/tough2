from t2listing import *   
from t2data import *      
import numpy as np
import matplotlib.pyplot as plt
import os 
import pandas as pd

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

# # parsing output file
name_input               = 'flow.inp'
inp                      = t2data(name_input)
name_output              = 'flow.out'
opt                      = t2listing(name_output)
aqui_con                 = toughreact_tecplot('aqui_con.dat',inp.grid.blocklist)
aqui_gas                 = toughreact_tecplot('aqui_gas.dat',inp.grid.blocklist)
aqui_min                 = toughreact_tecplot('aqui_min.dat',inp.grid.blocklist)

element_coordinate_m     = np.array([j.centre for j in inp.grid.blocklist])
element_x_m              = element_coordinate_m[:,0]
element_y_m              = element_coordinate_m[:,1]
element_z_m              = element_coordinate_m[:,2]
connection_x_location    = (element_x_m[1:]+element_x_m[:-1])/2
#connection_1st_distance  = np.array([blk.distance[0] for blk in inp.grid.connectionlist])

# print opt.element.column_name 
# print opt.connection.column_name
# print aqui_con.element.column_name
# print aqui_min.element.column_name
# print aqui_gas.element.column_name

opt.first(); aqui_gas.first(); aqui_min.first(); aqui_con.first()

# # plotting results
p=0
while p<opt.num_times:
    print("plotting " + str(p) + " / " + str(opt.num_times) + " result\n")

    fig = plt.figure(figsize=(16,12))
    no_row=5
    no_col=4
    ax = [[] for i in range(no_row*no_col)]
    k=0
    for i in np.arange(no_row):
        for j in np.arange(no_col):
            ax[k]= plt.subplot2grid((no_row, no_col), (i, j), colspan=1)
            ax[k].xaxis.set_tick_params(labelsize=10)
            ax[k].yaxis.set_tick_params(labelsize=10)
            k+=1
    fig.subplots_adjust(hspace=.50,wspace=.5)
    fig.subplots_adjust(left=0.10, right=0.90, top=0.92, bottom=0.05)

    # #aqui_con.element.column_name
    # #['X', 'Y', 'Z', 'P(bar)', 'Sg', 'Sl', 'T(C)', 'aH2O', 'pH', 't_h2o', 't_h+', 't_ca+2', 't_mg+2', 
    # #'t_na+', 't_k+', 't_hco3-', 't_so4-2', 't_cl-', 'X_na+', 'X_k+', 'X_ca+2', 'X_mg+2', 'X_h+']
    im0  =  ax[0].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['pH'])
    im1  =  ax[1].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_h2o'])
    im2  =  ax[2].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_h+'])
    im3  =  ax[3].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_ca+2'])
    im4  =  ax[4].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_mg+2'])
    im5  =  ax[5].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_na+'])
    im6  =  ax[6].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_k+'])
    im7  =  ax[7].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_hco3-'])
    im8  =  ax[8].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_so4-2'])
    im9  =  ax[9].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['t_cl-'])
    im10 = ax[10].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['X_na+'])
    im11 = ax[11].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['X_k+'])
    im12 = ax[12].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['X_ca+2'])
    im13 = ax[13].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['X_mg+2'])
    im14 = ax[14].plot(aqui_con.element.DataFrame['X'],aqui_con.element.DataFrame['X_h+'])
    
    # #aqui_min.element.column_name
    # #['X', 'Y', 'Z', 'T(C)', 'Porosity', 'Poros_Chg', 'Permx(m^2)', 'Kx/Kx0', 'Permz(m^2)', 'Kz/Kz0', 'calcite']
    im15 = ax[15].plot(aqui_min.element.DataFrame['X'],aqui_min.element.DataFrame['calcite'])
    im16 = ax[16].plot(aqui_min.element.DataFrame['X'],aqui_min.element.DataFrame['T(C)'])

    # #print aqui_gas.element.column_name
    # #['X', 'Y', 'Z', 'T(C)', 'Sg', 'RH']
	
	# #opt.element.column_name 
    # #['PRES', 'S(liq)', 'PCAP', 'K(rel)', 'DIFFUS.']
    im17 = ax[17].plot(element_x_m,opt.element.DataFrame['PRES'])	
    im18 = ax[18].plot(element_x_m,opt.element.DataFrame['S(liq)'])	
	
    # #opt.connection.column_name
    # #['FLO(LIQ.)', 'VEL(LIQ.)']
    im19 = ax[19].plot(connection_x_location,opt.connection.DataFrame['FLO(LIQ.)'])


    # # unit is given from aqui_con.dat header
    # ax[0 ].set_title('pH'          ,fontweight='bold')
    # ax[1 ].set_title('t_h20'        ,fontweight='bold')
    # ax[2 ].set_title('t_h+'         ,fontweight='bold')
    # ax[3 ].set_title('t_ca+2'       ,fontweight='bold')
    # ax[4 ].set_title('t_mg+2'       ,fontweight='bold')
    # ax[5 ].set_title('t_na+'        ,fontweight='bold')
    # ax[6 ].set_title('t_k+'         ,fontweight='bold')
    # ax[7 ].set_title('t_hco3-'      ,fontweight='bold')
    # ax[8 ].set_title('t_so4-2'      ,fontweight='bold')
    # ax[9 ].set_title('t_cl-'        ,fontweight='bold')
    # ax[10].set_title('X_na+'        ,fontweight='bold')
    # ax[11].set_title('X_k+'         ,fontweight='bold')
    # ax[12].set_title('X_ca+2'       ,fontweight='bold')
    # ax[13].set_title('X_mg+2'       ,fontweight='bold')
    # ax[14].set_title('X_h+'         ,fontweight='bold')
    # ax[15].set_title('calcite'      ,fontweight='bold')
    # ax[16].set_title('temperature'  ,fontweight='bold')
    # ax[17].set_title('pressure'     ,fontweight='bold')
    # ax[18].set_title('L_Saturation' ,fontweight='bold')
    # ax[19].set_title('Darcy_flow'   ,fontweight='bold')


    ax[0 ].set_ylabel('     pH     \n mol/L'      ,fontweight='bold')
    ax[1 ].set_ylabel('    t_h20   \n mol/L'      ,fontweight='bold')
    ax[2 ].set_ylabel('    t_h+    \n mol/L'      ,fontweight='bold')
    ax[3 ].set_ylabel('   t_ca+2   \n mol/L'      ,fontweight='bold')
    ax[4 ].set_ylabel('   t_mg+2   \n mol/L'      ,fontweight='bold')
    ax[5 ].set_ylabel('    t_na+   \n mol/L'      ,fontweight='bold')
    ax[6 ].set_ylabel('    t_k+    \n mol/L'      ,fontweight='bold')
    ax[7 ].set_ylabel('   t_hco3-  \n mol/L'      ,fontweight='bold')
    ax[8 ].set_ylabel('   t_so4-2  \n mol/L'      ,fontweight='bold')
    ax[9 ].set_ylabel('    t_cl-   \n mol/L'      ,fontweight='bold')
    ax[10].set_ylabel('X_na+'                     ,fontweight='bold')
    ax[11].set_ylabel('X_k+'                      ,fontweight='bold')
    ax[12].set_ylabel('X_ca+2'                    ,fontweight='bold')
    ax[13].set_ylabel('X_mg+2'                    ,fontweight='bold')
    ax[14].set_ylabel('X_h+'                      ,fontweight='bold')
    ax[15].set_ylabel('calcite'                   ,fontweight='bold')
    ax[16].set_ylabel('Temperature \n C'          ,fontweight='bold')
    ax[17].set_ylabel(' Pressure   \n Pa'         ,fontweight='bold')
    ax[18].set_ylabel('  Liquid    \n Saturation' ,fontweight='bold')
    ax[19].set_ylabel(' Darcy_flow \n Kg/s'       ,fontweight='bold')

	
    fig.suptitle('time: %.1e yrs' %(aqui_con.times[p]))
    plt.rcParams.update({'font.size':10})
    #fig.tight_layout()
    plt.savefig('figure/output_'+str(p+100)+'.png',dpi=200) 
    opt.next(); aqui_gas.next(); aqui_min.next(); aqui_con.next()	
    p+=1