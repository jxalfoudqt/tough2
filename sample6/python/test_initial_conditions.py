### this code is trying to analyse the initial conditons given by ITOUGH2 EOS4 sample 6 with Tao
### TO190702
import sys
import os 
pyduino_path=os.path.join(os.environ['pyduino'],'python','post_processing')
sys.path.append(pyduino_path)
import constants
temperature_k_top               = constants.kelvin+dat.incon['XX  1'][1][1]
P_gas_top                       = dat.incon['XX  1'][1][0]
P_air_top                       = dat.incon['XX  1'][1][2]
saturated_vapor_pressure_top_pa = constants.svp(temperature_k_top)
saturated_vapor_pressure_top_pa
P_vapor_top                     = P_gas_top-P_air_top
P_vapor_top
relative_humidity_top           = P_vapor_top/saturated_vapor_pressure_top_pa
relative_humidity_top

import numpy as np
matric_potential_top_m = np.log(relative_humidity_top)*constants.R*temperature_k_top/ constants.g / constants.molecular_weight_water
capillary_pressure_top_pa = matric_potential_top_m* constants.rhow_pure_water * constants.g
print 'from the listing file in tough2 sam6, the capillary pressure is set as -5.e7, very close to what we have calculated here'
print capillary_pressure_top_pa
text= """this has been tested successfully the initial condition of the top most node 
    XX  1            .10000000E-01
    .1000000000000E+06  .1300000000000E+02  .9897536985191E+05
    This follows a format of P_gas, temperature, P_air. 
    Bear in mind that P_gas=P_air+P_vapour
    """
print text

### below is to test the node after the top one.



#temperature_below_k  = constants.kelvin+dat.incon['XX  1'][1][1]

P_gas_below          = dat.incon['RR117'][1][0]
gas_saturation_below = dat.incon['RR117'][1][1]
P_air_below          = dat.incon['RR117'][1][2]
temperature_below_k=constants.kelvin+13

## it is very likely that T2 back calculate temperture use newton method in the code. we have tried to find out the iteration in the code and 
## yet found where it is. could potentially be in t2f.f or it2main.f
## now we dicided to assume the initial tempeature is 13 degreee and we could use them to back calculate the correlation.

liquid_saturation_below=1-gas_saturation_below

saturated_vapor_pressure_below_pa = constants.svp(temperature_below_k)
P_vapor_below                     = P_gas_below-P_air_below
relative_humidity_below=P_vapor_below/saturated_vapor_pressure_below_pa

matric_potential_below_m = np.log(relative_humidity_below)*constants.R*temperature_below_k/ constants.g / constants.molecular_weight_water

capillary_pressure_below_pa = matric_potential_below_m* constants.rhow_pure_water * constants.g

capillary_pressure=1*P_zero*(S_star**(-1/lamda)-1)**(1-lamda) 


matric_potential_m=-capillary_pressure/constants.g/constants.rhow_pure_water

relative_humidity=np.exp(matric_potential_m* constants.g* constants.molecular_weight_water / constants.R / temperature_below_k)




text="""RR  2            .10000000E-01
  .9968214212018E+05  .5802059195562E+00  .9823372312908E+05"""

text2= """MATRI    2     2706.       .01 1.000E-17 1.000E-17 1.000E-17       2.1    -1000.
 2.000E-11                     1.000E+00
    11            .00       .00
    11      3.000E+00 1.000E+06     """


#RR 31            .10000000E-01
#  .1047309748442E+06  .1390884268912E-02  .1032344587972E+06


#n=3.
#alpha=1.e-6
#m=1.-1./n

-(liquid_saturation_below**(-1./m)-1)**(1./n)/alpha



lambda_= 3.000E+00
p0=1e-6


-p0*(liquid_saturation_below**(-1./lambda_) - 1)**(1-lambda_)



#RR 30    30 0.10452E+06 0.13000E+02 0.13875E-02 0.99861E+00 0.99104E+00 0.16560E-04 0.10302E+06-0.30000E+01 0.12653E+01 0.99949E+03




# ELEM.  INDEX     P           T          SG          SL       XAIRG       XAIRL        PAIR        PCAP          DG          DL
#RR117   117 0.15991E+06 0.13000E+02 0.22020E-02 0.99780E+00 0.99415E+00 0.25465E-04 0.15842E+06-0.10833E+03 0.19396E+01 0.99951E+03
#
#
#RR117            .10000000E-01
#  .1599137276602E+06  .2201955175846E-02  .1584172111617E+06
# test results
#1. p_gas passed
#2. P_air passed
#3. liquid water saturation - capillary pressure passed
#4. 


