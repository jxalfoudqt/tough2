


```
import sys
import os 
pyduino_path=os.path.join(os.environ['pyduino'],'python','post_processing')
sys.path.append(pyduino_path)
import constants
temperature_k=273.15+13
saturated_vapor_pressure_pa=constants.svp(temperature_k)
saturated_vapor_pressure_pa
P_gas=1e5
P_air=98975
P_vapor=P_gas-P_air
P_vapor
relative_humidity=P_vapor/saturated_vapor_pressure_pa
relative_humidity
import numpy as np
matric_potential = np.log(relative_humidity)*constants.R*temperature_k/ constants.g / constants.molecular_weight_water
matric_potential
matric_potential_m = np.log(relative_humidity)*constants.R*temperature_k/ constants.g / constants.molecular_weight_water
capillary_pressure_pa = matric_potential* constants.rhow_pure_water * constants.g
capillary_pressure_pa
execfile("python/running_model.py")
execfile("python/read_output.py")
execfile("python/post_process.py")
plt.show()
lst.element.DataFrame
np.log(relative_humidity)*constants.R*temperature_k/ 9.8/constants.molecular_weight_water
constants.g
np.log(relative_humidity)*constants.R*temperature_k/ 9.81/constants.molecular_weight_water
matric_potential=np.log(relative_humidity)*constants.R*temperature_k/ 9.81/constants.molecular_weight_water
matric_potential
capillary_pressure_pa = matric_potential* constants.rhow_pure_water * 9.81
capillary_pressure_pa
constants.rhow_pure_water
capillary_pressure_pa
execfile("python/running_model.py")
execfile("python/running_model.py")
execfile("python/parsing_inputfile.py")
```
