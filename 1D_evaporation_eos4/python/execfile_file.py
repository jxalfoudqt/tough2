import os
cwd = os.getcwd()

#execfile(cwd+'/python/parsing_inputfile.py')

execfile(cwd+'/python/pre_process.py')
execfile(cwd+'/python/running_model.py')
execfile(cwd+'/python/parsing_outputfile.py')
execfile(cwd+'/python/post_process.py')