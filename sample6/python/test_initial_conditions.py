### this code is trying to analyse the initial conditons given by ITOUGH2 EOS4 sample 6 with Tao
### TO190702
import sys
import os 
pyduino_path=os.path.join(os.environ['pyduino'],'python','post_processing')
sys.path.append(pyduino_path)
import constants
temperature_k_top=constants.kelvin+dat.incon['XX  1'][1][1]
saturated_vapor_pressure_top_pa=constants.svp(temperature_k_top)
saturated_vapor_pressure_top_pa
P_gas_top= dat.incon['XX  1'][1][0]
P_air_top=   dat.incon['XX  1'][1][2]
P_vapor_top=P_gas_top-P_air_top
P_vapor_top
relative_humidity_top=P_vapor_top/saturated_vapor_pressure_top_pa
relative_humidity_top
import numpy as np
matric_potential_top_m = np.log(relative_humidity_top)*constants.R*temperature_k_top/ constants.g / constants.molecular_weight_water
capillary_pressure_top_pa = matric_potential_top_m* constants.rhow_pure_water * constants.g
capillary_pressure_top_pa
print 'from the listing file in tough2 sam6, the capillary pressure is set as -5.e7, very close to what we have calculated here'
text= """this has been tested successfully the initial condition of the top most node 
    XX  1            .10000000E-01
    .1000000000000E+06  .1300000000000E+02  .9897536985191E+05
    This follows a format of P_gas, temperature, P_air. 
    Bear in mind that P_gas=P_air+P_vapour
    """
print text

### below is to test the node after the top one.


