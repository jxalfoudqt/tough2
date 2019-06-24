import os
cwd = os.getcwd()

#execfile(cwd+'/python_code/Evaporation_1D_eos4_pre_process.py')
execfile(cwd+'/python_code/parsing_inputfile.py')
execfile(cwd+'/python_code/running_model.py')
execfile(cwd+'/python_code/Evaporation_1D_eos4_post_process.py')
